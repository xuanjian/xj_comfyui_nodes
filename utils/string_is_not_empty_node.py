class StringIsNotEmptyNode:
    """
    ComfyUI节点：判断字符串是否非空
    输入字符串，如果非空返回True，空字符串返回False
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
                "text": ("STRING", {
                    "multiline": False,
                    "default": "",
                    "tooltip": "要判断的字符串"
                })
            }
        }
    
    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("is_not_empty",)
    FUNCTION = "check_not_empty"
    CATEGORY = "XJ Nodes/Utils"
    
    def check_not_empty(self, text):
        """
        判断字符串是否非空
        
        Args:
            text (str): 输入的字符串
        
        Returns:
            tuple: 包含布尔值的元组，非空返回True，空返回False
        """
        # 去除首尾空白后判断是否为空
        is_not_empty = bool(text and text.strip())
        return (is_not_empty,)


# ComfyUI节点映射
NODE_CLASS_MAPPINGS = {
    "StringIsNotEmptyNode": StringIsNotEmptyNode
}

# 节点显示名称映射
NODE_DISPLAY_NAME_MAPPINGS = {
    "StringIsNotEmptyNode": "String Is Not Empty (XJ)"
}
