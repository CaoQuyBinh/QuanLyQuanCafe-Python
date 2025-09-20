from database.db_connect import execute_query, fetch_query

class Kho:
    def __init__(self, MaNL, TenNL, GiaNhap, SoLuong, MaNCC, TenNCC):
        self.MaNL = MaNL
        self.TenNL = TenNL
        self.GiaNhap = GiaNhap
        self.SoLuong = SoLuong
        self.MaNCC = MaNCC
        self.TenNCC = TenNCC

    @staticmethod
    def create(MaNL, TenNL, MaNCC, GiaNhap, SoLuong):
        execute_query("""
            INSERT INTO Kho (MaNL, TenNL, GiaNhap, SoLuong, MaNCC)
            VALUES (?, ?, ?, ?, ?)
        """, (MaNL, TenNL, GiaNhap, SoLuong, MaNCC))

    @staticmethod
    def get_all():
        warehouses = fetch_query("""
            SELECT Kho.MaNL, Kho.TenNL, Kho.GiaNhap, Kho.SoLuong, Kho.MaNCC, NCC.TenNCC
            FROM Kho
            LEFT JOIN NCC ON Kho.MaNCC = NCC.MaNCC
        """)
        return [Kho(*warehouse) for warehouse in warehouses]

    @staticmethod
    def find_by_id(MaNL):
        result = fetch_query("""
            SELECT Kho.MaNL, Kho.TenNL, Kho.GiaNhap, Kho.SoLuong, Kho.MaNCC, NCC.TenNCC
            FROM Kho
            LEFT JOIN NCC ON Kho.MaNCC = NCC.MaNCC
            WHERE Kho.MaNL = ?
        """, (MaNL,))
        return Kho(*result[0]) if result else None

    @staticmethod
    def update_stock(MaNL, change):
        execute_query("UPDATE Kho SET SoLuong = SoLuong + ? WHERE MaNL = ?", (change, MaNL))

    @staticmethod
    def update(MaNL, TenNL, GiaNhap, SoLuong, MaNCC):
        execute_query("""
            UPDATE Kho
            SET TenNL = ?, GiaNhap = ?, SoLuong = ?, MaNCC = ?
            WHERE MaNL = ?
        """, (TenNL, GiaNhap, SoLuong, MaNCC, MaNL))

    @staticmethod
    def delete(MaNL):
        execute_query("DELETE FROM Kho WHERE MaNL = ?", (MaNL,))

    @staticmethod
    def find_by_name(TenNL):
        result = fetch_query("""
            SELECT Kho.MaNL, Kho.TenNL, Kho.GiaNhap, Kho.SoLuong, Kho.MaNCC, NCC.TenNCC
            FROM Kho
            LEFT JOIN NCC ON Kho.MaNCC = NCC.MaNCC
            WHERE Kho.TenNL LIKE ?
        """, (f"%{TenNL}%",))
        return [Kho(*row) for row in result] if result else None

    @staticmethod
    def update_quantity(MaNL, SoLuongMoi):
        execute_query("""
            UPDATE Kho
            SET SoLuong = SoLuong + ?
            WHERE MaNL = ?
        """,(SoLuongMoi, MaNL))