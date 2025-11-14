# 数据库初始化和操作类
import sqlite3

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