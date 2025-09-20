# controllers/HoaDonController.py
from models.HoaDonModel import HoaDon

class HoaDonController:
    def __init__(self):
        pass

    # ----- Load / List -----
    def load(self):
        """Trả về list[HoaDon]."""
        return HoaDon.get_all()

    # Alias để tương thích Bills.py
    def get_bills(self):
        """Alias của load()."""
        return self.load()

    # ----- Search -----
    def search(self, keyword: str):
        return HoaDon.search(keyword)

    # ----- Create -----
    def add(self, MaHD, TenKH, VAT, Ngay, Tong):
        """Thêm hoá đơn với VAT truyền vào (nếu có)."""
        HoaDon.create(MaHD, TenKH, VAT, Ngay, Tong)

    # Alias cho Main.py (UI không truyền VAT) -> mặc định VAT = 0
    def add_bill(self, MaHD, TenKH, Ngay, Tong, VAT: float = 0.0):
        """Thêm hoá đơn, mặc định VAT = 0 để hợp với UI hiện tại."""
        HoaDon.create(MaHD, TenKH, VAT, Ngay, Tong)

    # ----- Read one -----
    def find_by_id(self, MaHD):
        return HoaDon.find_by_id(MaHD)

    # ----- Delete -----
    def delete(self, MaHD):
        HoaDon.delete(MaHD)
