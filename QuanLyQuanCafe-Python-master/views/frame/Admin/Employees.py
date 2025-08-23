from tkinter import *

def gui_employees(window):
#frame
    frame = Frame(window, bg="white")
    frame_list = Frame(frame, bg="white", bd=3, relief="solid")

    frame.place(x=200, y=0, width=1500, height=1000)
    frame_list.place(x=30, y=400, width=1270, height=370)
#buttons
    btn_add = Button(frame, text="Thêm", width=15, height=2)
    btn_edit = Button(frame, text="Sửa", width=15, height=2)
    btn_del = Button(frame, text="Xóa", width=15, height=2)
    btn_save = Button(frame, text="Lưu", width=15, height=2)
    btn_export = Button(frame, text="Xuất", width=15, height=2)

    btn_add.place(x=30, y=100)
    btn_edit.place(x=180, y=100)
    btn_del.place(x=330, y=100)
    btn_save.place(x=480, y=100)
    btn_export.place(x=630, y=100)
#...
    entry_search = Entry(frame, width=50)
    btn_search = Button(frame, text="Tìm", width=12, height=2)
    entry_search.place(x=850, y=100, height=40)
    btn_search.place(x=1200, y=100)

#Label
    label_1 = Label(frame, text="Quản Lý Nhân Viên", font=("Times New Roman", 20, "bold"), fg="#000000", bg="white")
    label_1.place(x=30, y=25)

    Label(frame, text="Mã nhân viên", font=("Times New Roman", 14), bg="white").place(x=30, y=180)
    entry_id = Entry(frame, width=28)
    entry_id.place(x=30, y=210, height=25)

    Label(frame, text="Tên nhân viên", font=("Times New Roman", 14), bg="white").place(x=300, y=180)
    entry_name = Entry(frame, width=28)
    entry_name.place(x=300, y=210, height=25)

    Label(frame, text="Email", font=("Times New Roman", 14), bg="white").place(x=600, y=180)
    entry_price = Entry(frame, width=28)
    entry_price.place(x=600, y=210, height=25)

    Label(frame, text="Số điện thoại", font=("Times New Roman", 14), bg="white").place(x=30, y=280)
    entry_type = Entry(frame, width=20)
    entry_type.place(x=30, y=320, height=25)

    Label(frame, text="Ngày sinh", font=("Times New Roman", 14), bg="white").place(x=300, y=280)
    entry_num = Entry(frame, width=20)
    entry_num.place(x=300, y=320, height=25)

    return frame