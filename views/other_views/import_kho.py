# views/other_views/import_kho.py
from tkinter import *
from tkinter import ttk, messagebox
from controllers.LichSuNhapKhoController import LichSuNhapKhoController
from controllers.NCCController import NCCController

def import_kho_dialog(parent, MaNL: str, TenNL: str, default_MaNCC: str | None = None, on_done=None):
    top = Toplevel(parent)
    top.title("Nhập hàng nguyên liệu")
    top.grab_set()
    top.resizable(False, False)

    ctrl = LichSuNhapKhoController()
    ncc_ctrl = NCCController()

    # Header
    Label(top, text=f"Nguyên liệu: {TenNL} ({MaNL})", font=("Times New Roman", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(10, 10), padx=12, sticky="w")

    # NCC
    Label(top, text="Nhà cung cấp").grid(row=1, column=0, sticky="w", padx=12, pady=6)
    cb_ncc = ttk.Combobox(top, state="readonly", width=28)
    list_ncc = ncc_ctrl.load() or []
    ncc_items = [f"{n.MaNCC} - {n.TenNCC}" for n in list_ncc]
    cb_ncc["values"] = ncc_items
    cb_ncc.grid(row=1, column=1, sticky="w", padx=12, pady=6)

    if default_MaNCC:
        for i, s in enumerate(ncc_items):
            if s.split(" - ")[0] == default_MaNCC:
                cb_ncc.current(i)
                break

    # Số lượng
    Label(top, text="Số lượng nhập").grid(row=2, column=0, sticky="w", padx=12, pady=6)
    ent_sl = Entry(top, width=30)
    ent_sl.grid(row=2, column=1, sticky="w", padx=12, pady=6)

    # Giá nhập
    Label(top, text="Giá nhập (VNĐ)").grid(row=3, column=0, sticky="w", padx=12, pady=6)
    ent_gia = Entry(top, width=30)
    ent_gia.grid(row=3, column=1, sticky="w", padx=12, pady=6)

    def do_save():
        try:
            if not cb_ncc.get():
                messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn nhà cung cấp.")
                return
            MaNCC = cb_ncc.get().split(" - ")[0]
            sl = int(ent_sl.get())
            gia = float(ent_gia.get())
            if sl <= 0 or gia <= 0:
                messagebox.showwarning("Giá trị không hợp lệ", "Số lượng và giá phải > 0.")
                return
            ctrl.nhap_hang(MaNL, MaNCC, sl, gia)
            messagebox.showinfo("Thành công", "Đã ghi lịch sử nhập và cập nhật tồn kho.")
            if on_done:
                on_done()
            top.destroy()
        except ValueError:
            messagebox.showerror("Lỗi", "Số lượng hoặc giá không hợp lệ.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu: {e}")

    # Buttons
    btn_frame = Frame(top)
    btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
    Button(btn_frame, text="Lưu", width=12, command=do_save, bg="#6FA8DC", fg="white").pack(side="left", padx=6)
    Button(btn_frame, text="Huỷ", width=12, command=top.destroy).pack(side="left", padx=6)
