# controllers/AttendanceController.py
import os, time, datetime
import numpy as np
import cv2

from models.AttendanceModel import Attendance

class AttendanceController:
    def __init__(self):
        self.data_dir = os.path.join("data", "faces")
        self.model_dir = "models"
        self.model_path = os.path.join(self.model_dir, "face_lbph.yml")
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.model_dir, exist_ok=True)
        self.cascade_path = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")
        self.detector = cv2.CascadeClassifier(self.cascade_path)

    # --------- Thu thập mẫu ----------
    def collect_samples(self, MaNV: str, num_samples: int = 30, cam_index: int = 0):
        user_dir = os.path.join(self.data_dir, str(MaNV))
        os.makedirs(user_dir, exist_ok=True)
        cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)
        count = 0
        try:
            while True:
                ok, frame = cap.read()
                if not ok: break
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.detector.detectMultiScale(gray, 1.3, 5)
                for (x,y,w,h) in faces:
                    face = gray[y:y+h, x:x+w]
                    face = cv2.resize(face, (200, 200))
                    fn = os.path.join(user_dir, f"{MaNV}_{int(time.time()*1000)}_{count}.png")
                    cv2.imwrite(fn, face)
                    count += 1
                    cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
                cv2.imshow("Thu thap mau - nhan q de thoat", frame)
                k = cv2.waitKey(1) & 0xFF
                if k == ord('q') or count >= num_samples:
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()
        return count

    # --------- Train ----------
    def train_model(self):
        id_map = {}
        next_id = 1
        images, labels = [], []

        for name in os.listdir(self.data_dir):
            user_dir = os.path.join(self.data_dir, name)
            if not os.path.isdir(user_dir):
                continue
            if name not in id_map:
                id_map[name] = next_id
                next_id += 1
            label = id_map[name]
            for fn in os.listdir(user_dir):
                path = os.path.join(user_dir, fn)
                img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                if img is None:
                    continue
                images.append(img)
                labels.append(label)

        if not images:
            raise RuntimeError("Chưa có dữ liệu mẫu để huấn luyện.")

        recognizer = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8)
        recognizer.train(images, np.array(labels, dtype=np.int32))
        recognizer.write(self.model_path)

        with open(self.model_path + ".labels.txt", "w", encoding="utf-8") as f:
            for code, lid in id_map.items():
                f.write(f"{lid},{code}\n")
        return len(images), len(id_map)

    def _load_label_map(self):
        p = self.model_path + ".labels.txt"
        m = {}
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                for line in f:
                    line=line.strip()
                    if not line: continue
                    i,code = line.split(",",1)
                    m[int(i)] = code
        return m

    # --------- Nhận diện chính xác 1 user ----------
    def _verify_face_for_user(self, MaNV: str, cam_index: int = 0, threshold: float = 60.0, timeout_sec: int = 20):
        if not os.path.exists(self.model_path):
            raise RuntimeError("Chưa có model khuôn mặt. Hãy huấn luyện trước.")
        recog = cv2.face.LBPHFaceRecognizer_create()
        recog.read(self.model_path)
        label_map = self._load_label_map()

        cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)
        start = time.time()
        ok = False
        try:
            while time.time() - start < timeout_sec:
                ret, frame = cap.read()
                if not ret: break
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.detector.detectMultiScale(gray, 1.3, 5)
                for (x,y,w,h) in faces:
                    face = cv2.resize(gray[y:y+h, x:x+w], (200, 200))
                    label, conf = recog.predict(face)
                    code = label_map.get(label, "UNKNOWN")
                    color = (0,255,0) if (code == str(MaNV) and conf < threshold) else (0,0,255)
                    cv2.rectangle(frame, (x,y), (x+w,y+h), color, 2)
                    cv2.putText(frame, f"{code} ({conf:.1f})", (x, y-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                    if code == str(MaNV) and conf < threshold:
                        ok = True
                        break
                cv2.imshow("Xac thuc - nhan q de huy", frame)
                k = cv2.waitKey(1) & 0xFF
                if k == ord('q'):
                    break
                if ok:
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()
        return ok

    # --------- Ép điểm danh sau đăng nhập ----------
    def has_checked_in_today(self, MaNV):
        today = datetime.date.today().strftime("%Y-%m-%d")
        return Attendance.has_checked_in_today(MaNV, today)

    def ensure_attendance_after_login(self, MaNV: str):
        today = datetime.date.today().strftime("%Y-%m-%d")
        if Attendance.has_checked_in_today(MaNV, today):
            return ('already', None)

        if not self._verify_face_for_user(MaNV):
            raise RuntimeError("Xác thực khuôn mặt thất bại hoặc hết thời gian.")

        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        Attendance.add(MaNV, ts, "Check-in", None)
        return ('checked', ts)

    # --------- Query danh sách hôm nay ----------
    def list_today(self, ymd: str):
        return Attendance.list_today(ymd)
