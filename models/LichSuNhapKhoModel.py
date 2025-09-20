# models/LichSuNhapKhoModel.py
from database.db_connect import execute_query, fetch_query

class LichSuNhapKho:
    def __init__(self, MaNhap, MaNL, MaNCC, SoLuong, GiaNhap, Ngay):
        self.MaNhap = MaNhap
        self.MaNL = MaNL
        self.MaNCC = MaNCC
        self.SoLuong = SoLuong
        self.GiaNhap = GiaNhap
        self.Ngay = Ngay

    @staticmethod
    def create(MaNL, MaNCC, SoLuong, GiaNhap, Ngay):
        execute_query("""
            INSERT INTO LichSuNhapKho (MaNL, MaNCC, SoLuong, GiaNhap, Ngay)
            VALUES (?, ?, ?, ?, ?)
        """, (MaNL, MaNCC, SoLuong, GiaNhap, Ngay))

    @staticmethod
    def get_all():
        rows = fetch_query("""
            SELECT MaNhap, MaNL, MaNCC, SoLuong, GiaNhap, Ngay
            FROM LichSuNhapKho
            ORDER BY MaNhap DESC
        """)
        return [LichSuNhapKho(*r) for r in rows]

    @staticmethod
    def get_by_ma_nl(MaNL):
        rows = fetch_query("""
            SELECT MaNhap, MaNL, MaNCC, SoLuong, GiaNhap, Ngay
            FROM LichSuNhapKho
            WHERE MaNL = ?
            ORDER BY MaNhap DESC
        """, (MaNL,))
        return [LichSuNhapKho(*r) for r in rows]
