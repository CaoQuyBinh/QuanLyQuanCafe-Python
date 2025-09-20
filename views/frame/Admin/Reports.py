# views/frame/Admin/Reports.py
from tkinter import *
import tkinter as tk
from tkinter.ttk import Treeview, Style, Combobox
from tkinter import filedialog, messagebox
import csv
from collections import defaultdict

# Vẽ biểu đồ bằng matplotlib (không dùng seaborn)
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from controllers.HoaDonController import HoaDonController
from controllers.SanPhamController import SanPhamController
from controllers.KhoController import KhoController


def gui_reports(window):
    hd_ctrl  = HoaDonController()
    sp_ctrl  = SanPhamController()
    kho_ctrl = KhoController()

    current_mode = tk.StringVar(value="Thống kê DT")
    current_canvas = {"obj": None}
    current_rows = []        # dữ liệu đang hiển thị trong bảng (phục vụ Export)

    # =============== KHUNG CHÍNH ===================
    frame = Frame(window, bg="white")
    frame.place(x=200, y=0, width=1500, height=1000)

    Label(frame, text="Báo cáo thống kê",
          font=("Times New Roman", 20, "bold"), bg="white").place(x=30, y=25)

    # Nút bên trái
    btn_detail = Button(frame, text="Chi tiết", width=12, height=2)
    btn_export = Button(frame, text="Xuất",    width=12, height=2)
    btn_detail.place(x=240, y=70)
    btn_export.place(x=390, y=70)

    # Combobox bên phải
    cb_mode = Combobox(frame, state="readonly",
                       values=["Thống kê DT", "Thống kê KH", "Thống kê SP", "Thống kê Kho"])
    cb_mode.set(current_mode.get())
    cb_mode.place(x=1140, y=80, width=160, height=28)

    # Khung biểu đồ + bảng (đúng layout đơn giản)
    chart_area = Frame(frame, bg="white", bd=3, relief="solid")
    table_area = Frame(frame, bg="white", bd=3, relief="solid")
    chart_area.place(x=30, y=140, width=1270, height=320)
    table_area.place(x=30, y=500, width=1270, height=320)

    # Bảng
    style = Style()
    style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
    table = Treeview(table_area, columns=(), show="headings")
    table.pack(fill=tk.BOTH, expand=True)

    # =============== HÀM PHỤ TRỢ ===================
    def clear_chart():
        if current_canvas["obj"] is not None:
            current_canvas["obj"].get_tk_widget().destroy()
            current_canvas["obj"] = None

    def draw_bar(labels, values, title, xlab="", ylab=""):
        clear_chart()
        fig = Figure(figsize=(6, 2.8), dpi=100)  # kích thước phù hợp khung 1270x320
        ax = fig.add_subplot(111)
        ax.bar(labels, values)       # không set màu theo yêu cầu
        ax.set_title(title)
        if xlab: ax.set_xlabel(xlab)
        if ylab: ax.set_ylabel(ylab)
        ax.tick_params(axis='x', labelrotation=0)
        canvas = FigureCanvasTkAgg(fig, master=chart_area)
        canvas.draw()
        canvas.get_tk_widget().place(x=5, y=5, width=1260, height=310)
        current_canvas["obj"] = canvas

    def reset_table(columns, headings):
        # columns: tuple ids; headings: list[(id, title, width, anchor)]
        table.configure(columns=columns)
        for c in table["columns"]:
            table.heading(c, text="")
            table.column(c, width=100)
        table.delete(*table.get_children())
        for cid, title, width, anchor in headings:
            table.heading(cid, text=title)
            table.column(cid, width=width, anchor=anchor)

    # =============== NỘI DUNG CÁC CHẾ ĐỘ ===============
    def render_dt():
        # Biểu đồ doanh thu theo ngày + bảng hoá đơn
        bills = hd_ctrl.load() or []   # HoaDon(MaHD, TenKH, VAT, Ngay, Tong)
        by_date = defaultdict(float)
        for b in bills:
            by_date[str(getattr(b, "Ngay", ""))] += float(getattr(b, "Tong", 0) or 0)

        labels = sorted(by_date.keys())
        values = [by_date[d] for d in labels]
        draw_bar(labels, values, "Thống kê doanh thu theo ngày", xlab="", ylab="Doanh thu")

        cols = ("MaHD", "TenKH", "Ngay", "Tong")
        reset_table(cols, [
            ("MaHD",  "MaHD",   160, "center"),
            ("TenKH", "TenKH",  340, "w"),
            ("Ngay",  "Ngày",   220, "center"),
            ("Tong",  "Tổng",   180, "e"),
        ])
        current_rows.clear()
        for b in bills:
            row = (getattr(b, "MaHD", ""), getattr(b, "TenKH", ""),
                   getattr(b, "Ngay", ""), getattr(b, "Tong", 0))
            current_rows.append(row)
            table.insert("", "end", values=row)

    def render_kh():
        # Doanh thu theo khách hàng
        bills = hd_ctrl.load() or []
        by_cust = defaultdict(float)
        for b in bills:
            by_cust[str(getattr(b, "TenKH", "Khách lẻ"))] += float(getattr(b, "Tong", 0) or 0)

        # Lấy top theo doanh thu
        pairs = sorted(by_cust.items(), key=lambda x: x[1], reverse=True)
        labels = [p[0] for p in pairs]
        values = [p[1] for p in pairs]
        draw_bar(labels, values, "Doanh thu theo khách hàng", ylab="Doanh thu")

        cols = ("TenKH", "Tong")
        reset_table(cols, [
            ("TenKH", "Khách hàng", 640, "w"),
            ("Tong",  "Doanh thu",  300, "e"),
        ])
        current_rows.clear()
        for name, money in pairs:
            row = (name, money)
            current_rows.append(row)
            table.insert("", "end", values=row)

    def render_sp():
        # Thống kê sản phẩm (dựa vào tồn kho hiện tại SP hoặc số lượng SP hiện có)
        items = sp_ctrl.load() or []   # SanPham(MaSP, TenSP, LoaiSP, Gia, SoLuong)
        # Biểu đồ top theo số lượng tồn (đơn giản & thống nhất layout)
        pairs = sorted([(i.TenSP, int(i.SoLuong or 0)) for i in items],
                       key=lambda x: x[1], reverse=True)
        labels = [p[0] for p in pairs[:10]]
        values = [p[1] for p in pairs[:10]]
        draw_bar(labels, values, "Top sản phẩm theo số lượng (tồn)", ylab="Số lượng")

        cols = ("MaSP", "TenSP", "LoaiSP", "Gia", "SoLuong")
        reset_table(cols, [
            ("MaSP",    "Mã SP",     120, "center"),
            ("TenSP",   "Tên SP",    360, "w"),
            ("LoaiSP",  "Loại",      180, "w"),
            ("Gia",     "Giá",       160, "e"),
            ("SoLuong", "Số lượng",  140, "center"),
        ])
        current_rows.clear()
        for i in items:
            row = (i.MaSP, i.TenSP, i.LoaiSP, i.Gia, i.SoLuong)
            current_rows.append(row)
            table.insert("", "end", values=row)

    def render_kho():
        # Thống kê kho (nguyên liệu): top theo tồn kho, bảng chi tiết + giá trị tồn
        items = kho_ctrl.load() or []  # Kho(MaNL, TenNL, GiaNhap, SoLuong, MaNCC, TenNCC)
        pairs = sorted([(i.TenNL, int(i.SoLuong or 0)) for i in items],
                       key=lambda x: x[1], reverse=True)
        labels = [p[0] for p in pairs[:10]]
        values = [p[1] for p in pairs[:10]]
        draw_bar(labels, values, "Top nguyên liệu theo tồn kho", ylab="Số lượng")

        cols = ("MaNL", "TenNL", "GiaNhap", "TenNCC", "SoLuong", "GiaTri")
        reset_table(cols, [
            ("MaNL",    "ID",             90,  "center"),
            ("TenNL",   "Tên nguyên liệu",320, "w"),
            ("GiaNhap", "Giá nhập",       140, "e"),
            ("TenNCC",  "Nhà cung cấp",   260, "w"),
            ("SoLuong", "Tồn kho",        120, "center"),
            ("GiaTri",  "Giá trị tồn",    160, "e"),
        ])
        current_rows.clear()
        for i in items:
            giatri = float(i.GiaNhap or 0) * int(i.SoLuong or 0)
            row = (i.MaNL, i.TenNL, i.GiaNhap, i.TenNCC, i.SoLuong, giatri)
            current_rows.append(row)
            table.insert("", "end", values=row)

    # =============== CHUYỂN CHẾ ĐỘ ===============
    def switch_mode(*_):
        mode = cb_mode.get()
        current_mode.set(mode)
        if mode == "Thống kê DT":
            render_dt()
        elif mode == "Thống kê KH":
            render_kh()
        elif mode == "Thống kê SP":
            render_sp()
        elif mode == "Thống kê Kho":
            render_kho()
        else:
            render_dt()

    cb_mode.bind("<<ComboboxSelected>>", switch_mode)

    # =============== XUẤT CSV ===============
    def do_export():
        mode = current_mode.get()
        filename = {
            "Thống kê DT":  "thong_ke_doanh_thu.csv",
            "Thống kê KH":  "thong_ke_khach_hang.csv",
            "Thống kê SP":  "thong_ke_san_pham.csv",
            "Thống kê Kho": "thong_ke_kho.csv",
        }.get(mode, "thong_ke.csv")

        path = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV", "*.csv")],
                                            initialfile=filename)
        if not path:
            return
        # Lấy tên cột đang hiển thị
        cols = table["columns"]
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(cols)
            for row in current_rows:
                w.writerow(list(row))
        messagebox.showinfo("Thành công", f"Đã xuất: {path}")

    btn_export.configure(command=do_export)

    # Nút "Chi tiết" tuỳ ý — để sẵn hook
    btn_detail.configure(command=lambda: messagebox.showinfo("Chi tiết", f"Đang ở: {current_mode.get()}"))

    # Hiển thị mặc định
    switch_mode()

    return frame
