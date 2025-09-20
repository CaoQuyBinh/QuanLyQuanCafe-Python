# database/db_tables.py
import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("QLCafe.db")
    cur = conn.cursor()

    cur.execute("PRAGMA foreign_keys = ON;")

    # Bảng tài khoản
    cur.execute("""
    CREATE TABLE IF NOT EXISTS TaiKhoan (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        HoTen TEXT NOT NULL,
        TenDangNhap TEXT NOT NULL UNIQUE,
        MatKhau TEXT NOT NULL,
        Email TEXT NOT NULL,
        Role TEXT DEFAULT 'Nhân viên'
    )
    """)

    cur.execute("""
       CREATE TABLE IF NOT EXISTS NhanVien (
           MaNV INTEGER PRIMARY KEY AUTOINCREMENT,
           Ten TEXT NOT NULL,
           ChucVu TEXT NOT NULL,
           NgaySinh TEXT NOT NULL,
           Email TEXT NOT NULL
       )
       """)

    cur.execute("""
           CREATE TABLE IF NOT EXISTS NhanVien (
               MaNV INTEGER PRIMARY KEY AUTOINCREMENT,
               Ten TEXT NOT NULL,
               ChucVu TEXT NOT NULL,
               NgaySinh TEXT NOT NULL,
               Email TEXT NOT NULL
           )
           """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Luong (
            MaNV INTEGER,
            Ngay TEXT NOT NULL,
            NgayCong INTEGER NOT NULL,
            VAT REAL,
            TongLuong REAL,
            PRIMARY KEY(MaNV),
            FOREIGN KEY(MaNV) REFERENCES NhanVien(MaNV)
        )
    """)

    # Bảng sản phẩm
    cur.execute("""
    CREATE TABLE IF NOT EXISTS SanPham (
        MaSP TEXT PRIMARY KEY,
        TenSP TEXT NOT NULL,
        LoaiSP TEXT,
        Gia REAL NOT NULL,
        SoLuong INTEGER DEFAULT 0,
        Anh TEXT
    )
    """)

    # Bảng NCC
    cur.execute("""
    CREATE TABLE IF NOT EXISTS NCC (
        MaNCC TEXT PRIMARY KEY,
        TenNCC TEXT NOT NULL,
        SDT TEXT
    )
    """)

    # Bảng Kho (nguyên liệu)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Kho (
        MaNL TEXT PRIMARY KEY,
        TenNL TEXT NOT NULL,
        GiaNhap REAL NOT NULL,
        SoLuong INTEGER DEFAULT 0,
        MaNCC TEXT,
        FOREIGN KEY (MaNCC) REFERENCES NCC(MaNCC)
    )
    """)

    #Bảng công thức
    cur.execute("""
        CREATE TABLE IF NOT EXISTS CongThuc (
            MaSP TEXT NOT NULL,
            MaNL TEXT NOT NULL,
            SoLuongCan REAL NOT NULL,
            GhiChu TEXT,
            PRIMARY KEY (MaSP, MaNL),
            FOREIGN KEY (MaSP) REFERENCES SanPham(MaSP) ON DELETE CASCADE,
            FOREIGN KEY (MaNL) REFERENCES Kho(MaNL) ON DELETE CASCADE
        )
        """)

    # Bảng hoá đơn
    cur.execute("""
    CREATE TABLE IF NOT EXISTS HoaDon (
        MaHD TEXT PRIMARY KEY,
        TenKH TEXT,
        VAT REAL DEFAULT 0,
        Ngay TEXT NOT NULL,
        Tong REAL DEFAULT 0
    )
    """)

    # Chi tiết hoá đơn
    cur.execute("""
    CREATE TABLE IF NOT EXISTS ChiTietHoaDon (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        MaHD TEXT NOT NULL,
        MaSP TEXT NOT NULL,
        TenSP TEXT,
        SoLuong INTEGER NOT NULL,
        Gia REAL NOT NULL,
        VAT REAL DEFAULT 0,
        Ngay TEXT NOT NULL,
        Tong REAL DEFAULT 0,
        FOREIGN KEY (MaHD) REFERENCES HoaDon(MaHD),
        FOREIGN KEY (MaSP) REFERENCES SanPham(MaSP)
    )
    """)

    # Lịch sử nhập kho nguyên liệu (MỚI)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS LichSuNhapKho (
        MaNhap INTEGER PRIMARY KEY AUTOINCREMENT,
        MaNL TEXT NOT NULL,
        MaNCC TEXT,
        SoLuong INTEGER NOT NULL,
        GiaNhap REAL NOT NULL,
        Ngay TEXT NOT NULL,
        FOREIGN KEY (MaNL) REFERENCES Kho(MaNL),
        FOREIGN KEY (MaNCC) REFERENCES NCC(MaNCC)
    )
    """)

    conn.commit()
    conn.close()
    print("Kết nối thành công database")

init_db()
