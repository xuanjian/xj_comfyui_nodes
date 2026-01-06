# 创建AnyType类以支持通配符类型
class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

# 创建any实例作为通配符
any_type = AnyType("*")


class ConditionalPassNode:
    """
    ComfyUI节点：条件传递节点
    根据布尔值决定是否传递值到下一个节点
    如果condition为True，则输出value继续流程
    如果condition为False，则输出None（后续节点需要处理None值）
    
    注意：ComfyUI无法真正"终止"流程，当condition为False时，节点会输出None。
    建议后续节点检查输入是否为None来决定是否执行。
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
                "condition": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "条件值，True时传递值，False时输出None"
                }),
                "value": (any_type, {
                    "tooltip": "要传递的值，可以是任何类型"
                })
            }
        }
    
    @classmethod
    def VALIDATE_INPUTS(cls, **kwargs):
        """
        验证输入，允许任何类型的value输入
        """
        return True
    
    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("output",)
    FUNCTION = "conditional_pass"
    CATEGORY = "XJ Nodes/Utils"
    
    def conditional_pass(self, condition, value):
        """
        根据条件决定是否传递值
        
        Args:
            condition (bool): 条件值
            value: 要传递的值
        
        Returns:
            tuple: 如果condition为True返回(value,)，否则返回(None,)
        """
        if condition:
            return (value,)
        else:
            # 返回None，后续节点可以检查是否为None来决定是否执行
            return (None,)


# ComfyUI节点映射
NODE_CLASS_MAPPINGS = {
    "ConditionalPassNode": ConditionalPassNode
}

# 节点显示名称映射
NODE_DISPLAY_NAME_MAPPINGS = {
    "ConditionalPassNode": "Conditional Pass (XJ)"
}
