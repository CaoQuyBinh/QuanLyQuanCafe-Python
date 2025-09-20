from tkinter import *
import tkinter as tk
from tkinter.ttk import Treeview, Style, Combobox
from tkinter import messagebox

from controllers.KhoController import KhoController
from controllers.NCCController import NCCController

def gui_storage2(window):
    controller = KhoController()
    ncc_controller = NCCController()
    editing = tk.BooleanVar(value=False)

    def load_data():
        tree.delete(*tree.get_children())
        for storage in controller.load():
            tree.insert("", "end", values=(
                storage.MaNL,
                storage.TenNL,
                storage.GiaNhap,
                storage.TenNCC,
                storage.SoLuong
            ))

    def load_supplier():
        global storage_dict
        storage_dict = {}
        storages = ncc_controller.load()
        if storages:
            for storage in storages:
                storage_dict[storage.MaNCC] = storage.TenNCC
            cb_ncc["values"] = list(storage_dict.values())
        else:
            messagebox.showwarning("Cảnh báo", "Không có nhà cung cấp nào trong cơ sở dữ liệu!")

    def enable(state):
        if state:
            entry_name.config(state="normal")
            cb_ncc.config(state="readonly")
            entry_price.config(state="normal")
            entry_quantity.config(state="normal")
            if not editing.get():
                entry_id.config(state="normal")
        else:
            entry_id.config(state="disabled")
            entry_name.config(state="disabled")
            entry_price.config(state="disabled")
            cb_ncc.config(state="disabled")
            entry_quantity.config(state="disabled")

    def add():
        editing.set(False)
        entry_id.config(state="normal")
        entry_id.delete(0, tk.END)
        entry_name.delete(0, tk.END)
        entry_price.delete(0, tk.END)
        cb_ncc.set("")
        entry_quantity.delete(0, tk.END)
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
            load_supplier()
            cb_ncc.set(item_values[3])
            entry_price.delete(0, tk.END)
            entry_price.insert(0, item_values[2])
            entry_quantity.delete(0, tk.END)
            entry_quantity.insert(0, item_values[4])
            editing.set(True)
            enable(True)
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một nguyên liệu để sửa!")

    def save():
        MaNL = entry_id.get().strip()
        TenNL = entry_name.get().strip()
        TenNCC = cb_ncc.get().strip()
        GiaNhap = entry_price.get().strip()
        SoLuong = entry_quantity.get().strip()

        if not MaNL or not TenNL or not TenNCC or not GiaNhap or not SoLuong:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        MaNCC = next((key for key, value in storage_dict.items() if value == TenNCC), None)

        if editing.get():
            # ✅ chỉ cộng thêm số lượng
            controller.update_quantity(MaNL, int(SoLuong))
            # vẫn cho phép cập nhật tên + NCC + giá
            controller.edit(MaNL, TenNL, MaNCC, GiaNhap, 0)
            messagebox.showinfo("Thông báo", "Đã cập nhật số lượng + thông tin khác!")
        else:
            if controller.exist(MaNL):
                messagebox.showerror("Lỗi", "Mã nguyên liệu đã tồn tại!")
                return
            controller.add(MaNL, TenNL, MaNCC, GiaNhap, SoLuong)
            messagebox.showinfo("Thông báo", "Thêm nguyên liệu thành công!")

        entry_id.delete(0, tk.END)
        entry_name.delete(0, tk.END)
        entry_price.delete(0, tk.END)
        cb_ncc.set("")
        entry_quantity.delete(0, tk.END)
        enable(False)
        load_data()

    def delete():
        selected_item = tree.selection()
        if selected_item:
            MaNL = tree.item(selected_item)['values'][0]
            controller.delete(MaNL)
            messagebox.showinfo("Thông báo", "Xóa nguyên liệu thành công!")
            load_data()
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một nguyên liệu để xóa!")

    def search():
        name = entry_search.get().strip()
        tree.delete(*tree.get_children())
        storages = controller.search(name)
        if storages:
            for storage in storages:
                sup_name = storage_dict.get(storage.MaNCC, "Không xác định")
                tree.insert("", "end", values=(
                    storage.MaNL,
                    storage.TenNL,
                    storage.GiaNhap,
                    sup_name,
                    storage.SoLuong
                ))
        else:
            messagebox.showinfo("Kết quả", "Không tìm thấy nguyên liệu!")

    # ===== Frame UI =====
    frame = Frame(window, bg="white")
    frame_list = Frame(frame, bg="white", bd=3, relief="solid")

    frame.place(x=200, y=0, width=1500, height=1000)
    frame_list.place(x=30, y=400, width=1270, height=370)

    # Buttons
    btn_add = Button(frame, text="Thêm", width=15, height=2, command=add)
    btn_edit = Button(frame, text="Sửa", width=15, height=2, command=edit)
    btn_del = Button(frame, text="Xóa", width=15, height=2, command=delete)
    btn_save = Button(frame, text="Lưu", width=15, height=2, command=save)

    btn_add.place(x=30, y=100)
    btn_edit.place(x=180, y=100)
    btn_del.place(x=330, y=100)
    btn_save.place(x=480, y=100)

    entry_search = Entry(frame, width=50)
    btn_search = Button(frame, text="Tìm", width=12, height=2, command=search)
    entry_search.place(x=850, y=100, height=40)
    btn_search.place(x=1200, y=100)

    # Labels & Inputs
    label_1 = Label(frame, text="Quản Lý Kho", font=("Times New Roman", 20, "bold"), bg="white")
    label_1.place(x=30, y=25)

    Label(frame, text="Mã nguyên liệu", font=("Times New Roman", 14), bg="white").place(x=30, y=180)
    entry_id = Entry(frame, width=28)
    entry_id.place(x=30, y=210, height=25)

    Label(frame, text="Tên nguyên liệu", font=("Times New Roman", 14), bg="white").place(x=300, y=180)
    entry_name = Entry(frame, width=28)
    entry_name.place(x=300, y=210, height=25)

    Label(frame, text="Giá nhập", font=("Times New Roman", 14), bg="white").place(x=600, y=180)
    entry_price = Entry(frame, width=28)
    entry_price.place(x=600, y=210, height=25)

    Label(frame, text="Nhà cung cấp", font=("Times New Roman", 14), bg="white").place(x=900, y=180)
    cb_ncc = Combobox(frame, state="readonly")
    cb_ncc.place(x=900, y=210, height=25)

    Label(frame, text="Số lượng", font=("Times New Roman", 14), bg="white").place(x=30, y=280)
    entry_quantity = Entry(frame, width=20)
    entry_quantity.place(x=30, y=320, height=25)

    # Treeview
    style = Style()
    style.configure("Treeview", font=("Arial", 11))
    style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))

    columns = ("MaNL", "TenNL", "GiaNhap", "TenNCC", "SoLuong")
    tree = Treeview(frame_list, columns=columns, show="headings")

    tree.heading("MaNL", text="Mã NL")
    tree.heading("TenNL", text="Tên nguyên liệu")
    tree.heading("GiaNhap", text="Giá nhập")
    tree.heading("TenNCC", text="Nhà cung cấp")
    tree.heading("SoLuong", text="Số lượng")

    tree.column("MaNL", width=100, anchor="center")
    tree.column("TenNL", width=200, anchor="w")
    tree.column("GiaNhap", width=150, anchor="e")
    tree.column("TenNCC", width=180, anchor="w")
    tree.column("SoLuong", width=100, anchor="center")

    tree.pack(fill=tk.BOTH, expand=True)

    load_data()
    load_supplier()
    enable(False)

    return frame
