# database.py
import sqlite3

DB_NAME = "system.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conditions TEXT,
            conclusion TEXT
        )
    ''')
    conn.commit()

    # 示例规则初始化
    cursor.execute("SELECT COUNT(*) FROM rules")
    if cursor.fetchone()[0] == 0:
        sample_rules = [
            ('科幻,外国作家,20世纪', '《基地》'),
            ('文学,外国作家,19世纪', '《悲惨世界》'),
            ('哲学,古代,外国作家', '《理想国》'),
            ('悬疑,外国作家,现代', '《福尔摩斯探案集》'),
            ('科技,非虚构,现代', '《人类简史》'),
        ]
        cursor.executemany("INSERT INTO rules (conditions, conclusion) VALUES (?, ?)", sample_rules)
        conn.commit()
    conn.close()

def get_all_rules():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rules")
    data = cursor.fetchall()
    conn.close()
    return data

def add_rule(conditions, conclusion):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO rules (conditions, conclusion) VALUES (?, ?)", (conditions, conclusion))
    conn.commit()
    conn.close()

def delete_rule(rule_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM rules WHERE id=?", (rule_id,))
    conn.commit()
    conn.close()

def update_rule(rule_id, conditions, conclusion):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE rules SET conditions=?, conclusion=? WHERE id=?", (conditions, conclusion, rule_id))
    conn.commit()
    conn.close()
