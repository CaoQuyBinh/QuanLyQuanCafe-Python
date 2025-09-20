from database.db_connect import execute_query, fetch_query

class NCC:
    def __init__(self, MaNCC, TenNCC, SDT):
        self.MaNCC = MaNCC
        self.TenNCC = TenNCC
        self.SDT = SDT

    @staticmethod
    def create(MaNCC, TenNCC, SDT):
        execute_query("INSERT INTO NCC (MaNCC, TenNCC, SDT) VALUES (?, ?, ?)", (MaNCC, TenNCC, SDT))

    @staticmethod
    def get_all():
        suppliers = fetch_query("SELECT * FROM NCC")
        return [NCC(*supplier) for supplier in suppliers]

    @staticmethod
    def find_by_id(MaNCC):
        result = fetch_query("SELECT * FROM NCC WHERE MaNCC= ?", (MaNCC,))
        return NCC(*result[0]) if result else None

    @staticmethod
    def update(MaNCC, TenNCC, SDT):
        execute_query("UPDATE NCC SET TenNCC = ? WHERE MaNCC = ?", (MaNCC, TenNCC, SDT))

    @staticmethod
    def delete(MaNCC):
        execute_query("DELETE FROM Supplier WHERE supId = ?", (MaNCC,))

    @staticmethod
    def find_by_name(TenNCC):
        result = fetch_query("SELECT * FROM Supplier WHERE supName LIKE ?", (f"%{TenNCC}%",))
        return [NCC(*row) for row in result] if result else None