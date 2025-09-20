import sqlite3
from database.db_connect import execute_query, fetch_query
from datetime import datetime

class Luong:
    def __init__(self, MaLuong, MaNV, Ngay, NgayCong):
        self.MaLuong = MaLuong
        self.MaNV = MaNV
        self.Ngay = Ngay
        self.NgayCong = NgayCong

    @staticmethod
    def cham_cong(maNV):
        ngay = datetime.now().strftime("%d-%m-%Y")

        # kiểm tra đã chấm công chưa
        result = fetch_query("SELECT 1 FROM Luong WHERE MaNV=? AND Ngay=?", (maNV, ngay))
        if not result:
            execute_query("INSERT INTO Luong (MaNV, Ngay, NgayCong) VALUES (?, ?, 1)", (maNV, ngay))
            return True
        return False

    @staticmethod
    def tinh_luong_theo_thang(maNV, muc_luong_ngay=300000):
        thang = datetime.now().strftime("%m-%Y")
        result = fetch_query("""
            SELECT COUNT(*) as SoNgayCong
            FROM Luong
            WHERE MaNV=? AND strftime('%m-%Y', Ngay)=?
        """, (maNV, thang))

        so_ngay_cong = result[0][0] if result else 0
        tong_luong = so_ngay_cong * muc_luong_ngay
        return so_ngay_cong, tong_luong

    @staticmethod
    def get_all():
        rows = fetch_query("SELECT * FROM Luong")
        return [Luong(*row) for row in rows]
