import requests
from PIL import Image
import torch
import numpy as np
from io import BytesIO

class ImageUrlLoaderNode:
    """
    ComfyUI节点：从URL加载图片
    输入图片URL，输出图片对象
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
                "image_url": ("STRING", {
                    "default": "https://example.com/image.jpg",
                    "multiline": False,
                    "display": "text"
                })
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "load_image_from_url"
    CATEGORY = "XJ Nodes/Image"
    
    def load_image_from_url(self, image_url):
        """
        从URL加载图片并转换为ComfyUI格式
        
        Args:
            image_url (str): 图片的URL地址
        
        Returns:
            tuple: 包含图片张量的元组
        """
        try:
            # 发送HTTP请求获取图片数据
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            # 使用PIL打开图片
            image = Image.open(BytesIO(response.content))
            
            # 转换为RGB格式（如果不是的话）
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # 转换为numpy数组
            image_np = np.array(image).astype(np.float32) / 255.0
            
            # 转换为torch张量并调整维度 (H, W, C) -> (1, H, W, C)
            image_tensor = torch.from_numpy(image_np).unsqueeze(0)
            
            return (image_tensor,)
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"无法从URL加载图片: {str(e)}")
        except Exception as e:
            raise Exception(f"图片处理错误: {str(e)}")

# 节点映射
NODE_CLASS_MAPPINGS = {
    "ImageUrlLoaderNode": ImageUrlLoaderNode
}

# 显示名称映射
NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageUrlLoaderNode": "图像URL加载器 (XJ)"
}