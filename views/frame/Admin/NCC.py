from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview, Style
import tkinter as tk

from controllers.NCCController import NCCController

def gui_ncc(window):

    controller = NCCController()
    editing = tk.BooleanVar(value=False)

    def load_data():
        tree.delete(*tree.get_children())
        suppliers = controller.load()
        for supplier in suppliers:
            tree.insert("", "end", values=(supplier.MaNCC, supplier.TenNCC, supplier.SDT))

    def enable(state):
        if state:
            entry_name.config(state="normal")
            if not editing.get():
                entry_id.config(state="normal")
                entry_phone.config(state="normal")
        else:
            entry_name.config(state="disabled")
            entry_id.config(state="disabled")
            entry_phone.config(state="disabled")

    def add():
        editing.set(False)
        entry_id.config(state="normal")
        entry_id.delete(0, tk.END)
        entry_name.delete(0, tk.END)
        entry_phone.delete(0, tk.END)
        enable(True)

    def edit():
        selected_item = tree.selection()
        if selected_item:
            item_values = tree.item(selected_item)['values']
            entry_id.config(state="normal")
            entry_id.delete(0, tk.END)
            entry_id.insert(0, item_values[0])
            entry_id.config(state="disabled")
            entry_name.delete(0, tk.END)
            entry_name.insert(0, item_values[1])
            entry_phone.delete(0, tk.END)
            entry_phone.insert(0, item_values[2])
            editing.set(True)
            enable(True)
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một nhà cung cấp để sửa!")

    def save():
        MaNCC = entry_id.get().strip()
        TenNCC = entry_name.get().strip()
        SDT = entry_phone.get().strip()
        if not MaNCC or not TenNCC or not SDT:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        if editing.get():
            controller.edit(MaNCC, TenNCC, SDT)
            messagebox.showinfo("Thông báo", "Cập nhật nhà cung cấp thành công!")
        else:
            if controller.exist(MaNCC):
                messagebox.showerror("Lỗi", "Mã nhà cung cấp đã tồn tại!")
                return
            controller.add(MaNCC, TenNCC, SDT)
            messagebox.showinfo("Thông báo", "Thêm nhà cung cấp thành công!")

        entry_id.delete(0, tk.END)
        entry_name.delete(0, tk.END)
        entry_phone.delete(0, tk.END)
        enable(False)
        load_data()

    def delete():
        selected_item = tree.selection()
        if selected_item:
            MaNCC = tree.item(selected_item)['values'][0]
            controller.delete(MaNCC)
            messagebox.showinfo("Thông báo", "Xóa nhà cung cấp thành công!")
            load_data()
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một nhà cung cấp để xóa!")

    def search():
        name = entry_search.get()
        tree.delete(*tree.get_children())
        suppliers = controller.search(name)
        if suppliers:
            for supplier in suppliers:
                tree.insert("", "end", values=(supplier.MaNCC, supplier.TenNCC, supplier.SDT))
        else:
            messagebox.showinfo("Kết quả", "Không tìm thấy nhà cung cấp!")
#frame
    frame = Frame(window, bg="white")
    frame_list = Frame(frame, bg="white", bd=3, relief="solid")

    frame.place(x=200, y=0, width=1500, height=1000)
    frame_list.place(x=30, y=400, width=1270, height=370)
#buttons
    btn_add = Button(frame, text="Thêm", width=15, height=2,command=add)
    btn_edit = Button(frame, text="Sửa", width=15, height=2,command=edit)
    btn_del = Button(frame, text="Xóa", width=15, height=2, command=delete)
    btn_save = Button(frame, text="Lưu", width=15, height=2,command=save)
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
    label_1 = Label(frame, text="Quản Lý Nhà Cung Cấp", font=("Times New Roman", 20, "bold"), fg="#000000", bg="white")
    label_1.place(x=30, y=25)

    Label(frame, text="Mã cung cấp", font=("Times New Roman", 14), bg="white").place(x=30, y=180)
    entry_id = Entry(frame, width=28)
    entry_id.place(x=30, y=210, height=25)

    Label(frame, text="Tên nhà cung cấp", font=("Times New Roman", 14), bg="white").place(x=300, y=180)
    entry_name = Entry(frame, width=28)
    entry_name.place(x=300, y=210, height=25)

    Label(frame, text="Số điện thoại", font=("Times New Roman", 14), bg="white").place(x=30, y=280)
    entry_phone = Entry(frame, width=20)
    entry_phone.place(x=30, y=320, height=25)


    frameTable = tk.Frame(frame)
    frameTable.place(x=30, y=400, width=1270, height=370)

    style = Style()
    style.configure("Treeview", font=("Arial", 11))
    style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), foreground="black", background="#1e3d7b")
    style.map("Treeview.Heading", background=[("active", "#1e3d7b")])
    columns = ("ID", "Tên nhà cung cấp", "SĐT")
    tree = Treeview(frameTable, columns=columns, show="headings", style="Treeview")
    tree.heading("ID", text="ID")
    tree.heading("Tên nhà cung cấp", text="Tên nhà cung cấp")
    tree.heading("SĐT", text="SĐT")
    tree.pack(fill=tk.BOTH, expand=True)
    tree.column("ID", anchor="center")
    tree.column("Tên nhà cung cấp", anchor="w")
    tree.column("SĐT", anchor="w")

    load_data()
    enable(False)

    return frame