import requests
import json
import base64
from typing import Dict, Any, Optional, Tuple

class LLMAPINode:
    """
    LLM API调用节点
    支持OpenAI兼容的API接口调用各种大语言模型
    包括但不限于：OpenAI、阿里云通义千问、百度文心一言、智谱GLM等
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
                    "default": "gpt-3.5-turbo",
                    "multiline": False,
                    "tooltip": "模型名称，如：gpt-3.5-turbo、qwen-turbo、ERNIE-Bot等"
                }),
                "prompt": ("STRING", {
                    "default": "你好，请介绍一下你自己。",
                    "multiline": True,
                    "tooltip": "用户输入的提示词"
                }),
            },
            "optional": {
                "system_prompt": ("STRING", {
                    "default": "你是一个有用的AI助手。",
                    "multiline": True,
                    "tooltip": "系统提示词，定义AI的角色和行为"
                }),
                "temperature": ("FLOAT", {
                    "default": 0.7,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1,
                    "tooltip": "控制输出的随机性，0为确定性输出，2为最随机"
                }),
                "max_tokens": ("INT", {
                    "default": 1000,
                    "min": 1,
                    "max": 8192,
                    "step": 1,
                    "tooltip": "最大输出token数量"
                }),
                "top_p": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1,
                    "tooltip": "核采样参数，控制输出的多样性"
                }),
                "stream": (["false", "true"], {
                    "default": "false",
                    "tooltip": "是否启用流式输出"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("response", "full_response", "usage_info")
    FUNCTION = "call_llm_api"
    CATEGORY = "XJ Nodes/LLM"
    
    def call_llm_api(
        self,
        base_url: str,
        api_key: str,
        model: str,
        prompt: str,
        system_prompt: str = "你是一个有用的AI助手。",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        top_p: float = 1.0,
        stream: str = "false"
    ) -> Tuple[str, str, str]:
        """
        调用LLM API获取响应
        
        Args:
            base_url: API基础URL
            api_key: API密钥
            model: 模型名称
            prompt: 用户提示词
            system_prompt: 系统提示词
            temperature: 温度参数
            max_tokens: 最大token数
            top_p: top_p参数
            stream: 是否流式输出
            
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
            
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            # 构建请求数据
            data = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p,
                "stream": stream.lower() == "true"
            }
            
            print(f"[LLM API] 发送请求到: {url}")
            print(f"[LLM API] 使用模型: {model}")
            print(f"[LLM API] 请求参数: temperature={temperature}, max_tokens={max_tokens}, top_p={top_p}")
            
            # 发送请求
            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=60
            )
            
            print(f"[LLM API] 响应状态码: {response.status_code}")
            
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
            print(f"[LLM API] 响应数据结构: {list(response_data.keys())}")
            
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
            
            print(f"[LLM API] 成功获取响应，内容长度: {len(content)}")
            
            return (content, full_response, usage_info)
            
        except requests.exceptions.Timeout:
            error_msg = "请求超时，请检查网络连接或增加超时时间"
            print(f"[LLM API] 错误: {error_msg}")
            return (error_msg, "", "")
            
        except requests.exceptions.ConnectionError:
            error_msg = "连接错误，请检查base_url是否正确以及网络连接"
            print(f"[LLM API] 错误: {error_msg}")
            return (error_msg, "", "")
            
        except Exception as e:
            error_msg = f"调用LLM API时发生错误: {str(e)}"
            print(f"[LLM API] 错误: {error_msg}")
            return (error_msg, "", "")

# 节点映射
NODE_CLASS_MAPPINGS = {
    "LLMAPINode": LLMAPINode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LLMAPINode": "LLM API调用"
}