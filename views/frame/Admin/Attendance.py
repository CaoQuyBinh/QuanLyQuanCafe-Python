# views/frame/Admin/Attendance.py
from tkinter import *
import tkinter as tk
from tkinter.ttk import Treeview, Style
from tkinter import messagebox
import datetime

from controllers.AttendanceController import AttendanceController

__all__ = ["gui_attendance"]   # export rõ ràng tên hàm


def gui_attendance(window):
    ctrl = AttendanceController()

    def refresh_today():
        today = datetime.date.today().strftime("%Y-%m-%d")
        tree.delete(*tree.get_children())
        rows = ctrl.list_today(today) or []
        for a in rows:
            tree.insert("", "end", values=(a.MaNV, a.HoTen or "", a.ThoiGian, a.TrangThai))

    def do_collect():
        manv = entry_id.get().strip()
        if not manv:
            messagebox.showwarning("Thiếu dữ liệu", "Nhập Mã NV trước khi thu thập mẫu!")
            return
        try:
            n = ctrl.collect_samples(manv, num_samples=30, cam_index=0)
            messagebox.showinfo("Xong", f"Đã lưu {n} ảnh cho {manv}.")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def do_train():
        try:
            imgs, users = ctrl.train_model()
            messagebox.showinfo("Xong", f"Đã huấn luyện với {imgs} ảnh / {users} nhân viên.")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def do_attend():
        manv = entry_id.get().strip()
        if not manv:
            messagebox.showwarning("Thiếu dữ liệu", "Nhập Mã NV trước khi điểm danh!")
            return
        try:
            if ctrl.has_checked_in_today(manv):
                messagebox.showinfo("Điểm danh", "Hôm nay bạn đã điểm danh rồi!")
                return
            status, ts = ctrl.ensure_attendance_after_login(manv)
            if status == 'checked':
                messagebox.showinfo("Điểm danh", f"Điểm danh thành công lúc {ts}")
            refresh_today()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    frame = Frame(window, bg="white")
    frame_list = Frame(frame, bg="white", bd=3, relief="solid")

    frame.place(x=200, y=0, width=1500, height=1000)
    frame_list.place(x=30, y=200, width=1270, height=620)

    Label(frame, text="Điểm danh (Nhận diện khuôn mặt)",
          font=("Times New Roman", 20, "bold"), bg="white").place(x=30, y=25)

    Label(frame, text="Mã NV:", font=("Times New Roman", 14), bg="white").place(x=30, y=100)
    entry_id = Entry(frame, width=25); entry_id.place(x=100, y=100, height=28)

    Button(frame, text="Thu thập mẫu", width=15, height=2, command=do_collect).place(x=350, y=90)
    Button(frame, text="Huấn luyện",  width=15, height=2, command=do_train).place(x=500, y=90)
    Button(frame, text="Điểm danh",   width=15, height=2, command=do_attend).place(x=650, y=90)
    Button(frame, text="Làm mới",     width=12, height=2, command=refresh_today).place(x=800, y=90, height=40)

    style = Style(); style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
    columns = ("MaNV","HoTen","ThoiGian","TrangThai")
    tree = Treeview(frame_list, columns=columns, show="headings")
    tree.heading("MaNV", text="Mã NV");         tree.column("MaNV", width=120, anchor="center")
    tree.heading("HoTen", text="Họ tên");       tree.column("HoTen", width=260, anchor="w")
    tree.heading("ThoiGian", text="Thời gian"); tree.column("ThoiGian", width=220, anchor="center")
    tree.heading("TrangThai", text="Trạng thái"); tree.column("TrangThai", width=140, anchor="center")
    tree.pack(fill=tk.BOTH, expand=True)

    refresh_today()
    return frame
