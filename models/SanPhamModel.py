from database.db_connect import execute_query, fetch_query

class SanPham:
    def __init__(self, MaSP, TenSP, LoaiSP, Gia, SoLuong, Anh=None):
        self.MaSP = MaSP
        self.TenSP = TenSP
        self.LoaiSP = LoaiSP
        self.Gia = float(Gia) if Gia is not None else 0.0
        self.SoLuong = int(SoLuong) if SoLuong is not None else 0
        self.Anh = Anh

    @staticmethod
    def _row_to_obj(row):
        if len(row) == 5:  # Nếu không có cột ảnh
            row = (*row, None)
        return SanPham(*row)

    # ===== CRUD =====
    @staticmethod
    def create(MaSP, TenSP, LoaiSP, Gia, SoLuong, Anh=None):
        try:
            execute_query(
                "INSERT INTO SanPham (MaSP, TenSP, LoaiSP, Gia, SoLuong, Anh) VALUES (?, ?, ?, ?, ?, ?)",
                (MaSP, TenSP, LoaiSP, Gia, SoLuong, Anh)
            )
        except Exception:
            execute_query(
                "INSERT INTO SanPham (MaSP, TenSP, LoaiSP, Gia, SoLuong) VALUES (?, ?, ?, ?, ?)",
                (MaSP, TenSP, LoaiSP, Gia, SoLuong)
            )

        if SoLuong > 0:
            SanPham._chinh_kho_theo_cong_thuc(MaSP, SoLuong, is_increase=True)

    @staticmethod
    def update(MaSP, TenSP, LoaiSP, Gia, SoLuong, Anh=None):
        SoLuong = int(SoLuong) if SoLuong is not None else 0
        Gia = float(Gia) if Gia is not None else 0.0
        old_sp = SanPham.find_by_id(MaSP)

        if old_sp:
            delta = SoLuong   # số lượng thêm mới
            new_qty = old_sp.SoLuong + SoLuong   # cộng dồn
        else:
            delta = SoLuong
            new_qty = SoLuong

        try:
            if Anh is not None:
                execute_query("""
                    UPDATE SanPham 
                       SET TenSP=?, LoaiSP=?, Gia=?, SoLuong=?, Anh=? 
                     WHERE MaSP=?
                """, (TenSP, LoaiSP, Gia, new_qty, Anh, MaSP))
            else:
                execute_query("""
                    UPDATE SanPham 
                       SET TenSP=?, LoaiSP=?, Gia=?, SoLuong=? 
                     WHERE MaSP=?
                """, (TenSP, LoaiSP, Gia, new_qty, MaSP))
        except Exception:
            execute_query("""
                UPDATE SanPham SET TenSP=?, LoaiSP=?, Gia=?, SoLuong=? WHERE MaSP=?
            """, (TenSP, LoaiSP, Gia, new_qty, MaSP))

        # Nếu có số lượng mới thì trừ kho theo công thức
        if delta > 0:
            from models.CongThucModel import CongThuc
            from models.KhoModel import Kho
            cong_thuc = CongThuc.get_by_sp(MaSP)
            for MaNL, SoLuongCan in cong_thuc:
                tieu_hao = delta * SoLuongCan
                Kho.update_stock(MaNL, -tieu_hao)

        return True

    @staticmethod
    def delete(MaSP):
        execute_query("DELETE FROM SanPham WHERE MaSP=?", (MaSP,))

    @staticmethod
    def get_all():
        try:
            result = fetch_query("SELECT MaSP, TenSP, LoaiSP, Gia, SoLuong, Anh FROM SanPham")
        except Exception:
            result = fetch_query("SELECT MaSP, TenSP, LoaiSP, Gia, SoLuong FROM SanPham")
        return [SanPham._row_to_obj(row) for row in result]

    @staticmethod
    def find_by_id(MaSP):
        try:
            result = fetch_query(
                "SELECT MaSP, TenSP, LoaiSP, Gia, SoLuong, Anh FROM SanPham WHERE MaSP=?",
                (MaSP,))
        except Exception:
            result = fetch_query(
                "SELECT MaSP, TenSP, LoaiSP, Gia, SoLuong FROM SanPham WHERE MaSP=?",
                (MaSP,))
        return SanPham._row_to_obj(result[0]) if result else None

    @staticmethod
    def find_by_name(TenSP):
        try:
            result = fetch_query(
                "SELECT MaSP, TenSP, LoaiSP, Gia, SoLuong, Anh FROM SanPham WHERE TenSP LIKE ?",
                (f"%{TenSP}%",))
        except Exception:
            result = fetch_query(
                "SELECT MaSP, TenSP, LoaiSP, Gia, SoLuong FROM SanPham WHERE TenSP LIKE ?",
                (f"%{TenSP}%",))
        return [SanPham._row_to_obj(row) for row in result] if result else None

    # ===== MỚI: phục vụ thống kê & UI người dùng =====
    @staticmethod
    def get_categories():
        rows = fetch_query("""
            SELECT DISTINCT LoaiSP
              FROM SanPham
             WHERE LoaiSP IS NOT NULL AND TRIM(LoaiSP) <> ''
             ORDER BY LoaiSP
        """)
        return [r[0] for r in rows]

    @staticmethod
    def get_by_category(LoaiSP):
        try:
            result = fetch_query("""
                SELECT MaSP, TenSP, LoaiSP, Gia, SoLuong, Anh
                  FROM SanPham
                 WHERE LoaiSP = ?
            """, (LoaiSP,))
        except Exception:
            result = fetch_query("""
                SELECT MaSP, TenSP, LoaiSP, Gia, SoLuong
                  FROM SanPham
                 WHERE LoaiSP = ?
            """, (LoaiSP,))
        return [SanPham._row_to_obj(row) for row in result]

    # ===== Điều chỉnh kho theo công thức =====
    @staticmethod
    def _chinh_kho_theo_cong_thuc(MaSP, delta, is_increase=True):
        from models.CongThucModel import CongThuc
        from models.KhoModel import Kho

        cong_thuc = CongThuc.get_by_sp(MaSP)
        if not cong_thuc:
            return

        for MaNL, SoLuongCan in cong_thuc:
            tieu_hao = delta * SoLuongCan
            if is_increase:
                Kho.update_stock(MaNL, -tieu_hao)
            else:
                Kho.update_stock(MaNL, tieu_hao)
