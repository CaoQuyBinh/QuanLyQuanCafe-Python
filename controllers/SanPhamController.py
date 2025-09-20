# controllers/SanPhamController.py
from models.SanPhamModel import SanPham

class SanPhamController:
    def __init__(self):
        pass

    # ===== CRUD =====
    def add(self, MaSP, TenSP, LoaiSP, Gia, SoLuong, Anh=None):
        SanPham.create(MaSP, TenSP, LoaiSP, Gia, SoLuong, Anh)

    def load(self):
        return SanPham.get_all()

    def edit(self, MaSP, TenSP, LoaiSP, Gia, SoLuong, Anh=None):
        SanPham.update(MaSP, TenSP, LoaiSP, Gia, SoLuong, Anh)

    def delete(self, MaSP):
        SanPham.delete(MaSP)

    def search(self, TenSP):
        return SanPham.find_by_name(TenSP)

    def exist(self, MaSP):
        return SanPham.find_by_id(MaSP) is not None

    def find_by_id(self, MaSP):
        return SanPham.find_by_id(MaSP)

    def get_categories(self):
        return SanPham.get_categories()

    def get_list_categories(self):
        return self.get_categories()

    def get_by_category(self, loai_sp: str):
        return SanPham.get_by_category(loai_sp)

    def get_products_by_category(self, loai_sp: str):
        return self.get_by_category(loai_sp)

    def find_by_name(self, name: str):
        """
        Trả về 1 SanPham theo tên.
        Ưu tiên trùng khớp chính xác; nếu không có, lấy phần tử đầu tiên trong kết quả LIKE.
        Không có -> trả về None.
        """
        results = SanPham.find_by_name(name) or []
        if not results:
            return None
        # ưu tiên exact match (không phân biệt hoa thường)
        lower = name.strip().lower()
        for sp in results:
            if (sp.TenSP or "").strip().lower() == lower:
                return sp
        return results[0]

    def get_product_by_name(self, name: str):
        return self.find_by_name(name)
