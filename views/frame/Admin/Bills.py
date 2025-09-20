from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview, Style
from controllers.HoaDonController import HoaDonController

def gui_bill(window):
    controller = HoaDonController()

    frame = Frame(window, bg="white")
    frame.place(x=200, y=0, width=1500, height=1000)

    Label(frame, text="Danh sách Hóa Đơn", font=("Times New Roman", 20, "bold"), bg="white").place(x=30, y=20)

    # Thanh tìm kiếm
    entry_search = Entry(frame, width=30)
    entry_search.place(x=850, y=25, height=30)
    btn_search = Button(frame, text="Tìm kiếm", width=12, command=lambda: search_bill())
    btn_search.place(x=1100, y=25)

    frame_list = Frame(frame, bg="white", bd=3, relief="solid")
    frame_list.place(x=30, y=80, width=1270, height=600)

    style = Style()
    style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"))

    tree = Treeview(frame_list, columns=("MaHD", "TenKH", "Ngay", "Tong"), show="headings")
    tree.heading("MaHD", text="Mã HĐ")
    tree.heading("TenKH", text="Tên KH")
    tree.heading("Ngay", text="Ngày")
    tree.heading("Tong", text="Tổng tiền")
    tree.pack(fill=BOTH, expand=True)

    # Các nút chức năng
    btn_edit = Button(frame, text="Sửa hóa đơn", width=15, height=2, command=lambda: edit_bill())
    btn_edit.place(x=200, y=700)
    btn_print = Button(frame, text="In hóa đơn", width=15, height=2, command=lambda: print_bill())
    btn_print.place(x=400, y=700)

    def load_data():
        tree.delete(*tree.get_children())
        for bill in controller.get_bills():
            tree.insert("", "end", values=(bill.MaHD, bill.TenKH, bill.Ngay, bill.Tong))

    def search_bill():
        keyword = entry_search.get().strip()
        tree.delete(*tree.get_children())
        result = controller.search(keyword)
        if result:
            for bill in result:
                tree.insert("", "end", values=(bill.MaHD, bill.TenKH, bill.Ngay, bill.Tong))
        else:
            messagebox.showinfo("Kết quả", "Không tìm thấy hóa đơn!")

    def edit_bill():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Thông báo", "Vui lòng chọn hóa đơn cần sửa!")
            return
        item = tree.item(selected)['values']
        messagebox.showinfo("Sửa", f"Chức năng sửa HĐ {item[0]} (bạn có thể mở form chỉnh sửa ở đây).")

    def print_bill():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Thông báo", "Vui lòng chọn hóa đơn cần in!")
            return
        item = tree.item(selected)['values']
        messagebox.showinfo("In", f"In hóa đơn {item[0]} cho khách {item[1]} với tổng {item[3]:,} đ")

    load_data()
    return frame
