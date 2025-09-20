from models.TaiKhoanModel import TaiKhoan

class TaiKhoanController:
    def __init__(self):
        pass

    def add(self, HoTen, TenDangNhap, MatKhau, Email, Role):
        if self.exist_by_username(TenDangNhap):
            print("Tên tài khoản đã tồn tại!")
            return
        TaiKhoan.create(HoTen, TenDangNhap, MatKhau, Email, Role)

    def edit(self, ID, HoTen, TenDangNhap, MatKhau, Email, Role):
        TaiKhoan.update(ID, HoTen, TenDangNhap, MatKhau, Email, Role)

    def load(self):
        return TaiKhoan.get_all()

    def delete(self, ID):
        TaiKhoan.delete(ID)

    def search(self, key):
        return TaiKhoan.find_by_search(key)

    def exist_by_id(self, ID):
        return bool(TaiKhoan.find_by_id(ID))

    def exist_by_username(self, TenDangNhap):
        return bool(TaiKhoan.find_by_username(TenDangNhap))