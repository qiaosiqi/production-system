# 推理引擎模块
# 负责根据用户选择的症状，应用规则库进行诊断推理
from db_manager import DatabaseManager

class InferenceEngine:
    def __init__(self, db_manager):
        """初始化推理引擎
        
        参数:
            db_manager: DatabaseManager实例，用于访问数据库中的规则和诊断结果
        """
        self.db_manager = db_manager
    
    def inference(self, selected_symptoms):
        """根据用户选择的症状进行推理
        
        参数:
            selected_symptoms: 用户选择的症状ID列表
            
        返回:
            tuple: (诊断结果列表, 推理过程列表)
                - 诊断结果列表: 包含(诊断名称, 诊断ID, 规则描述)的元组
                - 推理过程列表: 记录应用的规则描述
        """
        # 从数据库获取所有规则
        rules = self.db_manager.get_all_rules()
        results = []  # 存储诊断结果
        inference_process = []  # 存储推理过程
        
        # 将选中的症状转换为集合，提高判断效率
        selected_set = set(selected_symptoms)
        
        # 遍历所有规则，寻找匹配的条件
        for rule in rules:
            rule_id, premises_str, conclusion, description = rule
            # 将前提条件字符串拆分为症状ID列表
            premises = premises_str.split(',')
            
            # 检查当前规则的所有前提条件是否都在用户选择的症状中
            if set(premises).issubset(selected_set):
                # 根据诊断ID获取诊断名称
                diagnostic_name = self.db_manager.get_diagnostic_name(conclusion)
                # 添加到结果列表
                results.append((diagnostic_name, conclusion, description))
                # 记录推理过程
                inference_process.append(description)
        
        return results, inference_process