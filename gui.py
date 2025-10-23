# gui.py
import tkinter as tk
from tkinter import messagebox, StringVar
from tkinter.ttk import Combobox
from rules_engine import infer_book
from file_io import write_result_to_file
from knowledge_graph import show_knowledge_graph
from database import get_all_rules, add_rule, delete_rule, update_rule

class BookFinderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("📖 图书查找系统")
        self.root.geometry("600x800")

        # 改为复选框多选模式
        tk.Label(root, text="请选择图书特征（可多选）", font=("Arial", 12)).pack(pady=10)

        # 从数据库中读取所有规则条件关键词
        from database import get_all_rules
        rules = get_all_rules()
        all_features = set()
        for r in rules:
            for cond in r[1].split(','):
                if cond.strip():
                    all_features.add(cond.strip())

        # 存储每个复选框对应的变量
        self.feature_vars = {}

        # 创建一个可以滚动的区域放复选框（防止太多时界面撑开）
        frame_canvas = tk.Frame(root)
        frame_canvas.pack(fill="both", expand=True)
        canvas = tk.Canvas(frame_canvas)
        scrollbar = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 动态生成复选框
        for feature in sorted(all_features):
            var = tk.BooleanVar()
            chk = tk.Checkbutton(scrollable_frame, text=feature, variable=var, anchor="w")
            chk.pack(fill="x", padx=10)
            self.feature_vars[feature] = var

        tk.Button(root, text="🔍 开始推理", command=self.run_inference).pack(pady=5)
        tk.Button(root, text="📁 查看知识图谱", command=show_knowledge_graph).pack(pady=5)
        tk.Button(root, text="🧱 管理规则", command=self.manage_rules).pack(pady=5)

        self.text = tk.Text(root, height=15)
        self.text.pack(pady=10)

    def run_inference(self):
        features = [f for f, v in self.feature_vars.items() if v.get()]
        steps, result = infer_book(features)

        self.text.delete("1.0", tk.END)  # 清空旧内容
        self.text.insert(tk.END, "推理过程如下：\n\n")
        for step in steps:
            self.text.insert(tk.END, f"{step}\n")
        self.text.insert(tk.END, "\n" + result + "\n")

        write_result_to_file(features, result)

    def manage_rules(self):
        win = tk.Toplevel(self.root)
        win.title("规则管理")
        win.geometry("640x420")

        # ===== 输入区 =====
        tk.Label(win, text="条件：").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        cond_entry = tk.Entry(win, width=45, state="readonly")
        cond_entry.grid(row=0, column=1, pady=5)

        tk.Label(win, text="结论：").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        concl_entry = tk.Entry(win, width=45, state="readonly")
        concl_entry.grid(row=1, column=1, pady=5)


        # ===== 操作按钮区 =====
        def refresh_rules():
            rules = get_all_rules()
            listbox.delete(0, tk.END)
            for i, r in enumerate(rules, start=1):
                listbox.insert(tk.END, f"{i} | {r[1]} -> {r[2]}")

        def add():
            popup = tk.Toplevel(win)
            popup.title("➕ 添加新规则")
            popup.geometry("400x200")

            tk.Label(popup, text="条件：").pack(pady=5)
            cond_input = tk.Entry(popup, width=40)
            cond_input.pack(pady=5)

            tk.Label(popup, text="结论：").pack(pady=5)
            concl_input = tk.Entry(popup, width=40)
            concl_input.pack(pady=5)

            def confirm_add():
                cond = cond_input.get().strip()
                concl = concl_input.get().strip()
                if not cond or not concl:
                    messagebox.showwarning("警告", "条件和结论不能为空")
                    return
                add_rule(cond, concl)
                messagebox.showinfo("成功", "规则已添加")
                popup.destroy()
                refresh_rules()

            tk.Button(popup, text="确定添加", command=confirm_add).pack(pady=10)

        def delete():
            sel = listbox.curselection()
            if sel:
                rid = int(listbox.get(sel[0]).split('|')[0])
                delete_rule(rid)
                messagebox.showinfo("成功", "规则已删除")
                refresh_rules()

        def on_select(event):
            sel = listbox.curselection()
            if sel:
                rule_text = listbox.get(sel[0])
                rid, rest = rule_text.split('|', 1)
                cond, concl = rest.split('->')

                # 临时解除 readonly，更新后再恢复
                cond_entry.config(state='normal')
                cond_entry.delete(0, tk.END)
                cond_entry.insert(0, cond.strip())
                cond_entry.config(state='readonly')

                concl_entry.config(state='normal')
                concl_entry.delete(0, tk.END)
                concl_entry.insert(0, concl.strip())
                concl_entry.config(state='readonly')

        def edit():
            sel = listbox.curselection()
            if not sel:
                messagebox.showwarning("警告", "请先选中要编辑的规则")
                return
            rid = int(listbox.get(sel[0]).split('|')[0])
            rule_text = listbox.get(sel[0])
            _, rest = rule_text.split('|', 1)
            old_cond, old_concl = rest.split('->')
            old_cond, old_concl = old_cond.strip(), old_concl.strip()

            popup = tk.Toplevel(win)
            popup.title("💾 修改规则")
            popup.geometry("400x200")

            tk.Label(popup, text="条件：").pack(pady=5)
            cond_input = tk.Entry(popup, width=40)
            cond_input.insert(0, old_cond)
            cond_input.pack(pady=5)

            tk.Label(popup, text="结论：").pack(pady=5)
            concl_input = tk.Entry(popup, width=40)
            concl_input.insert(0, old_concl)
            concl_input.pack(pady=5)

            def confirm_edit():
                new_cond = cond_input.get().strip()
                new_concl = concl_input.get().strip()
                if not new_cond or not new_concl:
                    messagebox.showwarning("警告", "条件和结论不能为空")
                    return
                update_rule(rid, new_cond, new_concl)
                messagebox.showinfo("成功", "规则已更新")
                popup.destroy()
                refresh_rules()

            tk.Button(popup, text="确定修改", command=confirm_edit).pack(pady=10)

        # 三个操作按钮一行排列
        btn_frame = tk.Frame(win)
        btn_frame.grid(row=2, column=0, columnspan=3, pady=10)
        tk.Button(btn_frame, text="➕ 新增规则", width=12, command=add).pack(side="left", padx=5)
        tk.Button(btn_frame, text="💾 保存修改", width=12, command=edit).pack(side="left", padx=5)
        tk.Button(btn_frame, text="🗑 删除选中", width=12, command=delete).pack(side="left", padx=5)

        # ===== 规则列表区 =====
        listbox = tk.Listbox(win, width=85, height=12)
        listbox.grid(row=3, column=0, columnspan=3, pady=10, padx=10)
        listbox.bind('<<ListboxSelect>>', on_select)

        def clear_selection(event):
            # 获取点击坐标对应的索引
            index = listbox.nearest(event.y)
            bbox = listbox.bbox(index)
            if not bbox or event.y > bbox[1] + bbox[3]:  # 若点击在空白处
                listbox.selection_clear(0, tk.END)
                cond_entry.delete(0, tk.END)
                concl_entry.delete(0, tk.END)

        # 绑定鼠标点击事件
        listbox.bind("<Button-1>", clear_selection, add="+")

        refresh_rules()
