import subprocess
import tkinter as tk
from tkinter import messagebox


# Function to validate login credentials
def validate_login():
    username = entry_user.get()
    password = entry_pass.get()

    # Example validation (replace with your own logic)
    if username == "admin" and password == "123":
        messagebox.showinfo("Thông báo", "Đăng nhập thành công")
        root.destroy()
        subprocess.run(["python", "../../views/home.py"])
    elif username == "user" and password == "123":
        messagebox.showinfo("Thông báo", "Đăng nhập thành công")
        root.destroy()
        subprocess.run(["python", "../../views/home2.py"])
    else:
        messagebox.showerror("Thông báo", "Tài khoản hoặc mật khẩu không đúng")

def sign_up():
    root.destroy()
    subprocess.run(["python", "../views/other_views/signup.py"])

def forgot_pass():
    root.destroy()
    subprocess.run(["python", "../views/other_views/resetpassword.py"])


# Create the main window
root = tk.Tk()
root.title("Đăng nhập")
root.geometry("400x250")
root.config(bg="#cfe8ff")

#frame chính (nền xanh nhạt, bo tròn giả bằng border)
main_frame = tk.Frame(root, bg="#cfe8ff", bd=2, relief="groove")
main_frame.place(relx=0.5, rely=0.5, anchor="center", width=380, height=220)

#Tiêu đề
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

btn_register = tk.Button(frame_btn, text="Đăng ký", font=("Arial", 11, "bold"),
                         bg="#00aaff", fg="white", width=12, relief="flat", command=sign_up)
btn_register.pack(side="left", padx=5)


# Run the application
root.mainloop()
