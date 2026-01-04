import requests
import base64
import io
from PIL import Image
import numpy as np
import torch
import json

class QwenImageEditNode:
    """
    阿里云百炼平台Qwen图像编辑节点
    调用qwen-image-edit模型进行图像编辑
    
    支持功能：
    - 图像编辑和修改
    - 风格迁移
    - 物体增删
    - 文字编辑
    - 细节增强
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        """
        定义节点的输入类型
        
        Returns:
            dict: 包含required和optional参数的字典
        """
        return {
            "required": {
                "image": ("IMAGE", {
                    "tooltip": "输入要编辑的图像"
                }),
                "edit_instruction": ("STRING", {
                    "multiline": True,
                    "default": "请描述您想要对图像进行的编辑操作",
                    "tooltip": "编辑指令，支持中英文，最多800字符"
                }),
                "api_key": ("STRING", {
                    "default": "your-api-key-here",
                    "tooltip": "阿里云百炼平台API密钥"
                }),
            },
            "optional": {
                "model_name": ("STRING", {
                    "default": "qwen-image-edit",
                    "tooltip": "模型名称，默认为qwen-image-edit"
                }),
                "negative_prompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "低分辨率、错误、最差质量、低质量、残缺、多余的手指、比例不良等",
                    "tooltip": "反向提示词，描述不希望在画面中看到的内容，最多500字符"
                }),
                "watermark": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "是否添加水印标识，水印位于图片右下角"
                }),
                "seed": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 2147483647,
                    "step": 1,
                    "tooltip": "随机数种子，-1表示随机生成"
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("edited_image",)
    FUNCTION = "edit_image"
    CATEGORY = "XJ_Nodes/Image"
    
    def tensor_to_base64(self, tensor_image):
        """
        将tensor图像转换为base64编码
        
        Args:
            tensor_image: 输入的tensor图像，形状为[B,H,W,C]或[H,W,C]
            
        Returns:
            str: base64编码的图像字符串
            
        Raises:
            Exception: 当图像转换失败时抛出异常
        """
        try:
            # 处理tensor维度
            if len(tensor_image.shape) == 4:
                tensor_image = tensor_image.squeeze(0)
            elif len(tensor_image.shape) != 3:
                raise ValueError(f"不支持的tensor维度: {tensor_image.shape}")
            
            # 确保数值范围在0-1之间
            if tensor_image.max() > 1.0:
                tensor_image = tensor_image / 255.0
            
            # 限制数值范围
            tensor_image = torch.clamp(tensor_image, 0.0, 1.0)
                
            # 转换为numpy数组
            numpy_image = (tensor_image.cpu().numpy() * 255).astype(np.uint8)
            
            # 创建PIL图像
            pil_image = Image.fromarray(numpy_image)
            
            # 确保图像尺寸符合API要求（384-3072像素）
            width, height = pil_image.size
            if width < 384 or height < 384 or width > 3072 or height > 3072:
                # 调整图像尺寸
                if width < 384 or height < 384:
                    # 放大到最小尺寸
                    scale = max(384 / width, 384 / height)
                    new_width = int(width * scale)
                    new_height = int(height * scale)
                else:
                    # 缩小到最大尺寸
                    scale = min(3072 / width, 3072 / height)
                    new_width = int(width * scale)
                    new_height = int(height * scale)
                
                pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 转换为base64
            buffer = io.BytesIO()
            pil_image.save(buffer, format='JPEG', quality=95, optimize=True)
            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            return img_base64
            
        except Exception as e:
            raise Exception(f"图像转换为base64失败: {str(e)}")
    
    def base64_to_tensor(self, base64_string):
        """
        将base64编码转换为tensor图像
        
        Args:
            base64_string (str): base64编码的图像字符串
            
        Returns:
            torch.Tensor: tensor格式的图像，形状为[1,H,W,3]
            
        Raises:
            Exception: 当base64解码或图像转换失败时抛出异常
        """
        try:
            # 移除可能的data URL前缀
            if base64_string.startswith('data:image/'):
                base64_string = base64_string.split(',')[1]
            
            # 解码base64
            img_data = base64.b64decode(base64_string)
            
            # 转换为PIL图像
            pil_image = Image.open(io.BytesIO(img_data))
            
            # 确保是RGB模式
            if pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')
            
            # 转换为numpy数组
            numpy_image = np.array(pil_image).astype(np.float32) / 255.0
            
            # 转换为tensor，添加batch维度
            tensor_image = torch.from_numpy(numpy_image).unsqueeze(0)
            
            return tensor_image
            
        except Exception as e:
            raise Exception(f"base64转换为tensor失败: {str(e)}")
    
    def download_image_to_base64(self, image_url):
        """
        从URL下载图片并转换为base64字符串
        
        Args:
            image_url: 图片URL
            
        Returns:
            base64编码的图像字符串
        """
        try:
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            # 将图片数据转换为base64
            image_base64 = base64.b64encode(response.content).decode('utf-8')
            return image_base64
            
        except Exception as e:
            raise Exception(f"下载图片失败: {str(e)}")
    
    def call_qwen_api(self, image_base64, edit_instruction, api_key, model_name="qwen-image-edit", negative_prompt="", watermark=False, seed=-1):
        """
        调用阿里云百炼平台的Qwen图像编辑API
        
        Args:
            image_base64 (str): base64编码的输入图像
            instruction (str): 编辑指令，最多800字符
            api_key (str): API密钥
            model_name (str): 模型名称
            **kwargs: 其他参数
            
        Returns:
            str: 编辑后的图像base64字符串
            
        Raises:
            Exception: 当API调用失败时抛出异常
        """
        # 验证输入参数
        if not api_key or api_key == "your-api-key-here":
            raise Exception("请设置有效的API密钥")
        
        if len(edit_instruction) > 800:
            raise Exception("编辑指令不能超过800字符")
            
        if len(negative_prompt) > 500:
            raise Exception("负面提示词不能超过500字符")
        
        # 修正API端点URL - 使用正确的multimodal-generation端点
        url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # 构建请求数据，严格按照官方API文档格式
        data = {
            "model": model_name,
            "input": {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "image": f"data:image/jpeg;base64,{image_base64}"
                            },
                            {
                                "text": edit_instruction
                            }
                        ]
                    }
                ]
            },
            "parameters": {}
        }
        
        # 添加可选参数
        if negative_prompt.strip():
            data["parameters"]["negative_prompt"] = negative_prompt.strip()
        
        if watermark is not None:
            data["parameters"]["watermark"] = watermark
        
        if seed != -1:
            data["parameters"]["seed"] = seed
        
        try:
            print(f"正在调用API: {model_name}")
            response = requests.post(url, json=data, headers=headers, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            print(f"API响应状态: {result.get('status_code', 'unknown')}")
            
            # 根据官方文档解析响应格式
            if "output" in result and "choices" in result["output"]:
                choices = result["output"]["choices"]
                if choices and len(choices) > 0:
                    message = choices[0].get("message", {})
                    content = message.get("content", [])
                    
                    # 查找图像内容
                    for item in content:
                        if "image" in item:
                            image_data = item["image"]
                            print(f"获取到图像数据: {str(image_data)[:50]}...")
                            
                            # 如果是URL，下载并转换为base64
                            if isinstance(image_data, str) and image_data.startswith(('http://', 'https://')):
                                return self.download_image_to_base64(image_data)
                            elif isinstance(image_data, str) and image_data.startswith('data:image/'):
                                # 如果是base64格式，提取base64部分
                                if ';base64,' in image_data:
                                    return image_data.split(';base64,')[1]
                                return image_data
                            else:
                                # 直接返回图像数据
                                return str(image_data)
            
            # 检查错误信息
            if "code" in result:
                error_msg = result.get("message", "未知错误")
                raise Exception(f"API返回错误 {result['code']}: {error_msg}")
            
            raise Exception(f"API响应格式异常: {json.dumps(result, ensure_ascii=False)[:200]}")
            
        except requests.exceptions.Timeout:
            raise Exception("API请求超时，请稍后重试")
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")
        except json.JSONDecodeError:
            raise Exception("API响应不是有效的JSON格式")
        except Exception as e:
            if "API" in str(e):
                raise e
            else:
                raise Exception(f"处理API响应时出错: {str(e)}")
    
    def edit_image(self, image, edit_instruction, api_key, model_name="qwen-image-edit", 
                   negative_prompt="", watermark=False, seed=-1):
        """
        编辑图像的主函数
        
        Args:
            image (torch.Tensor): 输入图像tensor，形状为[B,H,W,C]
            edit_instruction (str): 编辑指令，支持中英文，最多800字符
            api_key (str): 阿里云百炼平台API密钥
            model_name (str): 模型名称，默认qwen-image-edit
            negative_prompt (str): 负面提示词，最多500字符
            watermark (bool): 是否添加水印标识
            seed (int): 随机种子，-1表示随机生成
            
        Returns:
            tuple: 包含编辑后图像tensor的元组
            
        Raises:
            Exception: 当图像编辑失败时抛出异常
        """
        try:
            print(f"开始图像编辑任务...")
            print(f"编辑指令: {edit_instruction[:50]}{'...' if len(edit_instruction) > 50 else ''}")
            
            # 验证输入参数
            if not api_key or api_key == "your-api-key-here":
                raise Exception("请设置有效的API密钥")
            
            if not edit_instruction.strip():
                raise Exception("编辑指令不能为空")
                
            if len(edit_instruction) > 800:
                raise Exception("编辑指令不能超过800字符")
            
            if len(negative_prompt) > 500:
                raise Exception("负面提示词不能超过500字符")
            
            # 验证图像tensor格式
            if not isinstance(image, torch.Tensor):
                raise Exception("输入必须是torch.Tensor格式")
                
            if len(image.shape) not in [3, 4]:
                raise Exception(f"不支持的图像tensor维度: {image.shape}")
            
            print(f"输入图像尺寸: {image.shape}")
            
            # 将输入图像转换为base64
            print("正在转换图像格式...")
            input_base64 = self.tensor_to_base64(image)
            
            # 调用API进行图像编辑
            print("正在调用千问图像编辑API...")
            result_base64 = self.call_qwen_api(
                image_base64=input_base64,
                edit_instruction=edit_instruction.strip(),
                api_key=api_key,
                model_name=model_name,
                negative_prompt=negative_prompt.strip(),
                watermark=watermark,
                seed=seed
            )
            
            # 将结果转换回tensor
            print("正在转换结果图像...")
            result_tensor = self.base64_to_tensor(result_base64)
            
            print(f"图像编辑完成，输出尺寸: {result_tensor.shape}")
            return (result_tensor,)
            
        except Exception as e:
            error_msg = f"图像编辑失败: {str(e)}"
            print(error_msg)
            # 抛出异常而不是返回原图，让用户知道具体错误
            raise Exception(error_msg)
    
    @staticmethod
    def test_api_connection(api_key):
        """
        测试API连接是否正常
        
        Args:
            api_key (str): API密钥
            
        Returns:
            bool: 连接是否成功
        """
        try:
            if not api_key or api_key == "your-api-key-here":
                return False, "请设置有效的API密钥"
            
            # 简单的API连接测试
            url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            # 发送一个简单的测试请求
            response = requests.get(url.replace('/generation', ''), headers=headers, timeout=10)
            
            if response.status_code == 401:
                return False, "API密钥无效"
            elif response.status_code == 403:
                return False, "API密钥权限不足"
            else:
                return True, "API连接正常"
                
        except Exception as e:
            return False, f"连接测试失败: {str(e)}"

# 节点映射
NODE_CLASS_MAPPINGS = {
    "QwenImageEditNode": QwenImageEditNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "QwenImageEditNode": "Qwen图像编辑"
}