from database.db_connect import fetch_query, execute_query

class CongThuc:
    def __init__(self, MaSP, MaNL, SoLuongCan, GhiChu=None):
        self.MaSP = MaSP
        self.MaNL = MaNL
        self.SoLuongCan = int(SoLuongCan)
        self.GhiChu = GhiChu

    @staticmethod
    def _row_to_obj(row):
        return CongThuc(row[0], row[1], row[2])

    @staticmethod
    def create(MaSP, MaNL, SoLuongCan, GhiChu=None):
        execute_query(
            "INSERT INTO CongThuc (MaSP, MaNL, SoLuongCan, GhiChu) VALUES (?, ?, ?, ?)",
            (MaSP, MaNL, SoLuongCan, GhiChu)
        )

    @staticmethod
    def get_by_sp(MaSP):
        result = fetch_query(
            "SELECT MaNL, SoLuongCan FROM CongThuc WHERE MaSP = ?",
            (MaSP,)
        )
        return [(row[0], row[1]) for row in result] if result else []

