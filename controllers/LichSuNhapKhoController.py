# controllers/LichSuNhapKhoController.py
from datetime import datetime
from models.LichSuNhapKhoModel import LichSuNhapKho
from models.KhoModel import Kho

class LichSuNhapKhoController:
    def __init__(self):
        pass

    def nhap_hang(self, MaNL, MaNCC, SoLuongNhap, GiaNhap, Ngay=None):
        # Ngày mặc định hôm nay (yyyy-mm-dd)
        if not Ngay:
            Ngay = datetime.now().strftime("%Y-%m-%d")

        # 1) Ghi lịch sử
        LichSuNhapKho.create(MaNL, MaNCC, SoLuongNhap, GiaNhap, Ngay)

        # 2) Cộng số lượng tồn kho
        Kho.update_quantity(MaNL, SoLuongNhap)

        # 3) (tuỳ chọn) cập nhật giá nhập hiện hành cho Kho nếu muốn đồng bộ
        #    Bỏ comment dòng dưới nếu Ngài muốn cập nhật luôn giá nhập hiển thị
        # Kho.update(MaNL, None, GiaNhap, None, None)  # cần hàm update linh hoạt
        # Do update() hiện tại yêu cầu đủ tham số, nên giữ nguyên giá trong Kho

        return True

    def list_all(self):
        return LichSuNhapKho.get_all()

    def list_by_item(self, MaNL):
        return LichSuNhapKho.get_by_ma_nl(MaNL)
