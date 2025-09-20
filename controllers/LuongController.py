from models.LuongModel import Luong

class LuongController:
    def __init__(self):
        pass

    def cham_cong(self, maNV):
        return Luong.cham_cong(maNV)

    def tinh_luong_thang(self, maNV, muc_luong_ngay=300000):
        return Luong.tinh_luong_theo_thang(maNV, muc_luong_ngay)

    def get_all(self):
        return Luong.get_all()
