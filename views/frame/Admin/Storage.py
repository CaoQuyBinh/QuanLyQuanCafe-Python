# views/frame/Admin/Storage.py
from tkinter import *
import tkinter as tk
from tkinter.ttk import Treeview, Style, Combobox
from tkinter import messagebox, filedialog
import csv

from controllers.KhoController import KhoController
from controllers.NCCController import NCCController
from controllers.LichSuNhapKhoController import LichSuNhapKhoController


def gui_storage(window):
    kho = KhoController()
    ncc = NCCController()
    history = LichSuNhapKhoController()
    editing = tk.BooleanVar(value=False)

    # =============== HÀM XỬ LÝ ===================
    def load_data():
        tree.delete(*tree.get_children())
        items = kho.load() or []
        for k in items:
            # Kho(MaNL, TenNL, GiaNhap, SoLuong, MaNCC, TenNCC)
            tree.insert("", "end", values=(
                k.MaNL, k.TenNL, k.GiaNhap, k.TenNCC, k.SoLuong
            ))

    def enable(state: bool):
        # state True = cho nhập liệu
        entry_id.config(state="normal" if state and not editing.get() else "disabled")
        entry_name.config(state="normal" if state else "disabled")
        entry_price.config(state="normal" if state else "disabled")
        entry_quantity.config(state="normal" if state else "disabled")
        cb_supplier.config(state="readonly" if state else "disabled")

    def reset_fields():
        entry_id.delete(0, tk.END)
        entry_name.delete(0, tk.END)
        entry_price.delete(0, tk.END)
        entry_quantity.delete(0, tk.END)
        cb_supplier.set("")

    def add():
        editing.set(False)
        reset_fields()
        enable(True)

    def edit():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn nguyên liệu để sửa!")
            return
        item = tree.item(selected_item)['values']
        reset_fields()
        entry_id.insert(0, item[0]); entry_id.config(state="disabled")
        entry_name.insert(0, item[1])
        entry_price.insert(0, item[2])
        entry_quantity.insert(0, item[4])
        cb_supplier.set(item[3] or "")
        editing.set(True)
        enable(True)

    def save():
        MaNL = entry_id.get().strip()
        TenNL = entry_name.get().strip()
        GiaNhap = entry_price.get().strip()
        SoLuong = entry_quantity.get().strip()
        ncc_text = cb_supplier.get().strip()
        MaNCC = ncc_text.split(" - ")[0] if ncc_text else None

        if not MaNL or not TenNL or not GiaNhap:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ Mã, Tên, Giá!")
            return

        try:
            GiaNhap = float(GiaNhap)
            SoLuong = int(SoLuong) if SoLuong else 0
        except:
            messagebox.showerror("Lỗi", "Giá/Số lượng không hợp lệ!")
            return

        if editing.get():
            if SoLuong:
                kho.update_quantity(MaNL, SoLuong)
            kho.edit(MaNL, TenNL, MaNCC, GiaNhap, 0)
            messagebox.showinfo("Thông báo", "Cập nhật nguyên liệu thành công!")
        else:
            if kho.exist(MaNL):
                messagebox.showerror("Lỗi", "Mã nguyên liệu đã tồn tại!")
                return
            kho.add(MaNL, TenNL, MaNCC, GiaNhap, SoLuong)
            messagebox.showinfo("Thông báo", "Thêm nguyên liệu thành công!")

        reset_fields()
        enable(False)
        load_data()

    def delete():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn nguyên liệu để xoá!")
            return
        MaNL = tree.item(selected_item)['values'][0]
        kho.delete(MaNL)
        messagebox.showinfo("Thông báo", "Xoá nguyên liệu thành công!")
        load_data()

    def search():
        key = entry_search.get().strip()
        tree.delete(*tree.get_children())
        if not key:
            load_data()
            return
        results = kho.search(key) or []
        for k in results:
            tree.insert("", "end", values=(k.MaNL, k.TenNL, k.GiaNhap, k.TenNCC, k.SoLuong))

    def export_csv():
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            initialfile="danh_sach_kho.csv",
            title="Xuất CSV"
        )
        if not path:
            return
        data = kho.load() or []
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["MaNL", "TenNL", "GiaNhap", "TenNCC", "SoLuong"])
            for k in data:
                w.writerow([k.MaNL, k.TenNL, k.GiaNhap, k.TenNCC, k.SoLuong])
        messagebox.showinfo("Thành công", f"Đã xuất: {path}")

    # ===== Nhập hàng (popup tối giản, lưu lịch sử) =====
    def import_goods():
        top = Toplevel(frame)
        top.title("Nhập hàng")
        top.resizable(False, False)

        # --- Chọn nguyên liệu ---
        Label(top, text="Nguyên liệu:").place(x=10, y=10)
        cb_nl = Combobox(top, state="readonly", width=28)
        nls = kho.load() or []
        nl_list = [f"{x.MaNL} - {x.TenNL}" for x in nls]
        cb_nl['values'] = nl_list
        cb_nl.place(x=120, y=10, width=220, height=26)

        # --- Chọn NCC ---
        Label(top, text="Nhà cung cấp:").place(x=10, y=50)
        cb_ncc = Combobox(top, state="readonly", width=28)
        nccs = ncc.load() or []
        ncc_list = [f"{y.MaNCC} - {y.TenNCC}" for y in nccs]
        cb_ncc['values'] = ncc_list
        cb_ncc.place(x=120, y=50, width=220, height=26)

        # --- Nhập số lượng ---
        Label(top, text="Số lượng:").place(x=10, y=90)
        ent_sl = Entry(top)
        ent_sl.place(x=120, y=90, width=220, height=26)

        # --- Nhập giá ---
        Label(top, text="Giá nhập:").place(x=10, y=130)
        ent_gia = Entry(top)
        ent_gia.place(x=120, y=130, width=220, height=26)

        # Khi chọn nguyên liệu => tự load giá hiện tại
        def on_select_nl(event):
            value = cb_nl.get()
            if not value:
                return
            MaNL = value.split(" - ")[0]
            for x in nls:
                if x.MaNL == MaNL:
                    ent_gia.delete(0, tk.END)
                    ent_gia.insert(0, str(x.GiaNhap))
                    break

        cb_nl.bind("<<ComboboxSelected>>", on_select_nl)

        def do_ok():
            try:
                if not cb_nl.get():
                    messagebox.showwarning("Thiếu thông tin", "Chọn nguyên liệu!")
                    return
                if not cb_ncc.get():
                    messagebox.showwarning("Thiếu thông tin", "Chọn nhà cung cấp!")
                    return

                MaNL = cb_nl.get().split(" - ")[0]
                MaNCC = cb_ncc.get().split(" - ")[0]
                sl = int(ent_sl.get())
                gia = float(ent_gia.get())

                if sl <= 0 or gia <= 0:
                    messagebox.showwarning("Giá trị không hợp lệ", "Số lượng/Giá phải > 0!")
                    return

                history.nhap_hang(MaNL, MaNCC, sl, gia)
                messagebox.showinfo("Thành công", "Đã ghi lịch sử nhập & cập nhật tồn kho.")
                top.destroy()
                load_data()
            except ValueError:
                messagebox.showerror("Lỗi", "Số lượng/Giá không hợp lệ!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu: {e}")

        Button(top, text="Lưu", width=12, command=do_ok, bg="#6FA8DC", fg="white").place(x=120, y=175, width=100, height=30)
        Button(top, text="Huỷ", width=12, command=top.destroy).place(x=240, y=175, width=100, height=30)
        top.geometry("360x220+200+120")


    # =============== GIAO DIỆN ===================
    frame = Frame(window, bg="white")
    frame_list = Frame(frame, bg="white", bd=3, relief="solid")

    frame.place(x=200, y=0, width=1500, height=1000)
    frame_list.place(x=30, y=400, width=1270, height=370)

    # Buttons (giống kiểu Product)
    btn_add = Button(frame, text="Thêm", width=15, height=2, command=add)
    btn_edit = Button(frame, text="Sửa", width=15, height=2, command=edit)
    btn_del = Button(frame, text="Xóa", width=15, height=2, command=delete)
    btn_save = Button(frame, text="Lưu", width=15, height=2, command=save)
    btn_import = Button(frame, text="Nhập hàng", width=15, height=2, command=import_goods)
    btn_export = Button(frame, text="Xuất CSV", width=15, height=2, command=export_csv)

    btn_add.place(x=30,  y=100)
    btn_edit.place(x=180, y=100)
    btn_del.place(x=330, y=100)
    btn_save.place(x=480, y=100)
    btn_import.place(x=630, y=100)
    btn_export.place(x=780, y=100)

    # Tìm kiếm bên phải
    entry_search = Entry(frame, width=50)
    btn_search = Button(frame, text="Tìm", width=12, height=2, command=search)
    entry_search.place(x=930, y=100, height=40)
    btn_search.place(x=1200, y=100)

    Label(frame, text="Quản Lý Kho (Nguyên liệu)", font=("Times New Roman", 20, "bold"),
          fg="#000000", bg="white").place(x=30, y=25)

    # Nhập liệu
    Label(frame, text="Mã NL", font=("Times New Roman", 14), bg="white").place(x=30, y=180)
    entry_id = Entry(frame, width=28)
    entry_id.place(x=30, y=210, height=25)

    Label(frame, text="Tên NL", font=("Times New Roman", 14), bg="white").place(x=300, y=180)
    entry_name = Entry(frame, width=28)
    entry_name.place(x=300, y=210, height=25)

    Label(frame, text="Giá nhập", font=("Times New Roman", 14), bg="white").place(x=600, y=180)
    entry_price = Entry(frame, width=20)
    entry_price.place(x=600, y=210, height=25)

    Label(frame, text="Số lượng (+)", font=("Times New Roman", 14), bg="white").place(x=780, y=180)
    entry_quantity = Entry(frame, width=20)
    entry_quantity.place(x=780, y=210, height=25)

    Label(frame, text="Nhà cung cấp", font=("Times New Roman", 14), bg="white").place(x=980, y=180)
    cb_supplier = Combobox(frame, state="readonly")
    # đổ NCC
    ncc_list = ncc.load() or []
    cb_supplier['values'] = [f"{x.MaNCC} - {x.TenNCC}" for x in ncc_list]
    cb_supplier.place(x=980, y=210, width=250, height=25)

    # Bảng kho
    style = Style()
    style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))

    columns = ("MaNL", "TenNL", "GiaNhap", "TenNCC", "SoLuong")
    tree = Treeview(frame_list, columns=columns, show="headings")
    tree.heading("MaNL", text="ID")
    tree.heading("TenNL", text="Tên nguyên liệu")
    tree.heading("GiaNhap", text="Giá nhập")
    tree.heading("TenNCC", text="Tên nhà cung cấp")
    tree.heading("SoLuong", text="Tồn kho")
    tree.pack(fill=tk.BOTH, expand=True)

    load_data()
    enable(False)

    return frame
