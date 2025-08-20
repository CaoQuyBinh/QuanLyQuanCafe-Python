import subprocess
import tkinter as tk
from tkinter import messagebox


# Function to validate login credentials
def validate_login():
    username = username_entry.get()
    password = password_entry.get()

    # Example validation (replace with your own logic)
    if username == "admin" and password == "123":
        messagebox.showinfo("Thông báo", "Đăng nhập thành công")
        subprocess.run(["python", "../views/home.py"])

    else:
        messagebox.showerror("Thông báo", "Tài khoản hoặc mật khẩu không đúng")

def sign_up():
    subprocess.run(["python", "../views/signup"])


# Create the main window
root = tk.Tk()
root.title("Login Form")
root.geometry("500x200")

# Username label and entry
lbl_username = tk.Label(root, text="Username:", font=("Arial", 12, "bold"))
lbl_username.place(x = 20, y = 10, width = 150, height = 50)
username_entry = tk.Entry(root)
username_entry.place(x=180, y=20, width=280, height=30)


# Password label and entry
lbl_password = tk.Label(root, text="Mật khẩu:", font=("Arial", 12, "bold"))
lbl_password.place(x=20, y=70, width=150, height=30)
password_entry = tk.Entry(root, show="●")
password_entry.place(x=180, y=70, width=280, height=30)


# Login button
login_btn = tk.Button(root, text="Đăng nhập", command=validate_login)
login_btn.place(x=40, y=120, width=120, height=40)
signup_btn = tk.Button(text="Đăng ký")
signup_btn.place(x=320, y=120, width=120, height=40)

# Run the application
root.mainloop()
