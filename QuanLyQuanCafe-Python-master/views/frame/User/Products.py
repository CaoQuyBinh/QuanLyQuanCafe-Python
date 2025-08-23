from tkinter import *

def gui_product2(window):
#frame
    frame = Frame(window, bg="white")
    frame_list = Frame(frame, bg="white", bd=3, relief="solid")
    frame.place(x=200, y=0, width=1500, height=1000)
    frame_list.place(x=30, y=200, width=1270, height=570)
#...
    entry_search = Entry(frame, width=180)
    btn_search = Button(frame, text="Tìm", width=12, height=2)
    entry_search.place(x=30, y=110, height=40)
    btn_search.place(x=1150, y=110)
#Label
    label_1 = Label(frame, text="Quản Lý Sản Phẩm", font=("Times New Roman", 20, "bold"), fg="#000000", bg="white")
    label_1.place(x=30, y=25)

    return frame