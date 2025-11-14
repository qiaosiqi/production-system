# 推理引擎类
from db_manager import DatabaseManager

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