from tkinter import *
import subprocess

def trang_chu():
    window.destroy()
    subprocess.run(["python", "../views/home.py"])

def dang_xuat():
    window.destroy()
    subprocess.run(["python", "../views/login.py"])

def thoat():
    exit()

def size(event=None):
    width = window.winfo_width()
    height = window.winfo_height()
    frame_menu.place(x=0, y=0, width=220, height=height)
    frame_main.place(x=170, y=0, width=width - 620, height=height)
    frame_option.place(x=1050, y=0, width=width - 250, height=height)
    label_1.place(x=(width - 400) // 2 - 200, y=10)
    # label_2.place(x=200, y=50)
    frame_gioithieu.place(x=20, y=50, width=width - 700, height=height - 100)
    frame_order.place(x=0, y=50, width=width - 1070, height=height - 100)

    num_buttons = len(buttons)
    gap_button = (height - 100) // (num_buttons + 1) + 5
    for i, button in enumerate(buttons):
        button.place(x=20, y=(i + 1) * gap_button, width=150, height=40)

window = Tk()
window.title("Cafe femboy")
window.state('zoomed')
# window.iconbitmap("../Img/icon.ico")

frame_menu = Frame(window, bg="#cfe8ff")
frame_main = Frame(window, bg="#cfe8ff")
frame_option = Frame(window, bg="#cfe8ff")

label_1 = Label(frame_main, text="ỨNG DỤNG QUẢN LÝ QUÁN CAFE", font=("Times New Roman", 20, "bold"), fg="#000000", bg="#cfe8ff")
#label_2 = Label(frame_main, text="THÔNG TIN HÓA ĐƠN", font=("Times New Roman", 20, "bold"), fg="#000000", bg="#A9A9A9")
frame_gioithieu = Frame(frame_main, bg="white", bd=3, relief="solid")
frame_order = Frame(frame_option, bg="white", bd=3, relief="solid")

label_noidung = Label(frame_gioithieu, text="", font=("Arial", 14), fg="black", bg="white")
label_noidung.pack(pady=10)

buttons = []
buttons.append(Button(frame_menu, text="Trang Chủ", font=("Times New Roman", 12)))
buttons.extend([
    Button(frame_menu, text="Sản phẩm", font=("Times New Roman", 12)),
    Button(frame_menu, text="Kho", font=("Times New Roman", 12)),
    Button(frame_menu, text="Nhà cung cấp", font=("Times New Roman", 12)),
    Button(frame_menu, text="Nhân viên", font=("Times New Roman", 12)),
    Button(frame_menu, text="Tài khoản", font=("Times New Roman", 12)),
    Button(frame_menu, text="Hóa đơn", font=("Times New Roman", 12)),
    Button(frame_menu, text="Đăng xuất", bg="#FFA3A3", fg="white", font=("Times New Roman", 12), command=dang_xuat),
    Button(frame_menu, text="Thoát ứng dụng", bg="#FF6666", fg="white", font=("Times New Roman", 12), command=thoat)
])

window.bind("<Configure>", size)
window.mainloop()