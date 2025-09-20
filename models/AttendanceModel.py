# models/AttendanceModel.py
from database.db_connect import execute_query, fetch_query

class Attendance:
    def __init__(self, MaNV, ThoiGian, TrangThai, HinhAnh=None, HoTen=None):
        self.MaNV = MaNV
        self.ThoiGian = ThoiGian
        self.TrangThai = TrangThai
        self.HinhAnh = HinhAnh
        self.HoTen = HoTen

    @staticmethod
    def _ensure_table():
        execute_query("""
        CREATE TABLE IF NOT EXISTS Attendance (
            MaNV TEXT,
            ThoiGian TEXT,
            TrangThai TEXT,
            HinhAnh TEXT
        );
        """, ())

    @staticmethod
    def add(MaNV, ThoiGian, TrangThai, HinhAnh=None):
        Attendance._ensure_table()
        execute_query("""
            INSERT INTO Attendance (MaNV, ThoiGian, TrangThai, HinhAnh)
            VALUES (?, ?, ?, ?)
        """, (MaNV, ThoiGian, TrangThai, HinhAnh))

    @staticmethod
    def list_today(date_str):
        Attendance._ensure_table()
        try:
            rows = fetch_query("""
                SELECT a.MaNV, a.ThoiGian, a.TrangThai, a.HinhAnh, n.TenNV
                  FROM Attendance a
             LEFT JOIN NhanVien n ON n.MaNV = a.MaNV
                 WHERE substr(a.ThoiGian,1,10)=?
              ORDER BY a.ThoiGian DESC
            """, (date_str,))
            return [Attendance(r[0], r[1], r[2], r[3], r[4]) for r in rows]
        except Exception:
            rows = fetch_query("""
                SELECT MaNV, ThoiGian, TrangThai, HinhAnh
                  FROM Attendance
                 WHERE substr(ThoiGian,1,10)=?
              ORDER BY ThoiGian DESC
            """, (date_str,))
            return [Attendance(r[0], r[1], r[2], r[3], None) for r in rows]

    @staticmethod
    def has_checked_in_today(MaNV, date_str):
        Attendance._ensure_table()
        rows = fetch_query(
            "SELECT COUNT(1) FROM Attendance WHERE MaNV=? AND substr(ThoiGian,1,10)=?",
            (MaNV, date_str)
        )
        return rows and rows[0][0] > 0
