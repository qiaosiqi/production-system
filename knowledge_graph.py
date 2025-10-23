# knowledge_graph.py
import os
import networkx as nx
import matplotlib.pyplot as plt
from database import get_all_rules

# ✅ 设置中文和负号
plt.rcParams['font.sans-serif'] = ['SimHei']
checkFlag = False
plt.rcParams['axes.unicode_minus'] = False


def show_knowledge_graph():
    if check():
        show_graph()
    else:
        print("Already existed.")

def show_graph():
    rules = get_all_rules()

    # 创建有向图
    G = nx.DiGraph()
    for _, cond, concl in rules:
        for c in cond.split(','):
            c = c.strip()
            if c:
                G.add_edge(c, concl.strip())

    if len(G.nodes) == 0:
        print("❌ 当前数据库中没有规则，无法生成知识图谱")
        return

    # ✅ 使用 spring_layout 自动布局，防止节点重叠
    pos = nx.spring_layout(G, k=1.5, iterations=100, seed=42)
    # k 值越大，节点间距离越远；iterations 越多布局越均匀

    plt.figure(figsize=(10, 8))

    # ✅ 不再使用 zorder 参数（兼容所有 NetworkX 版本）
    nx.draw_networkx_nodes(
        G,
        pos,
        node_color='skyblue',
        node_size=2600,
        edgecolors='black',
        linewidths=1.5
    )

    nx.draw_networkx_edges(
        G,
        pos,
        arrowstyle='-|>',
        arrowsize=16,
        edge_color='gray',
        width=1.2,
        connectionstyle="arc3,rad=0.15",  # 轻微弧线，减少箭头穿圈
        min_source_margin=25,
        min_target_margin=25
    )

    nx.draw_networkx_labels(
        G,
        pos,
        font_size=11,
        font_weight='bold',
        verticalalignment='center'
    )

    plt.title("📚 图书知识图谱", fontsize=14, fontweight='bold')
    plt.axis('off')

    # ✅ 保存图片到项目目录下
    output_path = os.path.join(os.path.dirname(__file__), "book_knowledge_graph.png")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    print(f"✅ 知识图谱已保存到: {output_path}")

    # plt.show()

def check():
    return checkFlag