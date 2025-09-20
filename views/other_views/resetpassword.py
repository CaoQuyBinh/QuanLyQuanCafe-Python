import tkinter as tk
from tkinter import messagebox
import sqlite3
import re
import subprocess


def reset_password():
    username = entry_user.get().strip()
    email = entry_email.get().strip()
    new_pass = entry_newpass.get().strip()
    confirm_pass = entry_confirmpass.get().strip()

    if not username or not email or not new_pass or not confirm_pass:
        messagebox.showwarning("Cảnh báo", "⚠ Vui lòng nhập đầy đủ thông tin!")
        return

    # Kiểm tra định dạng email
    if not re.match(r"[^@]+@gmail\.com$", email):
        messagebox.showerror("Lỗi", "❌ Email phải có định dạng hợp lệ: ...@gmail.com")
        return

    # Kiểm tra xác nhận mật khẩu
    if new_pass != confirm_pass:
        messagebox.showerror("Lỗi", "❌ Mật khẩu xác nhận không khớp!")
        return

    conn = sqlite3.connect("QLCafe.db")
    cur = conn.cursor()

    # Kiểm tra tài khoản có tồn tại không
    cur.execute("SELECT ID FROM TaiKhoan WHERE TenDangNhap=? AND Email=?", (username, email))
    account = cur.fetchone()
    if not account:
        messagebox.showerror("Lỗi", "❌ Không tìm thấy tài khoản với thông tin đã nhập!")
        conn.close()
        return

    # Cập nhật mật khẩu
    cur.execute("UPDATE TaiKhoan SET MatKhau=? WHERE TenDangNhap=? AND Email=?", (new_pass, username, email))
    conn.commit()
    conn.close()

    messagebox.showinfo("Thành công", "✅ Mật khẩu đã được thay đổi thành công!")
    root.destroy()
    subprocess.run(["python", "login.py"])  # quay lại màn đăng nhập


def go_back():
    root.destroy()
    subprocess.run(["python", "login.py"])


# ===== Giao diện =====
root = tk.Tk()
root.title("Đổi mật khẩu")
root.geometry("420x300")
root.config(bg="#cfe8ff")

main_frame = tk.Frame(root, bg="#cfe8ff", bd=2, relief="groove")
main_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=280)

title = tk.Label(main_frame, text="ĐỔI MẬT KHẨU", font=("Arial", 16, "bold"), bg="#cfe8ff")
title.grid(row=0, column=0, columnspan=2, pady=10)

# Tên tài khoản
tk.Label(main_frame, text="Tên tài khoản:", font=("Arial", 12), bg="#cfe8ff").grid(row=1, column=0, sticky="e", padx=5, pady=5)
entry_user = tk.Entry(main_frame, font=("Arial", 12), width=25)
entry_user.grid(row=1, column=1, padx=5, pady=5)

# Email
tk.Label(main_frame, text="Email:", font=("Arial", 12), bg="#cfe8ff").grid(row=2, column=0, sticky="e", padx=5, pady=5)
entry_email = tk.Entry(main_frame, font=("Arial", 12), width=25)
entry_email.grid(row=2, column=1, padx=5, pady=5)

# Mật khẩu mới
tk.Label(main_frame, text="Mật khẩu mới:", font=("Arial", 12), bg="#cfe8ff").grid(row=3, column=0, sticky="e", padx=5, pady=5)
entry_newpass = tk.Entry(main_frame, font=("Arial", 12), show="*", width=25)
entry_newpass.grid(row=3, column=1, padx=5, pady=5)

# Xác nhận mật khẩu
tk.Label(main_frame, text="Xác nhận mật khẩu:", font=("Arial", 12), bg="#cfe8ff").grid(row=4, column=0, sticky="e", padx=5, pady=5)
entry_confirmpass = tk.Entry(main_frame, font=("Arial", 12), show="*", width=25)
entry_confirmpass.grid(row=4, column=1, padx=5, pady=5)

# Buttons
btn_confirm = tk.Button(main_frame, text="Xác nhận", font=("Arial", 11, "bold"),
                        bg="#00aaff", fg="white", width=12, relief="flat", command=reset_password)
btn_confirm.grid(row=5, column=0, padx=10, pady=15)

btn_back = tk.Button(main_frame, text="Quay lại", font=("Arial", 11, "bold"),
                     bg="#00aaff", fg="white", width=12, relief="flat", command=go_back)
btn_back.grid(row=5, column=1, padx=10, pady=15)

root.mainloop()
