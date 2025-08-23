from views.frame.Admin import gui_product, gui_storage, gui_ncc, gui_employees, gui_account, gui_bill
from views.frame.User import gui_product2, gui_storage2, gui_bill2

frame = None

def show_frame(window, new_frame_func):
    global frame
    if frame is not None:
        frame.destroy()
    frame = new_frame_func(window)
    frame.place(x=200, y=0, width=1500, height=1000)

def product(window):
    show_frame(window, gui_product)

def storage(window):
    show_frame(window, gui_storage)

def ncc(window):
    show_frame(window, gui_ncc)

def employees(window):
    show_frame(window, gui_employees)

def account(window):
    show_frame(window, gui_account)

def bill(window):
    show_frame(window, gui_bill)

def bill2(window):
    show_frame(window, gui_bill2)

def storage2(window):
    show_frame(window, gui_storage2)

def product2(window):
    show_frame(window, gui_product2)