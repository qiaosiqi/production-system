# 腹痛诊断产生式系统主程序入口
import tkinter as tk
from gui import AbdomenPainDiagnosticSystem

if __name__ == "__main__":
    root = tk.Tk()
    app = AbdomenPainDiagnosticSystem(root)
    root.mainloop()