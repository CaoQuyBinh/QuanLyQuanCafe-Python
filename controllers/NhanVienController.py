from models.NhanVienModel import NhanVien

class NhanVienController:
    def __init__(self):
        pass

    def add(self, Ten, Email, ChucVu, NgaySinh):
        NhanVien.create(Ten, Email, ChucVu, NgaySinh)

    def load(self):
        return NhanVien.get_all()

    def edit(self, MaNV, Ten, Email, ChucVu, NgaySinh):
        NhanVien.update(MaNV, Ten, Email, ChucVu, NgaySinh)

    def delete(self, MaNV):
        NhanVien.delete(MaNV)

    def search(self, Ten):
        return NhanVien.find_by_name(Ten)

    def exist(self, MaNV):
        return NhanVien.find_by_id(MaNV) is not None

    def load_NV(self, cbNV):
        self.nv_dict = NhanVien.load_NV()
        cbNV["values"] = list(self.nv_dict.keys())