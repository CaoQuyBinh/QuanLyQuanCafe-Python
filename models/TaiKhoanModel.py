from database.db_connect import execute_query, fetch_query

class TaiKhoan:
    def __init__(self, ID, HoTen, TenDangNhap, MatKhau, Email, Role):
        self.ID = ID
        self.HoTen = HoTen
        self.TenDangNhap = TenDangNhap
        self.MatKhau = MatKhau
        self.Email = Email
        self.Role = Role

    @staticmethod
    def get_all():
        accounts = fetch_query("SELECT * FROM TaiKhoan")
        return [TaiKhoan(*acc) for acc in accounts]

    # Hàm tạo tài khoản
    @staticmethod
    def create(HoTen, TenDangNhap, MatKhau, Email, Role):
        try:
            execute_query("""
                       INSERT INTO TaiKhoan (HoTen, TenDangNhap, MatKhau, Email, Role) 
                       VALUES (?, ?, ?, ?, ?)""",
                (HoTen, TenDangNhap, MatKhau, Email, Role))
        except Exception as e:
            print(f"Lỗi khi tạo tài khoản: {e}")

    # Hàm tìm tài khoản theo ID
    @staticmethod
    def find_by_id(ID):
        result = fetch_query("SELECT * FROM TaiKhoan WHERE ID = ?", (ID,))
        return TaiKhoan(*result[0]) if result else None

    @staticmethod
    def find_by_username(TenDangNhap):
        result = fetch_query("SELECT * FROM TaiKhoan WHERE TenDangNhap = ?", (TenDangNhap,))
        return TaiKhoan(*result[0]) if result else None

    # Hàm tìm kiếm theo key (HoTen hoặc TenDangNhap)
    @staticmethod
    def find_by_search(key):
        result = fetch_query("SELECT * FROM TaiKhoan WHERE HoTen LIKE ? OR TenDangNhap LIKE ?", (f"%{key}%", f"%{key}%"))
        return [TaiKhoan(*row) for row in result]

    # Hàm cập nhật tài khoản
    @staticmethod
    def update(ID, HoTen, TenDangNhap, MatKhau, Email, Role):
        try:
            execute_query("""
                UPDATE TaiKhoan
                SET HoTen = ?, TenDangNhap = ?, MatKhau = ?, Email = ?, Role = ?
                WHERE ID = ?""",
                (HoTen, TenDangNhap, MatKhau, Email, Role, ID))
        except Exception as e:
            print(f"Lỗi khi cập nhật tài khoản: {e}")

    # Hàm xóa theo ID
    @staticmethod
    def delete(ID):
        try:
            execute_query("DELETE FROM TaiKhoan WHERE ID = ?", (ID,))
        except Exception as e:
            print(f"Lỗi khi xóa tài khoản: {e}")