import subprocess
import tkinter as tk
from tkinter import messagebox


# Function to validate login credentials
def validate_login():
    username = username_entry.get()
    password = password_entry.get()

    # Example validation (replace with your own logic)
    if username == "admin" and password == "123":
        messagebox.showinfo("Login Successful", "Welcome!")
        subprocess.run(["python", "../views/home.py"])

    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")


# Create the main window
root = tk.Tk()
root.title("Login Form")
root.geometry("300x200")

# Username label and entry
tk.Label(root, text="Username:").pack(pady=5)
username_entry = tk.Entry(root)
username_entry.pack(pady=5)

# Password label and entry
tk.Label(root, text="Password:").pack(pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=5)

# Login button
login_button = tk.Button(root, text="Login", command=validate_login)
login_button.pack(pady=10)

# Run the application
root.mainloop()
