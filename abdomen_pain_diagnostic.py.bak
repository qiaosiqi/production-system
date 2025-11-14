# 腹痛诊断产生式系统
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

# 数据库初始化和操作类
class DatabaseManager:
    def __init__(self, db_name='abdomen_pain.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.init_db()
    
    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
    
    def disconnect(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
    
    def init_db(self):
        """初始化数据库，创建症状和规则表"""
        self.connect()
        
        # 创建症状表
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS symptoms (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
        ''')
        
        # 创建规则表 (知识图谱形式，使用前提条件列表和结论)
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS rules (
            id INTEGER PRIMARY KEY,
            premises TEXT NOT NULL,  -- 前提条件ID列表，用逗号分隔
            conclusion TEXT NOT NULL,  -- 结论ID
            description TEXT  -- 规则描述
        )
        ''')
        
        # 创建诊断结果表
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS diagnostics (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
        ''')
        
        self.conn.commit()
        self.disconnect()
        
        # 插入初始数据
        self.insert_initial_data()
    
    def insert_initial_data(self):
        """插入初始的症状、规则和诊断结果数据"""
        self.connect()
        
        # 插入症状数据
        symptoms_data = [
            (1, '上腹痛', '位于肚脐以上的腹部疼痛'),
            (2, '下腹痛', '位于肚脐以下的腹部疼痛'),
            (3, '左侧腹痛', '位于腹部左侧的疼痛'),
            (4, '右侧腹痛', '位于腹部右侧的疼痛'),
            (5, '全腹痛', '整个腹部都有疼痛感'),
            (6, '持续性疼痛', '疼痛持续存在，没有明显缓解'),
            (7, '阵发性疼痛', '疼痛一阵一阵地发作'),
            (8, '恶心', '有想要呕吐的感觉'),
            (9, '呕吐', '胃内容物从口中吐出'),
            (10, '腹泻', '排便次数增多，大便稀薄'),
            (11, '便秘', '排便困难或次数减少'),
            (12, '发热', '体温升高，超过正常范围'),
            (13, '黄疸', '皮肤和巩膜发黄'),
            (14, '血尿', '尿液中含有血液'),
            (15, '便血', '大便中含有血液'),
            (16, '暴饮暴食史', '近期有大量进食的情况'),
            (17, '饮酒史', '近期有饮酒的情况'),
            (18, '油腻食物史', '近期有进食油腻食物的情况'),
            (19, '月经异常', '女性月经周期或量的异常'),
            (20, '腹部外伤史', '近期腹部受到过外力撞击')
        ]
        
        for symptom in symptoms_data:
            try:
                self.cursor.execute('INSERT INTO symptoms VALUES (?, ?, ?)', symptom)
            except sqlite3.IntegrityError:
                pass  # 忽略已存在的数据
        
        # 插入诊断结果数据
        diagnostics_data = [
            (101, '胃炎', '胃黏膜的炎症，常见症状包括上腹痛、恶心、呕吐等'),
            (102, '胃溃疡', '胃黏膜的溃疡性病变，常表现为周期性上腹痛'),
            (103, '胆囊炎', '胆囊的炎症，常由胆结石引起，表现为右上腹痛、发热等'),
            (104, '阑尾炎', '阑尾的炎症，典型症状为转移性右下腹痛'),
            (105, '胰腺炎', '胰腺的炎症，常由暴饮暴食或饮酒引起，表现为上腹痛、恶心、呕吐等'),
            (106, '肠梗阻', '肠道内容物通过障碍，表现为腹痛、呕吐、停止排气排便等'),
            (107, '尿路结石', '泌尿系统的结石，常表现为侧腹痛、血尿等'),
            (108, '急性胃肠炎', '胃肠道的急性炎症，表现为腹痛、腹泻、恶心、呕吐等'),
            (109, '妇科炎症', '女性生殖系统的炎症，表现为下腹痛、月经异常等'),
            (110, '腹膜炎', '腹膜的炎症，表现为全腹痛、发热等')
        ]
        
        for diagnostic in diagnostics_data:
            try:
                self.cursor.execute('INSERT INTO diagnostics VALUES (?, ?, ?)', diagnostic)
            except sqlite3.IntegrityError:
                pass  # 忽略已存在的数据
        
        # 插入规则数据 (知识图谱形式)
        rules_data = [
            ('1,6,8,9,16,17', '105', '上腹痛+持续性疼痛+恶心+呕吐+暴饮暴食史+饮酒史->胰腺炎'),
            ('1,7,8,9', '101', '上腹痛+阵发性疼痛+恶心+呕吐->胃炎'),
            ('1,6,8,9', '102', '上腹痛+持续性疼痛+恶心+呕吐->胃溃疡'),
            ('4,6,12,18', '103', '右侧腹痛+持续性疼痛+发热+油腻食物史->胆囊炎'),
            ('4,7,12', '104', '右侧腹痛+阵发性疼痛+发热->阑尾炎'),
            ('5,6,9,11', '106', '全腹痛+持续性疼痛+呕吐+便秘->肠梗阻'),
            ('3,7,14', '107', '左侧腹痛+阵发性疼痛+血尿->尿路结石'),
            ('2,7,10,12', '108', '下腹痛+阵发性疼痛+腹泻+发热->急性胃肠炎'),
            ('2,6,19', '109', '下腹痛+持续性疼痛+月经异常->妇科炎症'),
            ('5,6,12', '110', '全腹痛+持续性疼痛+发热->腹膜炎'),
            ('4,7,12,20', '104', '右侧腹痛+阵发性疼痛+发热+腹部外伤史->阑尾炎'),
            ('1,6,8,9,18', '103', '上腹痛+持续性疼痛+恶心+呕吐+油腻食物史->胆囊炎')
        ]
        
        for rule in rules_data:
            try:
                self.cursor.execute('INSERT INTO rules (premises, conclusion, description) VALUES (?, ?, ?)', rule)
            except sqlite3.IntegrityError:
                pass  # 忽略已存在的数据
        
        self.conn.commit()
        self.disconnect()
    
    def get_all_symptoms(self):
        """获取所有症状"""
        self.connect()
        self.cursor.execute('SELECT id, name FROM symptoms ORDER BY id')
        symptoms = self.cursor.fetchall()
        self.disconnect()
        return symptoms
    
    def get_all_rules(self):
        """获取所有规则"""
        self.connect()
        self.cursor.execute('SELECT id, premises, conclusion, description FROM rules ORDER BY id')
        rules = self.cursor.fetchall()
        self.disconnect()
        return rules
    
    def get_all_diagnostics(self):
        """获取所有诊断结果"""
        self.connect()
        self.cursor.execute('SELECT id, name FROM diagnostics ORDER BY id')
        diagnostics = self.cursor.fetchall()
        self.disconnect()
        return diagnostics
    
    def add_rule(self, premises, conclusion, description):
        """添加新规则"""
        self.connect()
        try:
            self.cursor.execute('INSERT INTO rules (premises, conclusion, description) VALUES (?, ?, ?)', 
                               (premises, conclusion, description))
            self.conn.commit()
            self.disconnect()
            return True
        except Exception as e:
            print(f"添加规则失败: {e}")
            self.disconnect()
            return False
    
    def update_rule(self, rule_id, premises, conclusion, description):
        """更新规则"""
        self.connect()
        try:
            self.cursor.execute('''
            UPDATE rules SET premises = ?, conclusion = ?, description = ? WHERE id = ?
            ''', (premises, conclusion, description, rule_id))
            self.conn.commit()
            self.disconnect()
            return True
        except Exception as e:
            print(f"更新规则失败: {e}")
            self.disconnect()
            return False
    
    def delete_rule(self, rule_id):
        """删除规则"""
        self.connect()
        try:
            self.cursor.execute('DELETE FROM rules WHERE id = ?', (rule_id,))
            self.conn.commit()
            self.disconnect()
            return True
        except Exception as e:
            print(f"删除规则失败: {e}")
            self.disconnect()
            return False
    
    def get_diagnostic_name(self, diagnostic_id):
        """根据诊断ID获取诊断名称"""
        self.connect()
        self.cursor.execute('SELECT name FROM diagnostics WHERE id = ?', (diagnostic_id,))
        result = self.cursor.fetchone()
        self.disconnect()
        return result[0] if result else '未知诊断'
    
    def get_symptom_name(self, symptom_id):
        """根据症状ID获取症状名称"""
        self.connect()
        self.cursor.execute('SELECT name FROM symptoms WHERE id = ?', (symptom_id,))
        result = self.cursor.fetchone()
        self.disconnect()
        return result[0] if result else '未知症状'

# 推理引擎类
class InferenceEngine:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def inference(self, selected_symptoms):
        """根据用户选择的症状进行推理"""
        # 获取所有规则
        rules = self.db_manager.get_all_rules()
        results = []
        inference_process = []
        
        # 将选中的症状转换为集合，便于检查
        selected_set = set(selected_symptoms)
        
        # 应用规则进行推理
        for rule in rules:
            rule_id, premises_str, conclusion, description = rule
            premises = premises_str.split(',')
            
            # 检查是否满足所有前提条件
            if set(premises).issubset(selected_set):
                # 获取诊断结果名称
                diagnostic_name = self.db_manager.get_diagnostic_name(conclusion)
                results.append((diagnostic_name, conclusion, description))
                inference_process.append(description)
        
        return results, inference_process

# 主界面类
class AbdomenPainDiagnosticSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("腹痛诊断产生式系统")
        self.root.geometry("1080x720")
        
        # 初始化数据库
        self.db_manager = DatabaseManager()
        self.inference_engine = InferenceEngine(self.db_manager)
        
        # 创建界面组件
        self.create_widgets()
        
        # 初始化症状列表
        self.load_symptoms()
        
    def create_widgets(self):
        """创建界面组件"""
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
        self.symptom_listbox = tk.Listbox(symptom_frame, selectmode=tk.MULTIPLE, font=('Arial', 12), height=10)
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
        """加载症状列表"""
        symptoms = self.db_manager.get_all_symptoms()
        self.symptom_listbox.delete(0, tk.END)
        for symptom_id, name in symptoms:
            self.symptom_listbox.insert(tk.END, f"{symptom_id}: {name}")
    
    def diagnose(self):
        """执行诊断"""
        # 获取选中的症状
        selected_indices = self.symptom_listbox.curselection()
        selected_symptoms = []
        
        for index in selected_indices:
            symptom_str = self.symptom_listbox.get(index)
            symptom_id = symptom_str.split(':')[0]
            selected_symptoms.append(symptom_id)
        
        if not selected_symptoms:
            messagebox.showwarning("警告", "请至少选择一个症状！")
            return
        
        # 执行推理
        results, inference_process = self.inference_engine.inference(selected_symptoms)
        
        # 显示结果
        self.display_results(results, inference_process, selected_symptoms)
        
        # 保存结果到文件
        self.save_results_to_file(results, inference_process, selected_symptoms)
    
    def display_results(self, results, inference_process, selected_symptoms):
        """显示诊断结果"""
        # 清空文本框
        self.process_text.config(state=tk.NORMAL)
        self.process_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        # 显示选中的症状
        self.result_text.insert(tk.END, "您选择的症状：\n")
        for symptom_id in selected_symptoms:
            symptom_name = self.db_manager.get_symptom_name(symptom_id)
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
        
        # 禁用文本框编辑
        self.process_text.config(state=tk.DISABLED)
        self.result_text.config(state=tk.DISABLED)
    
    def save_results_to_file(self, results, inference_process, selected_symptoms):
        """保存诊断结果到文件"""
        # 创建结果文件路径
        result_file = os.path.abspath("result.out")
        
        try:
            with open(result_file, 'w', encoding='utf-8') as f:
                f.write("腹痛诊断系统结果\n")
                f.write("=" * 30 + "\n\n")
                
                # 写入选中的症状
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
        """清空选择"""
        self.symptom_listbox.selection_clear(0, tk.END)
        self.process_text.config(state=tk.NORMAL)
        self.process_text.delete(1.0, tk.END)
        self.process_text.config(state=tk.DISABLED)
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)
        self.file_path_label.config(text="")
    
    def open_rule_management(self):
        """打开规则管理窗口"""
        RuleManagementWindow(self.root, self.db_manager)
    
    def open_result_file(self, event):
        """打开结果文件"""
        file_path = self.file_path_label.cget("text").replace("结果已保存至: ", "")
        if file_path and os.path.exists(file_path):
            os.startfile(file_path)

# 规则管理窗口类
class RuleManagementWindow:
    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        
        # 创建窗口
        self.window = tk.Toplevel(parent)
        self.window.title("规则管理")
        self.window.geometry("700x500")
        
        # 创建界面组件
        self.create_widgets()
        
        # 加载规则
        self.load_rules()
    
    def create_widgets(self):
        """创建界面组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建规则列表
        rule_frame = ttk.LabelFrame(main_frame, text="规则列表", padding="10")
        rule_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 规则列表框
        self.rule_listbox = tk.Listbox(rule_frame, font=('Arial', 10), height=15)
        scrollbar = ttk.Scrollbar(rule_frame, orient=tk.VERTICAL, command=self.rule_listbox.yview)
        self.rule_listbox.config(yscrollcommand=scrollbar.set)
        
        self.rule_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 创建按钮区域
        button_frame = ttk.Frame(main_frame, padding="10")
        button_frame.pack(fill=tk.X)
        
        # 添加规则按钮
        self.add_button = ttk.Button(button_frame, text="添加规则", command=self.add_rule)
        self.add_button.pack(side=tk.LEFT, padx=5)
        
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

# 主函数
if __name__ == "__main__":
    root = tk.Tk()
    app = AbdomenPainDiagnosticSystem(root)
    root.mainloop()