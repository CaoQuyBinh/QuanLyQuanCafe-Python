import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter.ttk import Treeview, Style
import re

from controllers.NhanVienController import NhanVienController

def gui_employees(window):
    controller = NhanVienController()
    editing = tk.BooleanVar(value=False)

    def load_data():
        tree.delete(*tree.get_children())
        employees = controller.load()
        for emp in employees:
            tree.insert("", "end",
                 values=(emp.MaNV, emp.Ten, emp.Email, emp.ChucVu, emp.NgaySinh))

    def enable(state):
        # entry_id luôn disabled, vì MaNV tự tăng hoặc chỉ read-only
        entry_id.config(state="disabled")
        entry_name.config(state="normal" if state else "disabled")
        entry_role.config(state="normal" if state else "disabled")
        entry_email.config(state="normal" if state else "disabled")
        entry_birthday.config(state="normal" if state else "disabled")

    def add():
        editing.set(False)
        entry_id.config(state="disabled")
        entry_id.delete(0, tk.END)  # Xóa MaNV vì không dùng
        for entry in [entry_name, entry_email, entry_role, entry_birthday]:
            entry.config(state="normal")
            entry.delete(0, tk.END)
        enable(True)  # Enable các trường khác, id vẫn disabled

    def edit():
        selected_item = tree.selection()
        if selected_item:
            item_values = tree.item(selected_item)['values']
            entry_id.config(state="normal")
            entry_id.delete(0, tk.END)
            entry_id.insert(0, item_values[0])
            entry_id.config(state="disabled")  # Giữ disabled sau khi điền
            entry_name.delete(0, tk.END)
            entry_name.insert(0, item_values[1])
            entry_email.delete(0, tk.END)
            entry_email.insert(0, item_values[2])
            entry_role.delete(0, tk.END)
            entry_role.insert(0, item_values[3])
            entry_birthday.delete(0, tk.END)
            entry_birthday.insert(0, item_values[4])
            editing.set(True)
            enable(True)
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một nhân viên để sửa!")

    def save():
        MaNV = entry_id.get().strip()
        Ten = entry_name.get().strip()
        Email = entry_email.get().strip()
        ChucVu = entry_role.get().strip()
        NgaySinh = entry_birthday.get().strip()

        if not Ten or not Email or not ChucVu or not NgaySinh:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin (trừ Mã NV)!")
            return

        # Kiểm tra định dạng email
        if not re.match(r"[^@]+@gmail\.com$", Email):
            messagebox.showerror("Lỗi", "Email phải có định dạng hợp lệ")
            return

        if editing.get():
            if not MaNV:
                messagebox.showerror("Lỗi", "Mã NV không hợp lệ cho sửa!")
                return
            controller.edit(MaNV, Ten, Email, ChucVu, NgaySinh)
            messagebox.showinfo("Thông báo", "Cập nhật nhân viên thành công!")
        else:
            # Không kiểm tra exist(MaNV) vì MaNV tự tăng, không nhập
            controller.add(Ten, Email, ChucVu, NgaySinh)
            messagebox.showinfo("Thông báo", "Thêm nhân viên thành công!")

        load_data()
        enable(False)

    def delete():
        selected_item = tree.selection()
        if selected_item:
            if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa nhân viên này?"):
                MaNV = tree.item(selected_item)['values'][0]
                controller.delete(MaNV)
                messagebox.showinfo("Thông báo", "Xóa nhân viên thành công!")
                load_data()
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một nhân viên để xóa!")

    def search():
        name = entry_search.get()
        tree.delete(*tree.get_children())
        employees = controller.search(name)
        if employees:
            for emp in employees:
                tree.insert("", "end", values=(emp.MaNV, emp.Ten, emp.Email, emp.ChucVu, emp.NgaySinh))
        else:
            messagebox.showinfo("Kết quả", "Không tìm thấy nhân viên!")

    # ==== GUI Layout ====
    frame = Frame(window, bg="white")
    frame.place(x=200, y=0, width=1500, height=1000)

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
    entry_search.place(x=850, y=100, height=40)
    btn_search = Button(frame, text="Tìm", width=12, height=2, command=search)
    btn_search.place(x=1200, y=100)

    Label(frame, text="Quản Lý Nhân Viên", font=("Times New Roman", 20, "bold"), bg="white").place(x=30, y=25)
    Label(frame, text="Mã NV", bg="white").place(x=30, y=180)
    entry_id = Entry(frame, width=20, state="disabled")  # Ban đầu disabled
    entry_id.place(x=30, y=210)

    Label(frame, text="Tên", bg="white").place(x=300, y=180)
    entry_name = Entry(frame, width=20)
    entry_name.place(x=300, y=210)

    Label(frame, text="Email", bg="white").place(x=600, y=180)
    entry_email = Entry(frame, width=20)
    entry_email.place(x=600, y=210)

    Label(frame, text="Ngày sinh", bg="white").place(x=30, y=280)
    entry_birthday = Entry(frame, width=20)
    entry_birthday.place(x=30, y=320)

    Label(frame, text="Chức vụ", bg="white").place(x=300, y=280)
    entry_role = Entry(frame, width=20)
    entry_role.place(x=300, y=320)

    # Table
    frameTable = tk.Frame(window)
    frameTable.place(x=240, y=400, width=1270, height=370)

    tree = Treeview(frameTable, columns=("MaNV", "Ten", "Email", "ChucVu", "NgaySinh"), show="headings")
    for col in ("MaNV", "Ten", "Email", "ChucVu", "NgaySinh"):
        tree.heading(col, text=col)
    tree.pack(fill=tk.BOTH, expand=True)

    load_data()
    enable(False)
    return frame