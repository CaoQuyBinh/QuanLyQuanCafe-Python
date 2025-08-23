import sys, os
from tkinter import *
from frame.User.Main import gui_main2
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controllers import func, fr

window = Tk()
window.title("Cafe femboy")
window.state('zoomed')
# window.iconbitmap("../Img/icon.ico")
nhanvien = "Tôi k muốn code"

frame = gui_main2(window)
frame_menu = Frame(window, bg="#cfe8ff")
frame_menu.place(x=0, y=0, width=200, height=1000)
label = Label(frame_menu, text=f"WELCOME \n {nhanvien} \n (Nhân Viên)", font=("Times New Roman", 18, "bold"), fg="#000000", bg="#cfe8ff")
label.place(x=2, y=40)

buttons = []
buttons.extend([
    Button(frame_menu, text="Trang Chủ", font=("Times New Roman", 12), command=lambda: func.home2(window)),
    Button(frame_menu, text="Sản phẩm", font=("Times New Roman", 12), command=lambda: fr.product2(window)),
    Button(frame_menu, text="Kho", font=("Times New Roman", 12), command=lambda: fr.storage2(window)),
    Button(frame_menu, text="Hóa đơn", font=("Times New Roman", 12), command=lambda: fr.bill2(window)),
])
func.size2(buttons)
btn = Button(frame_menu, text="Đăng xuất", font=("Times New Roman", 16, "bold"), fg="black", bg="#cfe8ff", bd=0, relief="flat", cursor="hand2",command=lambda: func.logout(window))
btn.place(x = 40, y = 750)

window.mainloop()