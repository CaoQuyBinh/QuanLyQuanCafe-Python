from tkinter import *
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Treeview, Style, Combobox
import csv

# Đổi import nếu controller của bạn tên khác
from controllers.TaiKhoanController import TaiKhoanController


def gui_accounts(window):
    ctrl = TaiKhoanController()
    editing = tk.BooleanVar(value=False)

    # ---------- helpers ----------
    def gv(obj, *names):
        """Get value from object/dict by trying several field names."""
        for n in names:
            if hasattr(obj, n):
                return getattr(obj, n)
            if isinstance(obj, dict) and n in obj:
                return obj[n]
        return ""

    # ================== HÀM XỬ LÝ ==================
    def load_data():
        tree.delete(*tree.get_children())
        rows = ctrl.load() or []
        for acc in rows:
            _id = gv(acc, "ID", "MaNV", "MaTK")
            hoten = gv(acc, "HoTen", "Ho_ten", "HoTenNV", "HoTenTK", "HoVaTen")
            tendn = gv(acc, "TenDangNhap", "TenDN", "Username", "TaiKhoan")
            matkhau = gv(acc, "MatKhau", "Password", "Mat_khau")
            email = gv(acc, "Email", "email")
            role = gv(acc, "Role", "VaiTro", "Vai_tro")
            tree.insert("", "end", values=(_id, hoten, tendn, matkhau, email, role))

    def enable(state: bool):
        state_e = "normal" if state else "disabled"
        # entry_id luôn disabled
        entry_id.config(state="disabled")
        entry_name.config(state=state_e)
        entry_user.config(state=state_e)
        entry_pass.config(state=state_e)
        entry_email.config(state=state_e)
        cb_role.config(state="readonly" if state else "disabled")

    def reset_fields():
        entry_id.delete(0, tk.END)
        entry_name.delete(0, tk.END)
        entry_user.delete(0, tk.END)
        entry_pass.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        cb_role.set("")

    def on_add():
        editing.set(False)
        reset_fields()
        enable(True)
        entry_name.focus_set()  # Focus không phải ID

    def on_edit():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn tài khoản để sửa!")
            return
        vals = tree.item(sel[0])["values"]
        reset_fields()
        entry_id.insert(0, vals[0])
        entry_name.insert(0, vals[1])
        entry_user.insert(0, vals[2])
        entry_pass.insert(0, vals[3])
        entry_email.insert(0, vals[4])
        cb_role.set(vals[5] if vals[5] else "")
        editing.set(True)
        enable(True)

    def on_save():
        ID = str(entry_id.get()).strip()
        HoTen = entry_name.get().strip()
        TenDN = entry_user.get().strip()
        MatKhau = entry_pass.get().strip()
        Email = entry_email.get().strip()
        Role = cb_role.get().strip()

        if not (HoTen and TenDN and MatKhau and Email and Role):
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin (trừ ID)!")
            return

        try:
            if editing.get():
                ctrl.edit(ID, HoTen, TenDN, MatKhau, Email, Role)
                messagebox.showinfo("Thành công", "Cập nhật tài khoản thành công!")
            else:
                if ctrl.exist_by_username(TenDN):
                    messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại!")
                    return
                ctrl.add(HoTen, TenDN, MatKhau, Email, Role)
                messagebox.showinfo("Thành công", "Thêm tài khoản thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu: {e}")
            return

        reset_fields()
        enable(False)
        load_data()

    def on_delete():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn tài khoản để xóa!")
            return
        ID = tree.item(sel[0])["values"][0]
        if messagebox.askyesno("Xác nhận", f"Xóa tài khoản ID {ID}?"):
            try:
                ctrl.delete(ID)
                messagebox.showinfo("Thành công", "Đã xóa tài khoản.")
                load_data()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa: {e}")

    def on_search():
        key = entry_search.get().strip()
        tree.delete(*tree.get_children())
        try:
            rows = ctrl.search(key) if key else (ctrl.load() or [])
        except Exception as e:
            messagebox.showerror("Lỗi", f"Tìm kiếm lỗi: {e}")
            return
        for acc in rows or []:
            _id = gv(acc, "ID", "MaNV", "MaTK")
            hoten = gv(acc, "HoTen", "Ho_ten", "HoTenNV", "HoTenTK", "HoVaTen")
            tendn = gv(acc, "TenDangNhap", "TenDN", "Username", "TaiKhoan")
            matkhau = gv(acc, "MatKhau", "Password", "Mat_khau")
            email = gv(acc, "Email", "email")
            role = gv(acc, "Role", "VaiTro", "Vai_tro")
            tree.insert("", "end", values=(_id, hoten, tendn, matkhau, email, role))

    def on_export():
        path = filedialog.asksaveasfilename(
            title="Xuất CSV",
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")]
        )
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                w = csv.writer(f)
                w.writerow(["ID", "Họ tên", "Tên đăng nhập", "Mật khẩu", "Email", "Vai trò"])
                for iid in tree.get_children():
                    w.writerow(tree.item(iid)["values"])
            messagebox.showinfo("Xuất", "Đã xuất danh sách ra CSV.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Xuất thất bại: {e}")

    # ================== GIAO DIỆN (PLACE) ==================
    frame = Frame(window, bg="white")
    frame_list = Frame(frame, bg="white", bd=3, relief="solid")

    frame.place(x=200, y=0, width=1500, height=1000)
    frame_list.place(x=30, y=400, width=1270, height=370)

    # Tiêu đề
    Label(frame, text="Quản Lý Tài Khoản",
          font=("Times New Roman", 20, "bold"),
          fg="#000000", bg="white").place(x=30, y=25)

    # Dãy nút
    Button(frame, text="Thêm", width=15, height=2, command=on_add).place(x=30,  y=100)
    Button(frame, text="Sửa",  width=15, height=2, command=on_edit).place(x=180, y=100)
    Button(frame, text="Xóa",  width=15, height=2, command=on_delete).place(x=330, y=100)
    Button(frame, text="Lưu",  width=15, height=2, command=on_save).place(x=480, y=100)
    Button(frame, text="Xuất", width=15, height=2, command=on_export).place(x=630, y=100)

    # Tìm kiếm
    entry_search = Entry(frame, width=50)
    entry_search.place(x=850, y=100, height=40)
    Button(frame, text="Tìm", width=12, height=2, command=on_search).place(x=1200, y=100)

    # Hàng nhập liệu 1
    Label(frame, text="ID", font=("Times New Roman", 14), bg="white").place(x=30, y=170)
    entry_id = Entry(frame, width=28, state="disabled"); entry_id.place(x=30, y=200, height=25)

    Label(frame, text="Họ và tên", font=("Times New Roman", 14), bg="white").place(x=300, y=170)
    entry_name = Entry(frame, width=28); entry_name.place(x=300, y=200, height=25)

    Label(frame, text="Tên tài khoản", font=("Times New Roman", 14), bg="white").place(x=600, y=170)
    entry_user = Entry(frame, width=28); entry_user.place(x=600, y=200, height=25)

    # Hàng nhập liệu 2
    Label(frame, text="Mật khẩu", font=("Times New Roman", 14), bg="white").place(x=30, y=260)
    entry_pass = Entry(frame, width=28, show="*"); entry_pass.place(x=30, y=290, height=25)

    Label(frame, text="Email", font=("Times New Roman", 14), bg="white").place(x=300, y=260)
    entry_email = Entry(frame, width=28); entry_email.place(x=300, y=290, height=25)

    Label(frame, text="Vai trò", font=("Times New Roman", 14), bg="white").place(x=600, y=260)
    cb_role = Combobox(frame, values=["Admin", "Staff"], state="readonly")
    cb_role.place(x=600, y=290, width=150, height=25)

    # Bảng
    style = Style()
    style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))

    columns = ("ID", "HoTen", "TenDN", "MatKhau", "Email", "VaiTro")
    tree = Treeview(frame_list, columns=columns, show="headings")

    tree.heading("ID", text="ID")
    tree.heading("HoTen", text="Họ tên")
    tree.heading("TenDN", text="Tên đăng nhập")
    tree.heading("MatKhau", text="Mật khẩu")
    tree.heading("Email", text="Email")
    tree.heading("VaiTro", text="Vai trò")

    tree.column("ID", width=80, anchor="center")
    tree.column("HoTen", width=240, anchor="w")
    tree.column("TenDN", width=180, anchor="w")
    tree.column("MatKhau", width=140, anchor="center")
    tree.column("Email", width=240, anchor="w")
    tree.column("VaiTro", width=120, anchor="center")

    tree.pack(fill=tk.BOTH, expand=True)

    # Khởi tạo
    load_data()
    enable(False)

    return frame