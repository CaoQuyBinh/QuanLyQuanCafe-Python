import subprocess
import sys
import os

def home(window=None):
    if window:
        window.destroy()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    home_path = os.path.join(current_dir, "..", "views", "home.py")
    subprocess.run([sys.executable, home_path])

def home2(window=None):
    if window:
        window.destroy()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    home_path = os.path.join(current_dir, "..", "views", "home2.py")
    subprocess.run([sys.executable, home_path])

def logout(window=None):
    if window:
        window.destroy()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    login_path = os.path.join(current_dir, "..", "views", "other_views", "login2.py")
    subprocess.run([sys.executable, login_path])

def size(buttons):
    num_buttons = len(buttons)
    gap_button = 450 // (num_buttons + 1) + 5
    for i, button in enumerate(buttons):
        button.place(x=20, y=(i + 2.5) * gap_button, width=150, height=40)

def size2(buttons):
    num_buttons = len(buttons)
    gap_button = 350 // (num_buttons + 1)
    for i, button in enumerate(buttons):
        button.place(x=20, y=(i+2.5) * gap_button, width=150, height=40)

