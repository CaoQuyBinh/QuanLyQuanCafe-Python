import os
import sys
import time
import subprocess
import sqlite3
from datetime import datetime

import tkinter as tk
from tkinter import messagebox

# ============= OPTIONAL: OpenCV for face verify =============
# Cần opencv-contrib-python (để có cv2.face)

from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]   # -> gốc dự án

DB_PATH = PROJECT_ROOT / "QLCafe.db"

def get_connection():
    return sqlite3.connect(str(DB_PATH))

try:
    import cv2
except Exception:
    cv2 = None

from database.db_tables import init_db

# ==================== KẾT NỐI DB ====================
def get_connection():
    return sqlite3.connect("QLCafe.db")

# ==================== FACE AUTH HELPERS ====================
def _project_root():
    # login2.py đang ở views/other_views => quay về root dự án
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def _model_paths():
    root = _project_root()
    model_path = os.path.join(root, "models", "face_lbph.yml")
    labels_path = model_path + ".labels.txt"
    return model_path, labels_path

def _load_label_map(labels_path):
    mapping = {}
    if not os.path.exists(labels_path):
        return mapping
    with open(labels_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            lid, code = line.split(",", 1)
            mapping[int(lid)] = code
    return mapping

def _verify_face_for_user(user_code: str, threshold: float = 60.0, timeout_sec: int = 20, cam_index: int = 0):
    """
    Mở webcam và chỉ chấp nhận khi nhận diện trùng mã nhân viên (user_code).
    Trả về True nếu khớp trong thời gian timeout, ngược lại False.
    """
    if cv2 is None or not hasattr(cv2, "face"):
        messagebox.showerror(
            "Thiếu thư viện",
            "Chưa có OpenCV (cv2.face). Hãy cài:\n\npip install opencv-contrib-python"
        )
        return False

    model_path, labels_path = _model_paths()
    if not os.path.exists(model_path):
        messagebox.showerror(
            "Thiếu model",
            f"Không tìm thấy model nhận diện:\n{model_path}\n\nHãy thu thập mẫu và huấn luyện trước."
        )
        return False

    # Chuẩn bị nhận diện
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(model_path)
    label_map = _load_label_map(labels_path)

    cascade_path = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")
    detector = cv2.CascadeClassifier(cascade_path)

    cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)
    start = time.time()
    ok = False

    # Để hạn chế nhầm, yêu cầu mặt đúng người xuất hiện liên tiếp vài frame
    stable_need = 6
    stable_cnt = 0

    try:
        while time.time() - start < timeout_sec:
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)

            match_this_frame = False
            for (x, y, w, h) in faces:
                face = cv2.resize(gray[y:y+h, x:x+w], (200, 200))
                label, conf = recognizer.predict(face)
                code = label_map.get(label, "UNKNOWN")
                is_ok = (code == str(user_code)) and (conf < threshold)

                color = (0, 255, 0) if is_ok else (0, 0, 255)
                txt = f"{code} ({conf:.1f})"
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame, txt, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

                if is_ok:
                    match_this_frame = True

            if match_this_frame:
                stable_cnt += 1
            else:
                stable_cnt = 0

            if stable_cnt >= stable_need:
                ok = True
                cv2.putText(frame, "XAC THUC OK", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0), 3)
                cv2.imshow("Xac thuc khuon mat", frame)
                cv2.waitKey(600)  # hiển thị 0.6s cho người dùng thấy
                break

            cv2.imshow("Xac thuc khuon mat - nhan Q de huy", frame)
            k = cv2.waitKey(1) & 0xFF
            if k == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

    return ok

