from tkinter import *

def gui_bill2(window):
    frame = Frame(window, bg="white")
    frame_bill = Frame(frame, bg="white", bd=3, relief="solid")
    frame_option = Frame(frame, bg="white", bd=3, relief="solid")
    frame_list = Frame(frame, bg="white", bd=3, relief="solid")

    label_1 = Label(frame_bill, text="THÔNG TIN HÓA ĐƠN", font=("Times New Roman", 18, "bold"), fg="#000000", bg="white")
    label_2 = Label(frame_option, text="THÔNG TIN SẢN PHẨM", font=("Times New Roman", 18, "bold"), fg="#000000", bg="white")

    frame.place(x=200, y=0, width=1500, height=1000)
    label_1.place(x=160, y=15)
    label_2.place(x=200, y=15)
    frame_bill.place(x=30, y=60, width=600, height=450)
    frame_option.place(x=650, y=60, width=670, height=450)
    frame_list.place(x=30, y=530, width=1290, height=250)

    label_1 = Label(frame, text="Quản Lý Hóa Đơn", font=("Times New Roman", 20, "bold"), fg="#000000", bg="white")
    label_1.place(x=30, y=20)

    return frame