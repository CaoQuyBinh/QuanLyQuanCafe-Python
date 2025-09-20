from database.db_connect import execute_query, fetch_query

class NhanVien:
    def __init__(self, MaNV, Ten, Email, ChucVu, NgaySinh):
        self.MaNV = MaNV
        self.Ten = Ten
        self.Email = Email
        self.ChucVu = ChucVu
        self.NgaySinh = NgaySinh

    @staticmethod
    def get_all():
        employees = fetch_query("SELECT * FROM NhanVien")
        return [NhanVien(*emp) for emp in employees]

    # Hàm tạo tài khoản (không insert MaNV, giả sử AUTOINCREMENT)
    @staticmethod
    def create(Ten, Email, ChucVu, NgaySinh):
        try:
            execute_query("""
                          INSERT INTO NhanVien (Ten, Email, ChucVu, NgaySinh) 
                          VALUES (?, ?, ?, ?)""",
                          (Ten, Email, ChucVu, NgaySinh))
        except Exception as e:
            print(f"Lỗi khi thêm nhân viên: {e}")

    # Hàm tìm tài khoản theo ID
    @staticmethod
    def find_by_id(MaNV):
        result = fetch_query("SELECT * FROM NhanVien WHERE MaNV = ?", (MaNV,))
        return NhanVien(*result[0]) if result else None

    @staticmethod
    def find_by_name(Ten):
        result = fetch_query("SELECT * FROM NhanVien WHERE Ten LIKE ?", (f"%{Ten}%",))
        return [NhanVien(*row) for row in result]

    @staticmethod
    def update(MaNV, Ten, Email, ChucVu, NgaySinh):
        try:
            execute_query("""
                   UPDATE NhanVien
                   SET Ten = ?, Email = ?, ChucVu = ?, NgaySinh = ?
                   WHERE MaNV = ?""",
                          (Ten, Email, ChucVu, NgaySinh, MaNV))
        except Exception as e:
            print(f"Lỗi khi cập nhật nhân viên: {e}")

    # Hàm xóa
    @staticmethod
    def delete(MaNV):
        try:
            execute_query("DELETE FROM NhanVien WHERE MaNV = ?", (MaNV,))
        except Exception as e:
            print(f"Lỗi khi xóa nhân viên: {e}")

    @staticmethod
    def load_NV():
        result = fetch_query("SELECT MaNV, Ten FROM NhanVien")
        return {row[1]: row[0] for row in result}