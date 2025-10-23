# rules_engine.py
from database import get_all_rules

def infer_book(features):
    """
    基于输入特征进行推理
    features: ['科幻','外国作家','20世纪']
    """
    rules = get_all_rules()
    for _, cond, concl in rules:
        cond_list = cond.split(',')
        if all(f in features for f in cond_list):
            return f"推荐书籍：{concl}"
    return "未找到符合条件的书籍，请尝试输入更多特征。"
