from models.NCCModel import NCC

class NCCController:
    def __init__(self):
        pass

    def add(self, MaNCC, TenNCC, SDT):
        NCC.create(MaNCC, TenNCC, SDT)

    def load(self):
        return NCC.get_all()

    def edit(self, MaNCC, TenNCC, SDT):
        NCC.update(MaNCC, TenNCC, SDT)

    def delete(self, MaNCC):
        NCC.delete(MaNCC)

    def search(self, TenNCC):
        return NCC.find_by_name(TenNCC)

    def exist(selfs, MaNCC):
        return NCC.find_by_id(MaNCC) is not None
