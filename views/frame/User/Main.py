from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox, Treeview, Style
from datetime import datetime
from controllers.SanPhamController import SanPhamController
from controllers.HoaDonController import HoaDonController


def gui_main2(window):
    product_controller = SanPhamController()
    bill_controller = HoaDonController()

    frame = Frame(window, bg="white")
    frame.place(x=200, y=0, width=1500, height=1000)

    # Trạng thái bàn
    tables = {}
    table_status = {}  # {B1: "trong"|"phucvu"|"thanhtoan"}
    current_table = StringVar(value="")

    # Khung bên trái: Danh sách bàn
    frame_tables = Frame(frame, bg="white", bd=3, relief="solid")
    frame_tables.place(x=20, y=80, width=250, height=600)

    Label(frame_tables, text="Bàn", font=("Times New Roman", 16, "bold"), bg="white").pack()

    canvas = Canvas(frame_tables)
    scroll_y = Scrollbar(frame_tables, orient="vertical", command=canvas.yview)
    scroll_frame = Frame(canvas, bg="white")

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set)
    canvas.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")

    def update_table_colors():
        for tb, btn in tables.items():
            if table_status.get(tb) == "phucvu":
                btn.config(bg="green", fg="white")
            elif table_status.get(tb) == "thanhtoan":
                btn.config(bg="lightblue")
            else:
                btn.config(bg="white")

    def select_table(tb):
        current_table.set(tb)
        if table_status.get(tb) != "phucvu":
            table_status[tb] = "phucvu"
        update_table_colors()
        load_table_items()

    for i in range(1, 22):
        tb = f"B{i}"
        btn = Button(
            scroll_frame,
            text=tb,
            width=8,
            height=3,
            command=lambda t=tb: select_table(t)  # CHỈNH Ở ĐÂY
        )
        btn.grid(row=(i - 1) // 3, column=(i - 1) % 3, padx=5, pady=5)
        tables[tb] = btn
        table_status[tb] = "trong"

    # Chú thích
    Label(frame, text="Trống", bg="white").place(x=30, y=700)
    Label(frame, text="Đang phục vụ", bg="green", fg="white").place(x=100, y=700)
    Label(frame, text="Đã thanh toán", bg="lightblue").place(x=250, y=700)

    # Khung thực đơn
    frame_menu = Frame(frame, bg="#e6f0ff", bd=3, relief="solid")
    frame_menu.place(x=300, y=80, width=500, height=600)

    Label(frame_menu, text="Thực đơn", font=("Times New Roman", 16, "bold"), bg="#e6f0ff").pack(pady=10)

    Label(frame_menu, text="Loại:", font=("Times New Roman", 13), bg="#e6f0ff").place(x=20, y=60)
    cb_loai = Combobox(frame_menu, state="readonly", width=25)
    cb_loai.place(x=150, y=60)

    Label(frame_menu, text="Menu:", font=("Times New Roman", 13), bg="#e6f0ff").place(x=20, y=100)
    cb_menu = Combobox(frame_menu, state="readonly", width=25)
    cb_menu.place(x=150, y=100)

    Label(frame_menu, text="Giá:", font=("Times New Roman", 13), bg="#e6f0ff").place(x=20, y=140)
    lbl_price = Label(frame_menu, text="0 đ", font=("Times New Roman", 13, "bold"), fg="green", bg="#e6f0ff")
    lbl_price.place(x=150, y=140)

    Label(frame_menu, text="Số lượng:", font=("Times New Roman", 13), bg="#e6f0ff").place(x=20, y=180)
    qty_var = IntVar(value=1)
    btn_minus = Button(frame_menu, text="-", command=lambda: qty_var.set(max(1, qty_var.get() - 1)))
    btn_minus.place(x=150, y=180)
    entry_qty = Entry(frame_menu, textvariable=qty_var, width=5, justify="center")
    entry_qty.place(x=190, y=180)
    btn_plus = Button(frame_menu, text="+", command=lambda: qty_var.set(qty_var.get() + 1))
    btn_plus.place(x=250, y=180)

    Label(frame_menu, text="Ghi chú:", font=("Times New Roman", 13), bg="#e6f0ff").place(x=20, y=220)
    entry_note = Entry(frame_menu, width=30)
    entry_note.place(x=150, y=220)

    btn_add = Button(frame_menu, text="Thêm", bg="lightgreen", width=15, command=lambda: add_item())
    btn_add.place(x=180, y=270)

    # Khung hóa đơn (bên phải)
    frame_bill = Frame(frame, bg="white", bd=3, relief="solid")
    frame_bill.place(x=820, y=80, width=650, height=600)

    lbl_table = Label(frame_bill, text="Bàn đang chọn: ---", font=("Times New Roman", 15, "bold"), bg="white")
    lbl_table.pack()

    columns = ("TenSP", "SoLuong", "Gia", "ThanhTien")
    tree = Treeview(frame_bill, columns=columns, show="headings")
    tree.heading("TenSP", text="Tên món")
    tree.heading("SoLuong", text="Số lượng")
    tree.heading("Gia", text="Đơn giá")
    tree.heading("ThanhTien", text="Thành tiền")
    tree.pack(fill=BOTH, expand=True)

    lbl_total = Label(frame_bill, text="Tổng cộng: 0 đ", font=("Times New Roman", 15, "bold"), fg="green", bg="white")
    lbl_total.pack()

    btn_pay = Button(frame_bill, text="THANH TOÁN VÀ IN HÓA ĐƠN", bg="lightgreen", font=("Times New Roman", 13, "bold"),
                     command=lambda: pay_bill())
    btn_pay.pack(pady=10)

    # ========== DỮ LIỆU ==============
    menu_items = {}  # {table: [(TenSP, SoLuong, Gia, ThanhTien)]}

    def load_categories():
        loais = product_controller.get_categories()
        cb_loai["values"] = loais
        if loais:
            cb_loai.current(0)
            load_menu_items()

    def load_menu_items(event=None):
        loai = cb_loai.get()
        items = product_controller.get_products_by_category(loai)
        cb_menu["values"] = [sp.TenSP for sp in items]
        if items:
            cb_menu.current(0)
            update_price()

    def update_price(event=None):
        ten = cb_menu.get()
        sp = product_controller.find_by_name(ten)
        if sp:
            lbl_price.config(text=f"{sp.Gia:,} đ")

    cb_loai.bind("<<ComboboxSelected>>", load_menu_items)
    cb_menu.bind("<<ComboboxSelected>>", update_price)

    def add_item():
        tb = current_table.get()
        if not tb:
            messagebox.showwarning("Chưa chọn bàn", "Vui lòng chọn bàn trước khi thêm món")
            return
        ten = cb_menu.get()
        sp = product_controller.find_by_name(ten)
        if not sp:
            return
        soluong = qty_var.get()
        gia = sp.Gia
        thanhtien = gia * soluong

        if tb not in menu_items:
            menu_items[tb] = []
        menu_items[tb].append((ten, soluong, gia, thanhtien))
        load_table_items()

    def load_table_items():
        tb = current_table.get()
        lbl_table.config(text=f"Bàn đang chọn: {tb}")
        tree.delete(*tree.get_children())
        tong = 0
        for item in menu_items.get(tb, []):
            tree.insert("", "end", values=item)
            tong += item[3]
        lbl_total.config(text=f"Tổng cộng: {tong:,} đ")

    def pay_bill():
        tb = current_table.get()
        if not tb or tb not in menu_items or not menu_items[tb]:
            messagebox.showwarning("Lỗi", "Không có món để thanh toán")
            return
        if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn thanh toán hóa đơn?"):
            return

        # Tạo hóa đơn
        MaHD = int(datetime.now().timestamp())  # ID đơn giản theo timestamp
        TenKH = tb
        Ngay = datetime.now().strftime("%d-%m-%Y")
        Tong = sum(item[3] for item in menu_items[tb])

        bill_controller.add_bill(MaHD, TenKH, Ngay, Tong)

        for ten, sl, gia, tt in menu_items[tb]:
            sp = product_controller.find_by_name(ten)
            bill_controller.add_bill_detail(MaHD, TenKH, sp.MaSP, sp.TenSP, sl, gia, Ngay, tt)

        table_status[tb] = "thanhtoan"
        update_table_colors()
        messagebox.showinfo("Thành công", f"Thanh toán thành công cho {tb}")
        menu_items[tb] = []
        load_table_items()

    load_categories()
    update_table_colors()
    return frame
