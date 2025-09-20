import subprocess
import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
from database.db_tables import init_db


# ==================== KẾT NỐI DB ====================
def get_connection():
    return sqlite3.connect("QLCafe.db")


# ==================== HÀM ĐĂNG NHẬP ====================
def validate_login():
    username = entry_user.get().strip()
    password = entry_pass.get().strip()

    if not username or not password:
        messagebox.showwarning("Thông báo", "⚠ Vui lòng nhập đầy đủ tài khoản và mật khẩu!")
        return

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT ID, HoTen, Role FROM TaiKhoan WHERE TenDangNhap=? AND MatKhau=?",
                (username, password))
    user = cur.fetchone()
    conn.close()

    if user:
        user_id, ho_ten, role = user
        messagebox.showinfo("Thông báo", f"✅ Đăng nhập thành công!\nXin chào {ho_ten} ({role})")

        # ---- Chấm công ----
        try:
            conn = get_connection()
            cur = conn.cursor()
            today = datetime.now().strftime("%d-%m-%Y")

            cur.execute("SELECT 1 FROM Luong WHERE MaNV=? AND Ngay=?", (user_id, today))
            exist = cur.fetchone()

            if not exist:
                cur.execute("""
                    INSERT INTO Luong (MaNV, Ngay, NgayCong)
                    VALUES (?, ?, ?)
                """, (user_id, today, 1))
                conn.commit()
                messagebox.showinfo("Chấm công", "✅ Bạn đã được chấm công hôm nay.")
            else:
                messagebox.showwarning("Chấm công", "⚠ Bạn đã chấm công hôm nay rồi.")

        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"❌ Lỗi khi chấm công: {e}")
        finally:
            conn.close()

        # ---- Phân quyền ----
        root.destroy()
        if role.lower() == "admin":
            subprocess.run(["python", "../../views/home.py"])
        else:
            subprocess.run(["python", "../../views/home2.py"])
    else:
        messagebox.showerror("Thông báo", "❌ Sai tên đăng nhập hoặc mật khẩu!")


# ==================== QUÊN MẬT KHẨU ====================
def forgot_pass():
    root.destroy()
    subprocess.run(["python", "../other_views/resetpassword.py"])


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