# main.py
from database import init_db
from gui import BookFinderGUI
import tkinter as tk


if __name__ == "__main__":
    init_db()  # 初始化数据库
    root = tk.Tk()
    app = BookFinderGUI(root)
    root.mainloop()
