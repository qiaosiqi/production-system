# # rules_engine.py
# from database import get_all_rules
#
# def infer_book(features):
#     """
#     基于输入特征进行推理
#     features: ['科幻','外国作家','20世纪']
#     """
#     rules = get_all_rules()
#     for _, cond, concl in rules:
#         cond_list = cond.split(',')
#         if all(f in features for f in cond_list):
#             return f"推荐书籍：{concl}"
#     return "未找到符合条件的书籍，请尝试输入更多特征。"

# rules_engine.py
from database import get_all_rules

def infer_book(features):
    """根据输入特征进行推理，返回推理过程与结果"""
    rules = get_all_rules()
    known_facts = set(features)
    reasoning_steps = []
    inferred = True

    # 不断尝试用规则推理，直到没有新结论产生
    while inferred:
        inferred = False
        for _, conds, concl in rules:
            cond_list = [c.strip() for c in conds.split(',')]
            if all(c in known_facts for c in cond_list) and concl not in known_facts:
                reasoning_steps.append(f"{'、'.join(cond_list)} → {concl}")
                known_facts.add(concl)
                inferred = True

    # 根据最终结论推测结果
    possible_results = [fact for fact in known_facts if fact not in features]

    if len(possible_results) > 0:
        final = possible_results[-1]  # 最后推导出的事实
        reasoning_steps.append(f"✅ 最终结论：{final}")
        return reasoning_steps, f"所识别的图书为：{final}"
    else:
        return reasoning_steps, "❌ 无法根据当前条件得出结论"
