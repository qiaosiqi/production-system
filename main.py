# 腹痛诊断产生式系统主程序入口
# 本文件负责初始化应用程序并启动主窗口
import tkinter as tk
from gui import AbdomenPainDiagnosticSystem

if __name__ == "__main__":
    # 创建Tkinter根窗口
    root = tk.Tk()
    # 初始化腹痛诊断系统
    app = AbdomenPainDiagnosticSystem(root)
    # 启动主事件循环
    root.mainloop()