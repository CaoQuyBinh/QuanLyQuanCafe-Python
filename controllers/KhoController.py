from models.KhoModel import Kho

class KhoController:
    def __init__(self):
        pass

    def add(self, MaNL, TenNL, MaNCC, GiaNhap, SoLuong):
        Kho.create(MaNL, TenNL, MaNCC, GiaNhap, SoLuong)

    def load(self):
        return Kho.get_all()

    def edit(self, MaNL, TenNL, MaNCC, GiaNhap, SoLuong):
        Kho.update(MaNL, TenNL, GiaNhap, SoLuong, MaNCC)

    def delete(self, MaNL):
        Kho.delete(MaNL)

    def search(self, TenNL):
        return Kho.find_by_name(TenNL)

    def exist(self, MaNL):
        return Kho.find_by_id(MaNL) is not None

    def update_quantity(self, MaNL, SoLuongMoi):
        Kho.update_quantity(MaNL, SoLuongMoi)
