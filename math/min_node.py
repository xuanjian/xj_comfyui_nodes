class MinNode:
    """
    ComfyUI节点：返回两个数字中的最小值
    输入两个数字，输出较小的数字
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
    
    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("min_value",)
    FUNCTION = "get_min"
    CATEGORY = "XJ Nodes/Math"
    
    def get_min(self, input1, input2):
        """
        返回两个数字中的最小值
        
        Args:
            input1 (int): 第一个输入值
            input2 (int): 第二个输入值
        
        Returns:
            tuple: 包含最小值的元组
        """
        result = min(input1, input2)
        return (result,)


# ComfyUI节点映射
NODE_CLASS_MAPPINGS = {
    "MinNode": MinNode
}

# 节点显示名称映射
NODE_DISPLAY_NAME_MAPPINGS = {
    "MinNode": "Min (XJ)"
}