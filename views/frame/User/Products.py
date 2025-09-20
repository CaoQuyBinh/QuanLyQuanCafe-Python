from tkinter import *
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Treeview, Style, Combobox
from PIL import Image, ImageTk
from io import BytesIO

from controllers.SanPhamController import SanPhamController

def gui_product2(window):
    controller = SanPhamController()
    editing = tk.BooleanVar(value=False)
    product_image_data = None  # lưu dữ liệu ảnh

    # =============== HÀM XỬ LÝ ===================
    def load_data():
        tree.delete(*tree.get_children())
        for sp in controller.load():
            tree.insert("", "end", values=(
                sp.MaSP, sp.TenSP, sp.LoaiSP, sp.Gia, sp.SoLuong
            ))

    def enable(state):
        entry_id.config(state="normal" if state else "disabled")
        entry_name.config(state="normal" if state else "disabled")
        cb_category.config(state="readonly" if state else "disabled")
        entry_price.config(state="normal" if state else "disabled")
        entry_quantity.config(state="normal" if state else "disabled")

    def reset_fields():
        entry_id.delete(0, tk.END)
        entry_name.delete(0, tk.END)
        cb_category.set("")
        entry_price.delete(0, tk.END)
        entry_quantity.delete(0, tk.END)
        lbl_preview.config(image="")
        lbl_preview.image = None
        nonlocal product_image_data
        product_image_data = None

    def add():
        editing.set(False)
        reset_fields()
        enable(True)

    def edit():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sản phẩm để sửa!")
            return
        item_values = tree.item(selected_item)['values']
        reset_fields()
        entry_id.insert(0, item_values[0])
        entry_id.config(state="disabled")
        entry_name.insert(0, item_values[1])
        cb_category.set(item_values[2])
        entry_price.insert(0, item_values[3])
        entry_quantity.insert(0, item_values[4])
        # load ảnh nếu có
        sp = controller.find_by_id(item_values[0])
        if sp and sp.Anh:
            show_preview(sp.Anh)
        editing.set(True)
        enable(True)

    def save():
        nonlocal product_image_data
        MaSP = entry_id.get().strip()
        TenSP = entry_name.get().strip()
        LoaiSP = cb_category.get().strip()
        Gia = entry_price.get().strip()
        SoLuong = entry_quantity.get().strip()

        if not MaSP or not TenSP or not LoaiSP or not Gia or not SoLuong:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        if editing.get():
            controller.edit(MaSP, TenSP, LoaiSP, Gia, SoLuong, product_image_data)
            messagebox.showinfo("Thông báo", "Cập nhật sản phẩm thành công!")
        else:
            if controller.exist(MaSP):
                messagebox.showerror("Lỗi", "Mã sản phẩm đã tồn tại!")
                return
            controller.add(MaSP, TenSP, LoaiSP, Gia, SoLuong, product_image_data)
            messagebox.showinfo("Thông báo", "Thêm sản phẩm thành công!")

        reset_fields()
        enable(False)
        load_data()

    def delete():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sản phẩm để xóa!")
            return
        MaSP = tree.item(selected_item)['values'][0]
        controller.delete(MaSP)
        messagebox.showinfo("Thông báo", "Xóa sản phẩm thành công!")
        load_data()

    def search():
        name = entry_search.get().strip()
        tree.delete(*tree.get_children())
        results = controller.search(name)
        if not results:
            messagebox.showinfo("Kết quả", "Không tìm thấy sản phẩm!")
            return
        for sp in results:
            tree.insert("", "end", values=(sp.MaSP, sp.TenSP, sp.LoaiSP, sp.Gia, sp.SoLuong))

    def choose_image():
        nonlocal product_image_data
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")]
        )
        if file_path:
            with open(file_path, "rb") as f:
                product_image_data = f.read()
            show_preview(product_image_data)

    def show_preview(img_data):
        img = Image.open(BytesIO(img_data))
        img.thumbnail((100, 100))
        photo = ImageTk.PhotoImage(img)
        lbl_preview.config(image=photo)
        lbl_preview.image = photo

    # =============== GIAO DIỆN ===================
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

    Label(frame, text="Quản Lý Sản Phẩm", font=("Times New Roman", 20, "bold"),
          fg="#000000", bg="white").place(x=30, y=25)

    # Nhập liệu
    Label(frame, text="Mã SP", font=("Times New Roman", 14), bg="white").place(x=30, y=180)
    entry_id = Entry(frame, width=28)
    entry_id.place(x=30, y=210, height=25)

    Label(frame, text="Tên SP", font=("Times New Roman", 14), bg="white").place(x=300, y=180)
    entry_name = Entry(frame, width=28)
    entry_name.place(x=300, y=210, height=25)

    Label(frame, text="Loại", font=("Times New Roman", 14), bg="white").place(x=600, y=180)
    cb_category = Combobox(frame, values=["Cà phê", "Trà", "Sinh tố", "Khác"], state="readonly")
    cb_category.place(x=600, y=210, width=150, height=25)

    Label(frame, text="Giá", font=("Times New Roman", 14), bg="white").place(x=30, y=280)
    entry_price = Entry(frame, width=20)
    entry_price.place(x=30, y=320, height=25)

    Label(frame, text="Số lượng", font=("Times New Roman", 14), bg="white").place(x=300, y=280)
    entry_quantity = Entry(frame, width=20)
    entry_quantity.place(x=300, y=320, height=25)

    btn_image = Button(frame, text="Chọn ảnh", command=choose_image)
    btn_image.place(x=600, y=280)
    lbl_preview = Label(frame, bg="white")
    lbl_preview.place(x=750, y=260, width=100, height=100)

    # Bảng sản phẩm
    style = Style()
    style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))

    columns = ("MaSP", "TenSP", "LoaiSP", "Gia", "SoLuong")
    tree = Treeview(frame_list, columns=columns, show="headings")
    tree.heading("MaSP", text="Mã SP")
    tree.heading("TenSP", text="Tên SP")
    tree.heading("LoaiSP", text="Loại")
    tree.heading("Gia", text="Giá")
    tree.heading("SoLuong", text="Số lượng")
    tree.pack(fill=tk.BOTH, expand=True)

    load_data()
    enable(False)

    return frame
