import sys, os
from tkinter import *
from frame.User.Main import gui_main2
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controllers import func, fr

window = Tk()
window.title("Cafe femboy")
window.state('zoomed')
# window.iconbitmap("../Img/icon.ico")
quanly = "Tôi k muốn code"

frame = gui_main2(window)
frame_menu = Frame(window, bg="#cfe8ff")
frame_menu.place(x=0, y=0, width=200, height=1000)
label = Label(frame_menu, text=f"WELCOME \n {quanly} \n (Quản Lý)", font=("Times New Roman", 18, "bold"), fg="#000000", bg="#cfe8ff")
label.place(x=2, y=40)

buttons = []
buttons.extend([
    Button(frame_menu, text="Trang Chủ", font=("Times New Roman", 12), command=lambda: func.home(window)),
    Button(frame_menu, text="Sản phẩm", font=("Times New Roman", 12), command=lambda: fr.product(window)),
    Button(frame_menu, text="Kho", font=("Times New Roman", 12), command=lambda: fr.storage(window)),
    Button(frame_menu, text="Nhà cung cấp", font=("Times New Roman", 12), command=lambda: fr.ncc(window)),
    Button(frame_menu, text="Nhân viên", font=("Times New Roman", 12), command=lambda: fr.employees(window)),
    Button(frame_menu, text="Tài khoản", font=("Times New Roman", 12), command=lambda: fr.account(window)),
    Button(frame_menu, text="Hóa đơn", font=("Times New Roman", 12), command=lambda: fr.bill(window)),
    Button(frame_menu, text="Thống kê", font=("Times New Roman", 12)) #, command=lambda: fr.bill(window)),
])
func.size(buttons)
btn = Button(frame_menu, text="Đăng xuất", font=("Times New Roman", 16, "bold"), fg="black", bg="#cfe8ff", bd=0, relief="flat", cursor="hand2",command=lambda: func.logout(window))
btn.place(x = 40, y = 750)

window.mainloop()