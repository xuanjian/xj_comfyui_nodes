class AverageNode:
    """
    ComfyUI节点：返回两个数字的平均值
    输入两个数字，输出它们的平均值
    """
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        """
        定义节点的输入类型
        返回输入参数的配置字典
        """
        return {
            "required": {
                "input1": ("INT", {
                    "default": 1
                }),
                "input2": ("INT", {
                    "default": 0
                })
            }
        }
    
    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("average_value",)
    FUNCTION = "get_average"
    CATEGORY = "XJ Nodes/Math"
    
    def get_average(self, input1, input2):
        """
        返回两个数字的平均值
        
        Args:
            input1 (int|float): 第一个输入值
            input2 (int|float): 第二个输入值
        
        Returns:
            tuple: 包含平均值的元组
        """
        result = (input1 + input2) / 2.0
        return (result,)


# ComfyUI节点映射
NODE_CLASS_MAPPINGS = {
    "AverageNode": AverageNode
}

# 节点显示名称映射
NODE_DISPLAY_NAME_MAPPINGS = {
    "AverageNode": "Average (XJ)"
}