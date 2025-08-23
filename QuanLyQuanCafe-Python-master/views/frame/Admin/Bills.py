from tkinter import *

def gui_bill(window):
    frame = Frame(window, bg="white")
    frame_bill = Frame(frame, bg="white", bd=3, relief="solid")
    frame_option = Frame(frame, bg="white", bd=3, relief="solid")

    label_1 = Label(frame_bill, text="THÔNG TIN HÓA ĐƠN", font=("Times New Roman", 18, "bold"), fg="#000000", bg="white")
    label_2 = Label(frame_option, text="LỰA CHỌN", font=("Times New Roman", 18, "bold"), fg="#000000", bg="white")

    frame.place(x=200, y=0, width=1500, height=1000)
    label_1.place(x=260, y=15)
    label_2.place(x=170, y=15)
    frame_bill.place(x=30, y=60, width=800, height=650)
    frame_option.place(x=850, y=60, width=470, height=650)

    return frame