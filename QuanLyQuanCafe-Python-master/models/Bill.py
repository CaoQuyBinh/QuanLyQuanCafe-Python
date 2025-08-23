class Bill:
    def __init__(self, bid, date, eName, cName, total):
        self.bID = bid
        self.Date = date
        self.eName = eName
        self.cName= cName
        self.Total= total

class BillDetail:
    def __init__(self, pid, pName, bdQuantity, price):
        self.pID = pid
        self.pName = pName
        self.bdQuantity = bdQuantity
        self.Price = price
        self.total = price * bdQuantity
