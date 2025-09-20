# controllers/AttendanceController.py
import os, time, datetime, sqlite3
import cv2, numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH    = os.path.join(ROOT, "QLCafe.db")
DATA_DIR   = os.path.join(ROOT, "data", "faces")
MODEL_DIR  = os.path.join(ROOT, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "face_lbph.yml")
LABELS_PATH = MODEL_PATH + ".labels.txt"
CASCADE = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

def get_conn():
    return sqlite3.connect(DB_PATH)

class Attendance:
    def __init__(self, MaNV, HoTen, ThoiGian, TrangThai):
        self.MaNV = MaNV; self.HoTen = HoTen; self.ThoiGian = ThoiGian; self.TrangThai = TrangThai

class AttendanceController:
    def _ensure_dirs(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        os.makedirs(MODEL_DIR, exist_ok=True)

    # ---- đọc danh sách điểm danh hôm nay (có Họ tên) ----
    def list_today(self, ymd):
        sql_tpl = """
        SELECT a.MaNV, COALESCE(t.HoTen,''), a.ThoiGian, COALESCE(a.TrangThai,'')
        FROM {tbl} a
        LEFT JOIN TaiKhoan t ON t.ID = a.MaNV
        WHERE substr(a.ThoiGian,1,10) = ?
        ORDER BY a.ThoiGian DESC
        """
        for tbl in ("Attendance", "DiemDanh"):
            try:
                with get_conn() as conn:
                    cur = conn.cursor()
                    cur.execute(sql_tpl.format(tbl=tbl), (ymd,))
                    rows = cur.fetchall()
                    return [Attendance(*r) for r in rows]
            except sqlite3.OperationalError:
                continue
        return []

    def has_checked_in_today(self, manv, ymd=None):
        if ymd is None:
            ymd = datetime.date.today().strftime("%Y-%m-%d")
        sql_tpl = "SELECT 1 FROM {tbl} WHERE MaNV=? AND substr(ThoiGian,1,10)=? LIMIT 1"
        for tbl in ("Attendance", "DiemDanh"):
            try:
                with get_conn() as conn:
                    cur = conn.cursor()
                    cur.execute(sql_tpl.format(tbl=tbl), (manv, ymd))
                    return cur.fetchone() is not None
            except sqlite3.OperationalError:
                continue
        return False

    def _insert_attendance(self, manv, status="Present"):
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql_tpl = "INSERT INTO {tbl}(MaNV, ThoiGian, TrangThai) VALUES (?,?,?)"
        for tbl in ("Attendance", "DiemDanh"):
            try:
                with get_conn() as conn:
                    cur = conn.cursor()
                    cur.execute(sql_tpl.format(tbl=tbl), (manv, ts, status))
                    conn.commit()
                    return ts
            except sqlite3.OperationalError:
                continue
        raise sqlite3.OperationalError("Không tìm thấy bảng Attendance/DiemDanh trong CSDL.")

    # ---- Thu thập mẫu ----
    def collect_samples(self, manv, num_samples=30, cam_index=0):
        self._ensure_dirs()
        folder = os.path.join(DATA_DIR, str(manv))
        os.makedirs(folder, exist_ok=True)

        cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)
        detector = cv2.CascadeClassifier(CASCADE)
        saved = 0
        try:
            while saved < num_samples:
                ret, frame = cap.read()
                if not ret: break
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x,y,w,h) in faces:
                    face = cv2.resize(gray[y:y+h, x:x+w], (200,200))
                    cv2.imwrite(os.path.join(folder, f"{int(time.time()*1000)}_{saved}.png"), face)
                    saved += 1
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                    cv2.putText(frame, f"{saved}/{num_samples}", (x,y-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
                    if saved >= num_samples: break
                cv2.imshow("Thu thap mau - nhan Q de huy", frame)
                if (cv2.waitKey(1) & 0xFF) == ord('q'):
                    break
        finally:
            cap.release(); cv2.destroyAllWindows()
        if saved == 0:
            raise RuntimeError("Không thu được mẫu nào. Kiểm tra webcam/ánh sáng.")
        return saved

    # ---- Huấn luyện ----
    def train_model(self):
        self._ensure_dirs()
        images, labels = [], []
        label_map = {}  # emp_code -> numeric label
        next_label = 0

        for emp_code in sorted(os.listdir(DATA_DIR)):
            folder = os.path.join(DATA_DIR, emp_code)
            if not os.path.isdir(folder): continue
            if emp_code not in label_map:
                label_map[emp_code] = next_label; next_label += 1
            lab = label_map[emp_code]
            for fn in os.listdir(folder):
                if not fn.lower().endswith((".png",".jpg",".jpeg",".bmp")): continue
                img = cv2.imread(os.path.join(folder, fn), cv2.IMREAD_GRAYSCALE)
                if img is None: continue
                img = cv2.resize(img, (200,200))
                images.append(img); labels.append(lab)

        if not images:
            raise RuntimeError("Không có ảnh mẫu để huấn luyện.")

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.train(images, np.array(labels))
        recognizer.write(MODEL_PATH)

        with open(LABELS_PATH, "w", encoding="utf-8") as f:
            for emp_code, lab in label_map.items():
                f.write(f"{lab},{emp_code}\n")
        return len(images), len(label_map)

    # ---- Xác thực & ghi công ----
    def ensure_attendance_after_login(self, manv, threshold=90, cam_index=0):
        if self.has_checked_in_today(manv):
            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return "already", ts

        if not os.path.exists(MODEL_PATH):
            raise RuntimeError(f"Không tìm thấy model: {MODEL_PATH}. Hãy huấn luyện trước.")

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(MODEL_PATH)

        id2code = {}
        if os.path.exists(LABELS_PATH):
            with open(LABELS_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    lid, code = line.strip().split(",", 1)
                    id2code[int(lid)] = code

        detector = cv2.CascadeClassifier(CASCADE)
        cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)
        stable_need, stable_cnt, ok = 6, 0, False

        try:
            start = time.time()
            while time.time() - start < 20:
                ret, frame = cap.read()
                if not ret: break
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                match_frame = False
                for (x,y,w,h) in faces:
                    face = cv2.resize(gray[y:y+h, x:x+w], (200,200))
                    lab, conf = recognizer.predict(face)
                    code = id2code.get(lab, "UNKNOWN")
                    if code == str(manv) and conf < float(threshold):
                        match_frame = True
                    cv2.rectangle(frame,(x,y),(x+w,y+h),
                                  (0,255,0) if match_frame else (0,0,255),2)
                    cv2.putText(frame, f"{code} ({conf:.1f})",(x,y-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                (0,255,0) if match_frame else (0,0,255),2)
                stable_cnt = stable_cnt + 1 if match_frame else 0
                if stable_cnt >= stable_need:
                    ok = True
                    cv2.imshow("Xac thuc OK", frame)
                    cv2.waitKey(400)
                    break
                cv2.imshow("Dang xac thuc (Nhan Q de huy)", frame)
                if (cv2.waitKey(1) & 0xFF) == ord('q'):
                    break
        finally:
            cap.release(); cv2.destroyAllWindows()

        if not ok:
            raise RuntimeError("Không nhận diện đúng nhân viên. Hãy thử lại/thu thập mẫu thêm & huấn luyện.")

        ts = self._insert_attendance(manv, "Present")
        return "checked", ts
