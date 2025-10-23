# knowledge_graph.py
import networkx as nx
import matplotlib.pyplot as plt
from database import get_all_rules

# ✅ 新增：设置中文字体和负号正常显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体（SimHei）
plt.rcParams['axes.unicode_minus'] = False    # 正常显示负号

def show_knowledge_graph():
    rules = get_all_rules()
    G = nx.DiGraph()
    for _, cond, concl in rules:
        for c in cond.split(','):
            G.add_edge(c.strip(), concl.strip())

    plt.figure(figsize=(8,6))
    nx.draw(G, with_labels=True, node_color='lightblue', node_size=1800, font_size=10, arrows=True)
    plt.title("📚 图书知识图谱")
    plt.show()
