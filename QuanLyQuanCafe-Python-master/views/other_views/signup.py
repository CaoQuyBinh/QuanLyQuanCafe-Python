import subprocess
import tkinter as tk
from tkinter import messagebox


def back():
    root.destroy()
    subprocess.run(["python", "../views/other_views/login.py"])


#main window
root = tk.Tk()
root.title("Đăng Ký")
root.geometry("400x250")
root.config(bg="#cfe8ff")

#frame chính (nền xanh nhạt, bo tròn giả bằng border)
main_frame = tk.Frame(root, bg="#cfe8ff", bd=2, relief="groove")
main_frame.place(relx=0.5, rely=0.5, anchor="center", width=380, height=220)

#Tiêu đề
title = tk.Label(main_frame, text="ĐĂNG KÝ", font=("Arial", 16, "bold"), bg="#cfe8ff")
title.pack(pady=5)

# ====== Nhập tài khoản ======
frame_user = tk.Frame(main_frame, bg="#cfe8ff")
frame_user.pack(pady=5)
tk.Label(frame_user, text="Tài khoản:", font=("Arial", 12), bg="#cfe8ff").pack(side="left", padx=5)
entry_user = tk.Entry(frame_user, font=("Arial", 12), width=20)
entry_user.pack(side="left", padx=5)

# ====== Nhập email ======
frame_email = tk.Frame(main_frame, bg="#cfe8ff")
frame_email.pack(pady=5)
tk.Label(frame_email, text="Email:", font=("Arial", 12), bg="#cfe8ff").pack(side="left", padx=5)
entry_pass = tk.Entry(frame_email, font=("Arial", 12), width=20)
entry_pass.pack(side="left", padx=5)

# ====== Nhập mật khẩu ======
frame_pass = tk.Frame(main_frame, bg="#cfe8ff")
frame_pass.pack(pady=5)
tk.Label(frame_pass, text="Mật khẩu:", font=("Arial", 12), bg="#cfe8ff").pack(side="left", padx=5)
entry_pass = tk.Entry(frame_pass, font=("Arial", 12), show="*", width=20)
entry_pass.pack(side="left", padx=5)

# ====== Các nút ======
frame_btn = tk.Frame(main_frame, bg="#cfe8ff")
frame_btn.pack(pady=15)

btn_login = tk.Button(frame_btn, text="Đăng ký", font=("Arial", 11, "bold"),
                      bg="#00aaff", fg="white", width=12, relief="flat")
btn_login.pack(side="left", padx=5)

btn_change = tk.Button(frame_btn, text="Quay lại", font=("Arial", 11, "bold"),
                       bg="#00aaff", fg="white", width=12, relief="flat", command=back)
btn_change.pack(side="left", padx=5)


# Run the application
root.mainloop()