# ==================== HÀM ĐĂNG NHẬP ====================
def validate_login():
    username = entry_user.get().strip()
    password = entry_pass.get().strip()

    if not username or not password:
        messagebox.showwarning("Thông báo", "⚠ Vui lòng nhập đầy đủ tài khoản và mật khẩu!")
        return

    # 1) Kiểm tra tài khoản
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT ID, HoTen, Role FROM TaiKhoan WHERE TenDangNhap=? AND MatKhau=?",
                (username, password))
    user = cur.fetchone()
    conn.close()

    if not user:
        messagebox.showerror("Thông báo", "❌ Sai tên đăng nhập hoặc mật khẩu!")
        return

    user_id, ho_ten, role = user

    # 2) Nếu CHƯA chấm công hôm nay -> bắt xác thực khuôn mặt
    today = datetime.now().strftime("%d-%m-%Y")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM Luong WHERE MaNV=? AND Ngay=?", (user_id, today))
        exist = cur.fetchone()

        if not exist:
            # BẮT QUÉT MẶT NGAY
            ok = _verify_face_for_user(str(user_id))
            if not ok:
                messagebox.showerror("Xác thực thất bại", "❌ Không nhận diện được đúng khuôn mặt hoặc đã hủy.")
                return

            # Ghi chấm công
            cur.execute("""
                INSERT INTO Luong (MaNV, Ngay, NgayCong)
                VALUES (?, ?, ?)
            """, (user_id, today, 1))
            conn.commit()
            messagebox.showinfo("Chấm công", "✅ Điểm danh thành công (khuôn mặt khớp).")
        else:
            # Đã có công hôm nay -> bỏ qua quét
            pass

    except Exception as e:
        messagebox.showerror("Lỗi CSDL", f"❌ Lỗi khi chấm công: {e}")
        try:
            conn.rollback()
        except Exception:
            pass
        return
    finally:
        try:
            conn.close()
        except Exception:
            pass

    # 3) Thông báo đăng nhập và điều hướng
    messagebox.showinfo("Thông báo", f"✅ Đăng nhập thành công!\nXin chào {ho_ten} ({role})")

    root.destroy()
    # Dùng đúng interpreter hiện tại để chạy home
    py = sys.executable or "python"
    if str(role).lower() == "admin":
        subprocess.run([py, os.path.join(_project_root(), "views", "home.py")])
    else:
        subprocess.run([py, os.path.join(_project_root(), "views", "home2.py")])

# ==================== ĐỔI MẬT KHẨU / QUÊN MẬT KHẨU ====================
def forgot_pass():
    root.destroy()
    py = sys.executable or "python"
    subprocess.run([py, os.path.join(_project_root(), "views", "other_views", "resetpassword.py")])

def sign_up():
    root.destroy()
    py = sys.executable or "python"
    subprocess.run([py, os.path.join(_project_root(), "views", "other_views", "signup.py")])

# ==================== MAIN WINDOW ====================
if __name__ == "__main__":
    init_db()  # đảm bảo DB đã tạo bảng

    root = tk.Tk()
    root.title("Đăng nhập")
    root.geometry("400x250")
    root.config(bg="#cfe8ff")

    # Frame chính
    main_frame = tk.Frame(root, bg="#cfe8ff", bd=2, relief="groove")
    main_frame.place(relx=0.5, rely=0.5, anchor="center", width=380, height=220)

    # Tiêu đề
    title = tk.Label(main_frame, text="ĐĂNG NHẬP", font=("Arial", 16, "bold"), bg="#cfe8ff")
    title.pack(pady=5)

    # ====== Nhập tài khoản ======
    frame_user = tk.Frame(main_frame, bg="#cfe8ff")
    frame_user.pack(pady=5)
    tk.Label(frame_user, text="Tài khoản:", font=("Arial", 12), bg="#cfe8ff").pack(side="left", padx=5)
    entry_user = tk.Entry(frame_user, font=("Arial", 12), width=20)
    entry_user.pack(side="left", padx=5)

    # ====== Nhập mật khẩu ======
    frame_pass = tk.Frame(main_frame, bg="#cfe8ff")
    frame_pass.pack(pady=5)
    tk.Label(frame_pass, text="Mật khẩu:", font=("Arial", 12), bg="#cfe8ff").pack(side="left", padx=5)
    entry_pass = tk.Entry(frame_pass, font=("Arial", 12), show="*", width=20)
    entry_pass.pack(side="left", padx=5)

    # ====== Các nút ======
    frame_btn = tk.Frame(main_frame, bg="#cfe8ff")
    frame_btn.pack(pady=15)

    btn_login = tk.Button(frame_btn, text="Đăng nhập", font=("Arial", 11, "bold"),
                          bg="#00aaff", fg="white", width=12, relief="flat", command=validate_login)
    btn_login.pack(side="left", padx=5)

    btn_change = tk.Button(frame_btn, text="Đổi mật khẩu", font=("Arial", 11, "bold"),
                           bg="#00aaff", fg="white", width=12, relief="flat", command=forgot_pass)
    btn_change.pack(side="left", padx=5)

    root.mainloop()
