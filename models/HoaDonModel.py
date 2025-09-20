# models/HoaDonModel.py
from database.db_connect import execute_query, fetch_query

class HoaDon:
    def __init__(self, MaHD, TenKH, Ngay, Tong, VAT=0.0):
        self.MaHD  = str(MaHD) if MaHD is not None else ""
        self.TenKH = TenKH or ""
        self.Ngay  = str(Ngay) if Ngay is not None else ""
        self.Tong  = float(Tong) if Tong is not None else 0.0
        self.VAT   = float(VAT) if VAT is not None else 0.0

    # --------- Internal helpers ----------
    @staticmethod
    def _rows_to_obj_list(rows, has_vat: bool):
        if has_vat:
            # rows: (MaHD, TenKH, VAT, Ngay, Tong)
            return [HoaDon(r[0], r[1], r[3], r[4], r[2]) for r in rows]
        else:
            # rows: (MaHD, TenKH, Ngay, Tong)
            return [HoaDon(r[0], r[1], r[2], r[3], 0.0) for r in rows]

    # --------- CRUD / Query ----------
    @staticmethod
    def get_all():
        """
        Trả về list[HoaDon]. Tự động fallback nếu DB không có cột VAT.
        """
        try:
            rows = fetch_query(
                "SELECT MaHD, TenKH, VAT, Ngay, Tong FROM HoaDon ORDER BY Ngay DESC, MaHD DESC"
            )
            return HoaDon._rows_to_obj_list(rows, has_vat=True)
        except Exception:
            rows = fetch_query(
                "SELECT MaHD, TenKH, Ngay, Tong FROM HoaDon ORDER BY Ngay DESC, MaHD DESC"
            )
            return HoaDon._rows_to_obj_list(rows, has_vat=False)

    # giữ tên cũ cho tương thích
    @staticmethod
    def get_bills():
        return HoaDon.get_all()

    @staticmethod
    def find_by_id(MaHD):
        try:
            rows = fetch_query(
                "SELECT MaHD, TenKH, VAT, Ngay, Tong FROM HoaDon WHERE MaHD=?", (MaHD,)
            )
            if rows:
                r = rows[0]
                return HoaDon(r[0], r[1], r[3], r[4], r[2])
        except Exception:
            rows = fetch_query(
                "SELECT MaHD, TenKH, Ngay, Tong FROM HoaDon WHERE MaHD=?", (MaHD,)
            )
            if rows:
                r = rows[0]
                return HoaDon(r[0], r[1], r[2], r[3], 0.0)
        return None

    @staticmethod
    def search(keyword: str):
        kw = f"%{keyword}%"
        try:
            rows = fetch_query("""
                SELECT MaHD, TenKH, VAT, Ngay, Tong
                  FROM HoaDon
                 WHERE MaHD LIKE ? OR TenKH LIKE ?
                 ORDER BY Ngay DESC, MaHD DESC
            """, (kw, kw))
            return HoaDon._rows_to_obj_list(rows, has_vat=True)
        except Exception:
            rows = fetch_query("""
                SELECT MaHD, TenKH, Ngay, Tong
                  FROM HoaDon
                 WHERE MaHD LIKE ? OR TenKH LIKE ?
                 ORDER BY Ngay DESC, MaHD DESC
            """, (kw, kw))
            return HoaDon._rows_to_obj_list(rows, has_vat=False)

    @staticmethod
    def create(MaHD, TenKH, VAT, Ngay, Tong):
        """
        Tạo hoá đơn. Nếu DB chưa có VAT, sẽ chèn bản ghi không VAT.
        """
        try:
            execute_query("""
                INSERT INTO HoaDon (MaHD, TenKH, VAT, Ngay, Tong)
                VALUES (?, ?, ?, ?, ?)
            """, (MaHD, TenKH, VAT, Ngay, Tong))
        except Exception:
            execute_query("""
                INSERT INTO HoaDon (MaHD, TenKH, Ngay, Tong)
                VALUES (?, ?, ?, ?)
            """, (MaHD, TenKH, Ngay, Tong))

    @staticmethod
    def delete(MaHD):
        execute_query("DELETE FROM HoaDon WHERE MaHD=?", (MaHD,))
