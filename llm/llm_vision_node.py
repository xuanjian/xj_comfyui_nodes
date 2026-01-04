import requests
import json
import base64
import io
from PIL import Image
from typing import Dict, Any, Optional, Tuple, Union

class LLMVisionNode:
    """
    LLM视觉API调用节点
    支持图像+文本输入的多模态大语言模型API调用
    支持GPT-4V、Qwen-VL、GLM-4V等视觉模型
    """
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        """
        定义节点的输入类型
        """
        return {
            "required": {
                "base_url": ("STRING", {
                    "default": "https://api.openai.com/v1",
                    "multiline": False,
                    "tooltip": "API基础URL，如：https://api.openai.com/v1 或 https://dashscope.aliyuncs.com/compatible-mode/v1"
                }),
                "api_key": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "tooltip": "API密钥"
                }),
                "model": ("STRING", {
                    "default": "gpt-4-vision-preview",
                    "multiline": False,
                    "tooltip": "视觉模型名称，如：gpt-4-vision-preview、qwen-vl-plus、glm-4v等"
                }),
                "prompt": ("STRING", {
                    "default": "请描述这张图片的内容。",
                    "multiline": True,
                    "tooltip": "用户输入的提示词"
                }),
            },
            "optional": {
                "image": ("IMAGE", {
                    "tooltip": "输入图像（可选）"
                }),
                "system_prompt": ("STRING", {
                    "default": "你是一个有用的AI视觉助手，能够理解和分析图像内容。",
                    "multiline": True,
                    "tooltip": "系统提示词，定义AI的角色和行为"
                }),
                "temperature": ("FLOAT", {
                    "default": 0.7,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1,
                    "tooltip": "控制输出的随机性"
                }),
                "max_tokens": ("INT", {
                    "default": 1000,
                    "min": 1,
                    "max": 4096,
                    "step": 1,
                    "tooltip": "最大输出token数量"
                }),
                "detail_level": (["low", "high", "auto"], {
                    "default": "auto",
                    "tooltip": "图像分析详细程度"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("response", "full_response", "usage_info")
    FUNCTION = "call_llm_vision_api"
    CATEGORY = "XJ Nodes/LLM"
    
    def image_to_base64(self, image_tensor) -> str:
        """
        将图像张量转换为base64编码字符串
        
        Args:
            image_tensor: ComfyUI图像张量
            
        Returns:
            str: base64编码的图像字符串
        """
        try:
            # 转换张量为PIL图像
            if len(image_tensor.shape) == 4:
                # 批次维度，取第一张图像
                image_array = image_tensor[0].cpu().numpy()
            else:
                image_array = image_tensor.cpu().numpy()
            
            # 确保数值范围在0-255
            if image_array.max() <= 1.0:
                image_array = (image_array * 255).astype('uint8')
            else:
                image_array = image_array.astype('uint8')
            
            # 转换为PIL图像
            pil_image = Image.fromarray(image_array)
            
            # 转换为base64
            buffer = io.BytesIO()
            pil_image.save(buffer, format='JPEG', quality=95)
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            return image_base64
            
        except Exception as e:
            print(f"[LLM Vision] 图像转换错误: {str(e)}")
            raise Exception(f"图像转换失败: {str(e)}")
    
    def call_llm_vision_api(
        self,
        base_url: str,
        api_key: str,
        model: str,
        prompt: str,
        image=None,
        system_prompt: str = "你是一个有用的AI视觉助手，能够理解和分析图像内容。",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        detail_level: str = "auto"
    ) -> Tuple[str, str, str]:
        """
        调用LLM视觉API获取响应
        
        Args:
            base_url: API基础URL
            api_key: API密钥
            model: 模型名称
            prompt: 用户提示词
            image: 输入图像（可选）
            system_prompt: 系统提示词
            temperature: 温度参数
            max_tokens: 最大token数
            detail_level: 图像分析详细程度
            
        Returns:
            Tuple[str, str, str]: (响应内容, 完整响应JSON, 使用信息)
        """
        try:
            # 验证输入参数
            if not base_url or not api_key or not model:
                raise ValueError("base_url、api_key和model参数不能为空")
            
            # 确保base_url以正确格式结尾
            if not base_url.endswith('/v1'):
                if not base_url.endswith('/'):
                    base_url += '/'
                if not base_url.endswith('v1/'):
                    base_url += 'v1'
            
            # 构建请求URL
            url = f"{base_url}/chat/completions"
            
            # 构建请求头
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            # 构建消息列表
            messages = []
            if system_prompt and system_prompt.strip():
                messages.append({
                    "role": "system",
                    "content": system_prompt.strip()
                })
            
            # 构建用户消息内容
            user_content = []
            
            # 添加文本内容
            user_content.append({
                "type": "text",
                "text": prompt
            })
            
            # 如果有图像，添加图像内容
            if image is not None:
                try:
                    image_base64 = self.image_to_base64(image)
                    user_content.append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}",
                            "detail": detail_level
                        }
                    })
                    print(f"[LLM Vision] 成功添加图像，base64长度: {len(image_base64)}")
                except Exception as e:
                    print(f"[LLM Vision] 图像处理失败: {str(e)}")
                    return (f"图像处理失败: {str(e)}", "", "")
            
            messages.append({
                "role": "user",
                "content": user_content
            })
            
            # 构建请求数据
            data = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            print(f"[LLM Vision] 发送请求到: {url}")
            print(f"[LLM Vision] 使用模型: {model}")
            print(f"[LLM Vision] 包含图像: {'是' if image is not None else '否'}")
            print(f"[LLM Vision] 请求参数: temperature={temperature}, max_tokens={max_tokens}")
            
            # 发送请求
            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=120  # 视觉模型通常需要更长时间
            )
            
            print(f"[LLM Vision] 响应状态码: {response.status_code}")
            
            # 检查响应状态
            if response.status_code != 200:
                error_msg = f"API请求失败，状态码: {response.status_code}"
                try:
                    error_detail = response.json()
                    error_msg += f"\n错误详情: {json.dumps(error_detail, ensure_ascii=False, indent=2)}"
                except:
                    error_msg += f"\n响应内容: {response.text}"
                raise Exception(error_msg)
            
            # 解析响应
            response_data = response.json()
            print(f"[LLM Vision] 响应数据结构: {list(response_data.keys())}")
            
            # 提取响应内容
            if "choices" in response_data and len(response_data["choices"]) > 0:
                choice = response_data["choices"][0]
                if "message" in choice and "content" in choice["message"]:
                    content = choice["message"]["content"]
                elif "text" in choice:
                    content = choice["text"]
                else:
                    content = str(choice)
            else:
                content = "未找到有效的响应内容"
            
            # 提取使用信息
            usage_info = ""
            if "usage" in response_data:
                usage = response_data["usage"]
                usage_info = f"输入tokens: {usage.get('prompt_tokens', 'N/A')}, 输出tokens: {usage.get('completion_tokens', 'N/A')}, 总计: {usage.get('total_tokens', 'N/A')}"
            
            # 格式化完整响应
            full_response = json.dumps(response_data, ensure_ascii=False, indent=2)
            
            print(f"[LLM Vision] 成功获取响应，内容长度: {len(content)}")
            
            return (content, full_response, usage_info)
            
        except requests.exceptions.Timeout:
            error_msg = "请求超时，视觉模型处理时间较长，请稍后重试"
            print(f"[LLM Vision] 错误: {error_msg}")
            return (error_msg, "", "")
            
        except requests.exceptions.ConnectionError:
            error_msg = "连接错误，请检查base_url是否正确以及网络连接"
            print(f"[LLM Vision] 错误: {error_msg}")
            return (error_msg, "", "")
            
        except Exception as e:
            error_msg = f"调用LLM视觉API时发生错误: {str(e)}"
            print(f"[LLM Vision] 错误: {error_msg}")
            return (error_msg, "", "")

# 节点映射
NODE_CLASS_MAPPINGS = {
    "LLMVisionNode": LLMVisionNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LLMVisionNode": "LLM视觉API调用"
}