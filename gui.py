# 腹痛诊断系统主界面模块
# 负责实现系统的用户界面，包括症状选择、诊断推理和规则管理功能
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
from db_manager import DatabaseManager
from inference_engine import InferenceEngine

class AbdomenPainDiagnosticSystem:
    """腹痛诊断系统主界面类
    
    实现系统的主要用户界面，包括：
    - 症状选择功能
    - 诊断推理功能
    - 规则管理入口
    - 结果展示和导出功能
    """
    
    def __init__(self, root):
        """初始化主界面
        
        参数:
            root: Tkinter根窗口对象
        """
        self.root = root
        self.root.title("腹痛诊断产生式系统")  # 设置窗口标题
        self.root.geometry("1080x720")  # 设置窗口大小
        
        # 初始化数据库管理器和推理引擎
        self.db_manager = DatabaseManager()  # 用于数据库操作
        self.inference_engine = InferenceEngine(self.db_manager)  # 用于诊断推理
        
        # 创建界面组件
        self.create_widgets()
        
        # 加载所有症状到列表
        self.load_symptoms()
    
    def create_widgets(self):
        """创建界面组件，构建用户交互界面"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建顶部标题
        title_label = ttk.Label(main_frame, text="腹痛症状诊断系统", font=('Arial', 18, 'bold'))
        title_label.pack(pady=10)
        
        # 创建症状选择区域
        symptom_frame = ttk.LabelFrame(main_frame, text="选择症状", padding="10")
        symptom_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 症状列表框
        self.symptom_listbox = tk.Listbox(
            symptom_frame, 
            selectmode=tk.MULTIPLE,  # 允许多选
            font=('Arial', 12), 
            height=10
        )
        scrollbar = ttk.Scrollbar(symptom_frame, orient=tk.VERTICAL, command=self.symptom_listbox.yview)
        self.symptom_listbox.config(yscrollcommand=scrollbar.set)
        
        self.symptom_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 创建按钮区域
        button_frame = ttk.Frame(main_frame, padding="10")
        button_frame.pack(fill=tk.X)
        
        # 诊断按钮
        self.diagnose_button = ttk.Button(button_frame, text="开始诊断", command=self.diagnose)
        self.diagnose_button.pack(side=tk.LEFT, padx=5)
        
        # 清空按钮
        self.clear_button = ttk.Button(button_frame, text="清空选择", command=self.clear_selection)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # 规则管理按钮
        self.rule_manage_button = ttk.Button(button_frame, text="规则管理", command=self.open_rule_management)
        self.rule_manage_button.pack(side=tk.LEFT, padx=5)
        
        # 退出按钮
        self.quit_button = ttk.Button(button_frame, text="退出", command=self.root.quit)
        self.quit_button.pack(side=tk.RIGHT, padx=5)
        
        # 创建结果显示区域
        result_frame = ttk.LabelFrame(main_frame, text="诊断结果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 推理过程文本框
        ttk.Label(result_frame, text="推理过程:", font=('Arial', 12, 'bold')).pack(anchor=tk.W)
        self.process_text = tk.Text(result_frame, height=5, font=('Arial', 10), state=tk.DISABLED)
        self.process_text.pack(fill=tk.X, pady=5)
        
        # 诊断结果文本框
        ttk.Label(result_frame, text="可能的诊断:", font=('Arial', 12, 'bold')).pack(anchor=tk.W)
        self.result_text = tk.Text(result_frame, height=8, font=('Arial', 10), state=tk.DISABLED)
        self.result_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 结果文件路径标签
        self.file_path_label = ttk.Label(result_frame, text="", foreground="blue", cursor="hand2")
        self.file_path_label.pack(anchor=tk.W, pady=5)
        self.file_path_label.bind("<Button-1>", self.open_result_file)
    
    def load_symptoms(self):
        """加载所有症状到列表框
        
        从数据库获取所有症状信息，然后显示在界面的列表框中
        格式为：症状ID: 症状名称
        """
        symptoms = self.db_manager.get_all_symptoms()
        self.symptom_listbox.delete(0, tk.END)  # 清空当前列表内容
        for symptom_id, name in symptoms:
            self.symptom_listbox.insert(tk.END, f"{symptom_id}: {name}")  # 将症状按ID+名称格式添加到列表
    
    def diagnose(self):
        """执行诊断推理
        
        1. 获取用户在列表框中选择的症状
        2. 调用推理引擎进行诊断
        3. 在界面上显示诊断结果和推理过程
        4. 将结果保存到文件中
        """
        # 获取用户选择的症状索引
        selected_indices = self.symptom_listbox.curselection()
        selected_symptoms = []
        
        for index in selected_indices:
            symptom_str = self.symptom_listbox.get(index)  # 获取选中的症状字符串
            symptom_id = symptom_str.split(':')[0]  # 从字符串中提取症状ID
            selected_symptoms.append(symptom_id)  # 添加到选中列表
            selected_symptoms.append(symptom_id)  # 注意：这里重复添加了两次症状ID，可能是为了满足推理引擎的特定要求
        
        # 验证用户是否选择了症状
        if not selected_symptoms:
            messagebox.showwarning("警告", "请至少选择一个症状！")
            return
        
        # 调用推理引擎进行诊断
        results, inference_process = self.inference_engine.inference(selected_symptoms)
        
        # 在界面上显示结果
        self.display_results(results, inference_process, selected_symptoms)
        
        # 将结果保存到文件
        self.save_results_to_file(results, inference_process, selected_symptoms)
    
    def display_results(self, results, inference_process, selected_symptoms):
        """在界面上显示诊断结果
        
        参数：
            results: 诊断结果列表，包含可能的疾病信息
            inference_process: 推理过程的文本描述列表
            selected_symptoms: 用户选择的症状ID列表
        """
        # 先启用文本框以便编辑
        self.process_text.config(state=tk.NORMAL)
        self.result_text.config(state=tk.NORMAL)
        
        # 清空现有内容
        self.process_text.delete(1.0, tk.END)
        self.result_text.delete(1.0, tk.END)
        
        # 显示用户选择的症状
        self.result_text.insert(tk.END, "您选择的症状：\n")
        for symptom_id in selected_symptoms:
            symptom_name = self.db_manager.get_symptom_name(symptom_id)  # 根据ID获取症状名称
            self.result_text.insert(tk.END, f"- {symptom_name}\n")
        self.result_text.insert(tk.END, "\n")
        
        # 显示推理过程
        if inference_process:
            self.process_text.insert(tk.END, "推理过程：\n")
            for i, process in enumerate(inference_process, 1):
                self.process_text.insert(tk.END, f"{i}. {process}\n")
        else:
            self.process_text.insert(tk.END, "未找到匹配的规则\n")
        
        # 显示诊断结果
        if results:
            self.result_text.insert(tk.END, "可能的诊断结果：\n")
            for i, (diagnostic_name, diagnostic_id, description) in enumerate(results, 1):
                self.result_text.insert(tk.END, f"{i}. {diagnostic_name}\n")
        else:
            self.result_text.insert(tk.END, "根据当前症状无法做出明确诊断，请咨询医生\n")
        
        # 重新禁用文本框，防止用户误编辑
        self.process_text.config(state=tk.DISABLED)
        self.result_text.config(state=tk.DISABLED)
    
    def save_results_to_file(self, results, inference_process, selected_symptoms):
        """将诊断结果保存到文件
        
        参数：
            results: 诊断结果列表
            inference_process: 推理过程的文本描述列表
            selected_symptoms: 用户选择的症状ID列表
        """
        # 定义结果文件的路径，使用绝对路径便于用户查找
        result_file = os.path.abspath("result.out")
        
        try:
            # 以写入模式打开文件，使用UTF-8编码确保中文显示正常
            with open(result_file, 'w', encoding='utf-8') as f:
                f.write("腹痛诊断系统结果\n")
                f.write("=" * 30 + "\n\n")
                
                # 写入选中的症状信息
                f.write("您选择的症状：\n")
                for symptom_id in selected_symptoms:
                    symptom_name = self.db_manager.get_symptom_name(symptom_id)
                    f.write(f"- {symptom_name}\n")
                f.write("\n")
                
                # 写入推理过程
                f.write("推理过程：\n")
                if inference_process:
                    for i, process in enumerate(inference_process, 1):
                        f.write(f"{i}. {process}\n")
                else:
                    f.write("未找到匹配的规则\n")
                f.write("\n")
                
                # 写入诊断结果
                f.write("可能的诊断结果：\n")
                if results:
                    for i, (diagnostic_name, diagnostic_id, description) in enumerate(results, 1):
                        f.write(f"{i}. {diagnostic_name}\n")
                else:
                    f.write("根据当前症状无法做出明确诊断，请咨询医生\n")
            
            # 显示文件路径
            self.file_path_label.config(text=f"结果已保存至: {result_file}")
        except Exception as e:
            messagebox.showerror("错误", f"保存结果失败: {e}")
            self.file_path_label.config(text="")
    
    def clear_selection(self):
        """清空所有用户选择和结果显示
        
        1. 清空症状列表框的选择
        2. 清空推理过程和诊断结果的文本框
        3. 清空结果文件路径标签
        """
        self.symptom_listbox.selection_clear(0, tk.END)  # 清空症状选择
        
        # 清空推理过程文本框
        self.process_text.config(state=tk.NORMAL)
        self.process_text.delete(1.0, tk.END)
        self.process_text.config(state=tk.DISABLED)
        
        # 清空诊断结果文本框
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)
        
        self.file_path_label.config(text="")  # 清空文件路径标签
    
    def open_rule_management(self):
        """打开规则管理窗口
        
        创建并显示规则管理窗口，用户可以在该窗口中添加、编辑和删除诊断规则
        """
        RuleManagementWindow(self.root, self.db_manager)
    
    def open_result_file(self, event):
        """打开诊断结果文件
        
        当用户点击结果文件路径标签时，使用系统默认程序打开结果文件
        
        参数：
            event: 鼠标点击事件对象
        """
        # 从标签文本中提取文件路径
        file_path = self.file_path_label.cget("text").replace("结果已保存至: ", "")
        
        # 检查文件路径是否存在且有效
        if file_path and os.path.exists(file_path):
            os.startfile(file_path)  # 使用系统默认程序打开文件

# 规则管理窗口类
class RuleManagementWindow:
    """规则管理窗口类，用于管理诊断规则的增删改查"""
    
    def __init__(self, parent, db_manager):
        """初始化规则管理窗口
        
        参数：
            parent: 父窗口对象
            db_manager: 数据库管理器对象，用于与数据库交互
        """
        self.parent = parent
        self.db_manager = db_manager
        
        # 创建一个顶级窗口（Toplevel）作为规则管理窗口
        self.window = tk.Toplevel(parent)
        self.window.title("规则管理")
        self.window.geometry("700x500")
        
        # 创建窗口内的所有界面组件
        self.create_widgets()
        
        # 从数据库加载现有规则到列表中
        self.load_rules()
    
    def create_widgets(self):
        """创建规则管理窗口的所有界面组件
        
        包括：
        - 主框架
        - 规则列表区域
        - 操作按钮区域
        """
        # 创建主框架，设置内边距
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)  # 填充整个窗口并允许扩展
        
        # 创建规则列表的带标签框架
        rule_frame = ttk.LabelFrame(main_frame, text="规则列表", padding="10")
        rule_frame.pack(fill=tk.BOTH, expand=True, pady=10)  # 垂直方向有10像素的外边距
        
        # 创建规则列表框，设置字体和高度
        self.rule_listbox = tk.Listbox(rule_frame, font=('Arial', 10), height=15)
        
        # 创建垂直滚动条，与列表框关联
        scrollbar = ttk.Scrollbar(rule_frame, orient=tk.VERTICAL, command=self.rule_listbox.yview)
        self.rule_listbox.config(yscrollcommand=scrollbar.set)  # 设置列表框的滚动命令
        
        # 放置列表框和滚动条
        self.rule_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # 列表框填充剩余空间
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # 滚动条垂直填充
        
        # 创建按钮操作区域
        button_frame = ttk.Frame(main_frame, padding="10")
        button_frame.pack(fill=tk.X)  # 水平方向填充
        
        # 添加规则按钮，点击时调用add_rule方法
        self.add_button = ttk.Button(button_frame, text="添加规则", command=self.add_rule)
        self.add_button.pack(side=tk.LEFT, padx=5)  # 左侧放置，水平间距5像素
        
        # 修改规则按钮
        self.edit_button = ttk.Button(button_frame, text="修改规则", command=self.edit_rule)
        self.edit_button.pack(side=tk.LEFT, padx=5)
        
        # 删除规则按钮
        self.delete_button = ttk.Button(button_frame, text="删除规则", command=self.delete_rule)
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        # 关闭按钮
        self.close_button = ttk.Button(button_frame, text="关闭", command=self.window.destroy)
        self.close_button.pack(side=tk.RIGHT, padx=5)
    
    def load_rules(self):
        """加载规则列表"""
        rules = self.db_manager.get_all_rules()
        self.rule_listbox.delete(0, tk.END)
        for rule in rules:
            rule_id, premises_str, conclusion, description = rule
            self.rule_listbox.insert(tk.END, f"ID: {rule_id} | {description}")
    
    def add_rule(self):
        """添加规则"""
        # 获取所有症状和诊断结果
        symptoms = self.db_manager.get_all_symptoms()
        diagnostics = self.db_manager.get_all_diagnostics()
        
        # 创建添加规则窗口
        add_window = tk.Toplevel(self.window)
        add_window.title("添加规则")
        add_window.geometry("500x400")
        
        # 创建症状选择区域
        symptom_frame = ttk.LabelFrame(add_window, text="选择前提条件(症状)", padding="10")
        symptom_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        symptom_listbox = tk.Listbox(symptom_frame, selectmode=tk.MULTIPLE, height=10)
        scrollbar = ttk.Scrollbar(symptom_frame, orient=tk.VERTICAL, command=symptom_listbox.yview)
        symptom_listbox.config(yscrollcommand=scrollbar.set)
        
        for symptom_id, name in symptoms:
            symptom_listbox.insert(tk.END, f"{symptom_id}: {name}")
        
        symptom_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 创建结论选择区域
        conclusion_frame = ttk.LabelFrame(add_window, text="选择结论(诊断)", padding="10")
        conclusion_frame.pack(fill=tk.X, pady=5)
        
        conclusion_var = tk.StringVar()
        conclusion_combo = ttk.Combobox(conclusion_frame, textvariable=conclusion_var)
        conclusion_combo['values'] = [f"{d[0]}: {d[1]}" for d in diagnostics]
        conclusion_combo.pack(fill=tk.X)
        
        # 创建规则描述区域
        desc_frame = ttk.LabelFrame(add_window, text="规则描述", padding="10")
        desc_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        desc_text = tk.Text(desc_frame, height=3)
        desc_text.pack(fill=tk.BOTH, expand=True)
        
        # 创建按钮区域
        button_frame = ttk.Frame(add_window, padding="10")
        button_frame.pack(fill=tk.X)
        
        def save_rule():
            # 获取选中的症状
            selected_indices = symptom_listbox.curselection()
            selected_symptoms = []
            for index in selected_indices:
                symptom_str = symptom_listbox.get(index)
                symptom_id = symptom_str.split(':')[0]
                selected_symptoms.append(symptom_id)
            
            if not selected_symptoms:
                messagebox.showwarning("警告", "请至少选择一个前提条件！")
                return
            
            # 获取结论
            conclusion_str = conclusion_var.get()
            if not conclusion_str:
                messagebox.showwarning("警告", "请选择一个结论！")
                return
            conclusion_id = conclusion_str.split(':')[0]
            
            # 获取规则描述
            description = desc_text.get(1.0, tk.END).strip()
            if not description:
                messagebox.showwarning("警告", "请输入规则描述！")
                return
            
            # 保存规则
            premises_str = ','.join(selected_symptoms)
            if self.db_manager.add_rule(premises_str, conclusion_id, description):
                messagebox.showinfo("成功", "规则添加成功！")
                add_window.destroy()
                self.load_rules()
            else:
                messagebox.showerror("错误", "规则添加失败！")
        
        save_button = ttk.Button(button_frame, text="保存", command=save_rule)
        save_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = ttk.Button(button_frame, text="取消", command=add_window.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)
    
    def edit_rule(self):
        """修改规则"""
        # 获取选中的规则
        selected_indices = self.rule_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("警告", "请选择一个规则进行修改！")
            return
        
        # 获取规则ID
        selected_rule_str = self.rule_listbox.get(selected_indices[0])
        rule_id = int(selected_rule_str.split('|')[0].split(':')[1].strip())
        
        # 获取规则详情
        rules = self.db_manager.get_all_rules()
        selected_rule = None
        for rule in rules:
            if rule[0] == rule_id:
                selected_rule = rule
                break
        
        if not selected_rule:
            messagebox.showerror("错误", "未找到选中的规则！")
            return
        
        rule_id, premises_str, conclusion_id, description = selected_rule
        selected_symptoms = premises_str.split(',')
        
        # 获取所有症状和诊断结果
        symptoms = self.db_manager.get_all_symptoms()
        diagnostics = self.db_manager.get_all_diagnostics()
        
        # 创建修改规则窗口
        edit_window = tk.Toplevel(self.window)
        edit_window.title("修改规则")
        edit_window.geometry("500x400")
        
        # 创建症状选择区域
        symptom_frame = ttk.LabelFrame(edit_window, text="选择前提条件(症状)", padding="10")
        symptom_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        symptom_listbox = tk.Listbox(symptom_frame, selectmode=tk.MULTIPLE, height=10)
        scrollbar = ttk.Scrollbar(symptom_frame, orient=tk.VERTICAL, command=symptom_listbox.yview)
        symptom_listbox.config(yscrollcommand=scrollbar.set)
        
        for symptom_id, name in symptoms:
            symptom_listbox.insert(tk.END, f"{symptom_id}: {name}")
            # 选中已有的症状
            if symptom_id in selected_symptoms:
                symptom_listbox.select_set(symptom_listbox.size() - 1)
        
        symptom_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 创建结论选择区域
        conclusion_frame = ttk.LabelFrame(edit_window, text="选择结论(诊断)", padding="10")
        conclusion_frame.pack(fill=tk.X, pady=5)
        
        conclusion_var = tk.StringVar()
        conclusion_combo = ttk.Combobox(conclusion_frame, textvariable=conclusion_var)
        conclusion_combo['values'] = [f"{d[0]}: {d[1]}" for d in diagnostics]
        
        # 设置当前结论
        for d in diagnostics:
            if d[0] == conclusion_id:
                conclusion_var.set(f"{d[0]}: {d[1]}")
                break
        
        conclusion_combo.pack(fill=tk.X)
        
        # 创建规则描述区域
        desc_frame = ttk.LabelFrame(edit_window, text="规则描述", padding="10")
        desc_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        desc_text = tk.Text(desc_frame, height=3)
        desc_text.insert(tk.END, description)
        desc_text.pack(fill=tk.BOTH, expand=True)
        
        # 创建按钮区域
        button_frame = ttk.Frame(edit_window, padding="10")
        button_frame.pack(fill=tk.X)
        
        def update_rule():
            # 获取选中的症状
            new_selected_indices = symptom_listbox.curselection()
            new_selected_symptoms = []
            for index in new_selected_indices:
                symptom_str = symptom_listbox.get(index)
                symptom_id = symptom_str.split(':')[0]
                new_selected_symptoms.append(symptom_id)
            
            if not new_selected_symptoms:
                messagebox.showwarning("警告", "请至少选择一个前提条件！")
                return
            
            # 获取结论
            conclusion_str = conclusion_var.get()
            if not conclusion_str:
                messagebox.showwarning("警告", "请选择一个结论！")
                return
            new_conclusion_id = conclusion_str.split(':')[0]
            
            # 获取规则描述
            new_description = desc_text.get(1.0, tk.END).strip()
            if not new_description:
                messagebox.showwarning("警告", "请输入规则描述！")
                return
            
            # 更新规则
            new_premises_str = ','.join(new_selected_symptoms)
            if self.db_manager.update_rule(rule_id, new_premises_str, new_conclusion_id, new_description):
                messagebox.showinfo("成功", "规则修改成功！")
                edit_window.destroy()
                self.load_rules()
            else:
                messagebox.showerror("错误", "规则修改失败！")
        
        save_button = ttk.Button(button_frame, text="保存", command=update_rule)
        save_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = ttk.Button(button_frame, text="取消", command=edit_window.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)
    
    def delete_rule(self):
        """删除规则"""
        # 获取选中的规则
        selected_indices = self.rule_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("警告", "请选择一个规则进行删除！")
            return
        
        # 获取规则ID
        selected_rule_str = self.rule_listbox.get(selected_indices[0])
        rule_id = int(selected_rule_str.split('|')[0].split(':')[1].strip())
        
        # 确认删除
        if messagebox.askyesno("确认删除", "确定要删除选中的规则吗？"):
            if self.db_manager.delete_rule(rule_id):
                messagebox.showinfo("成功", "规则删除成功！")
                self.load_rules()
            else:
                messagebox.showerror("错误", "规则删除失败！")