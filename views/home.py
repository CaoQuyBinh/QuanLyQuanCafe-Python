from tkinter import *
import subprocess
from PIL import Image, ImageTk
# from Apl import QuanLyDichVu
# from Apl import QuanLyNguoiThue
# from Apl import QuanLyPhongTro
# from Apl import QuanLyNhanVien
# from Apl import QuanLyHopDong


def trang_chu():
    window.destroy()
    subprocess.run(["python", "home.py"])

def dang_xuat():
    window.destroy()
    subprocess.run(["python", "login.py"])

def thoat():
    exit()

def kich_thuoc(event=None):
    dai = window.winfo_width()
    cao = window.winfo_height()
    frame_menu.place(x=0, y=0, width=250, height=cao)
    frame_main.place(x=250, y=0, width=dai - 250, height=cao)
    frame_option.place(x=850, y=0, width=dai - 250, height=cao)
    label_tieude.place(x=(dai - 250) // 2 - 200, y=10)
    frame_gioithieu.place(x=20, y=50, width=dai - 290, height=cao - 100)
    label_gt3.place(x=(dai - 250) // 2 - 150, y=20)
    label_gt2.place(x=(dai - 250) // 2 - 330, y=60)

    SL_buttons = len(buttons)
    khoang_cach_button = (cao - 100) // (SL_buttons + 1) + 5
    for i, button in enumerate(buttons):
        button.place(x=20, y=(i + 1) * khoang_cach_button, width=200, height=40)

window = Tk()
window.title("Cafe femboy")
window.geometry("1250x700")
window.configure(bg="Alice Blue")
# window.iconbitmap("../Picture_Icon/icon.ico")

frame_menu = Frame(window, bg="Powder Blue")
frame_main = Frame(window, bg="#F0F8FF")
frame_option = Frame(window, bg="#808080")

label_tieude = Label(frame_main, text="ỨNG DỤNG QUẢN LÝ PHÒNG TRỌ", font=("Times New Roman", 20, "bold"), fg="#89CFF0", bg="#F0F8FF")
frame_gioithieu = Frame(frame_main, bg="white", bd=3, relief="solid")

label_noidung = Label(frame_gioithieu, text="", font=("Arial", 14), fg="black", bg="white")
label_noidung.pack(pady=10)

# img = Image.open("../Picture_Icon/bg1.png")
# img = img.resize((1000, 660), Image.Resampling.LANCZOS)
# bg_image = ImageTk.PhotoImage(img)
# label_bg = Label(frame_gioithieu, image=bg_image)
# label_bg.place(relwidth=1, relheight=1)

text_gt3 = "Phần mềm quản lý cho thuê"
label_gt3 = Label(frame_gioithieu, text="", font=("Arial", 16, "bold"), fg="red", bg="white")

def gt3(index=0):
    if index < len(text_gt3):
        label_gt3.config(text=text_gt3[:index + 1])
        window.after(250, gt3, index + 1)
gt3()

text_gt2 = "Hiệu quả - Chuyên nghiệp - Tránh sai sót... Quản lý chưa bao giờ dễ dàng hơn thế!"
label_gt2 = Label(frame_gioithieu, text="", font=("Arial", 14), fg="darkblue", bg="white")

def gt2(index=0):
    if index < len(text_gt2):
        label_gt2.config(text=text_gt2[:index + 1])
        window.after(80, gt2, index + 1)
gt2()

buttons = []
buttons.append(Button(frame_menu, text="Trang Chủ", font=("Times New Roman", 12)))
buttons.append(Button(frame_menu, text="Tạo tài khoản nhân viên", font=("Times New Roman", 12)))
buttons.append(Button(frame_menu, text="Quản lý nhân viên", font=("Times New Roman", 12)))
buttons.extend([
    Button(frame_menu, text="Trang chủ", font=("Times New Roman", 12), command=trang_chu),
    Button(frame_menu, text="Xem thông tin tài khoản", font=("Times New Roman", 12)),
    Button(frame_menu, text="Phòng Trọ", font=("Times New Roman", 12)),
    Button(frame_menu, text="Chỉ số điện nước", font=("Times New Roman", 12)),
    Button(frame_menu, text="Hóa đơn", font=("Times New Roman", 12)),
    Button(frame_menu, text="Dịch vụ", font=("Times New Roman", 12)),
    Button(frame_menu, text="Thống kê", font=("Times New Roman", 12)),
    Button(frame_menu, text="Hợp đồng thuê", font=("Times New Roman", 12)),
    Button(frame_menu, text="Đăng xuất", bg="#FFA3A3", fg="white", font=("Times New Roman", 12), command=dang_xuat),
    Button(frame_menu, text="Thoát ứng dụng", bg="#FF6666", fg="white", font=("Times New Roman", 12), command=thoat)
])

window.bind("<Configure>", kich_thuoc)
window.mainloop()