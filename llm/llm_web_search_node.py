import requests
import json
import base64
import io
from PIL import Image
from typing import Dict, Any, Optional, Tuple
import urllib.parse

class LLMWebSearchNode:
    """
    LLM API调用节点（支持网络搜索）
    支持在调用LLM之前先进行Google搜索，然后将搜索结果作为上下文提供给LLM
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
                    "default": "请搜索并告诉我最新的AI技术发展。",
                    "multiline": True,
                    "tooltip": "用户输入的提示词"
                }),
                "enable_search": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "是否启用网络搜索"
                }),
                "search_api": (["serpapi", "google_custom", "duckduckgo"], {
                    "default": "serpapi",
                    "tooltip": "选择搜索引擎API"
                }),
            },
            "optional": {
                "image": ("IMAGE", {
                    "tooltip": "输入图像（可选），支持图像+文本+搜索的多模态查询"
                }),
                "system_prompt": ("STRING", {
                    "default": "你是一个有用的AI助手，能够根据搜索结果回答问题。",
                    "multiline": True,
                    "tooltip": "系统提示词"
                }),
                "search_api_key": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "tooltip": "搜索引擎API密钥\nSerpAPI: https://serpapi.com/dashboard (注册后获取)\nGoogle Custom Search: https://console.cloud.google.com/apis/credentials (创建API密钥)"
                }),
                "google_cx": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "tooltip": "Google Custom Search Engine ID\n获取地址: https://programmablesearchengine.google.com/controlpanel/create (创建自定义搜索引擎后获取)"
                }),
                "num_results": ("INT", {
                    "default": 5,
                    "min": 1,
                    "max": 10,
                    "tooltip": "搜索结果数量"
                }),
                "temperature": ("FLOAT", {
                    "default": 0.7,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.01,
                    "tooltip": "温度参数，控制输出的随机性"
                }),
                "max_tokens": ("INT", {
                    "default": 2000,
                    "min": 1,
                    "max": 16384,
                    "step": 1,
                    "tooltip": "最大token数"
                }),
                "top_p": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "tooltip": "top_p参数"
                }),
                "detail_level": (["low", "high", "auto"], {
                    "default": "auto",
                    "tooltip": "图像分析详细程度（仅在有图像输入时有效）"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("response", "search_results", "full_response", "usage_info")
    FUNCTION = "call_llm_with_search"
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
            print(f"[LLM Web Search] 图像转换错误: {str(e)}")
            raise Exception(f"图像转换失败: {str(e)}")
    
    def google_search_serpapi(self, query: str, api_key: str, num_results: int = 5) -> str:
        """
        使用SerpAPI进行Google搜索
        需要注册SerpAPI账号：https://serpapi.com/
        """
        try:
            url = "https://serpapi.com/search"
            params = {
                "q": query,
                "api_key": api_key,
                "engine": "google",
                "num": num_results
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # 提取搜索结果
            results = []
            if "organic_results" in data:
                for item in data["organic_results"][:num_results]:
                    title = item.get("title", "")
                    snippet = item.get("snippet", "")
                    link = item.get("link", "")
                    results.append(f"标题: {title}\n摘要: {snippet}\n链接: {link}\n")
            
            return "\n".join(results) if results else "未找到相关搜索结果。"
        except Exception as e:
            return f"搜索出错: {str(e)}"
    
    def google_search_custom(self, query: str, api_key: str, cx: str, num_results: int = 5) -> str:
        """
        使用Google Custom Search API进行搜索
        需要：
        1. 在Google Cloud Console创建项目并启用Custom Search API
        2. 创建自定义搜索引擎：https://programmablesearchengine.google.com/
        """
        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                "key": api_key,
                "cx": cx,
                "q": query,
                "num": min(num_results, 10)  # Google API最多返回10个结果
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # 提取搜索结果
            results = []
            if "items" in data:
                for item in data["items"][:num_results]:
                    title = item.get("title", "")
                    snippet = item.get("snippet", "")
                    link = item.get("link", "")
                    results.append(f"标题: {title}\n摘要: {snippet}\n链接: {link}\n")
            
            return "\n".join(results) if results else "未找到相关搜索结果。"
        except Exception as e:
            return f"搜索出错: {str(e)}"
    
    def duckduckgo_search(self, query: str, num_results: int = 5) -> str:
        """
        使用DuckDuckGo进行搜索（免费，无需API密钥）
        注意：DuckDuckGo可能在某些地区被限制
        """
        try:
            # 使用DuckDuckGo Instant Answer API
            url = "https://api.duckduckgo.com/"
            params = {
                "q": query,
                "format": "json",
                "no_html": "1",
                "skip_disambig": "1"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = []
            
            # 提取Abstract（摘要）
            if data.get("Abstract"):
                results.append(f"摘要: {data.get('Abstract')}\n来源: {data.get('AbstractURL', '')}\n")
            
            # 提取RelatedTopics（相关主题）
            if data.get("RelatedTopics"):
                for topic in data["RelatedTopics"][:num_results-1]:
                    if isinstance(topic, dict) and "Text" in topic:
                        results.append(f"相关: {topic.get('Text', '')}\n")
            
            return "\n".join(results) if results else "未找到相关搜索结果。"
        except Exception as e:
            return f"搜索出错: {str(e)}"
    
    def perform_search(self, query: str, search_api: str, search_api_key: str, 
                      google_cx: str, num_results: int) -> str:
        """
        执行网络搜索
        """
        if search_api == "serpapi":
            if not search_api_key:
                return "错误: 使用SerpAPI需要提供API密钥。请访问 https://serpapi.com/ 注册获取。"
            return self.google_search_serpapi(query, search_api_key, num_results)
        elif search_api == "google_custom":
            if not search_api_key or not google_cx:
                return "错误: 使用Google Custom Search需要提供API密钥和搜索引擎ID。"
            return self.google_search_custom(query, search_api_key, google_cx, num_results)
        elif search_api == "duckduckgo":
            return self.duckduckgo_search(query, num_results)
        else:
            return "错误: 未知的搜索引擎API。"
    
    def call_llm_api(
        self,
        base_url: str,
        api_key: str,
        model: str,
        prompt: str,
        system_prompt: str = "你是一个有用的AI助手。",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        top_p: float = 1.0,
        image=None,
        detail_level: str = "auto"
    ) -> Tuple[str, str, str]:
        """
        调用LLM API获取响应
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
            if image is not None:
                # 如果有图像，使用多模态格式
                user_content = []
                user_content.append({
                    "type": "text",
                    "text": prompt
                })
                try:
                    image_base64 = self.image_to_base64(image)
                    user_content.append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}",
                            "detail": detail_level
                        }
                    })
                    print(f"[LLM Web Search] 成功添加图像，base64长度: {len(image_base64)}")
                    messages.append({
                        "role": "user",
                        "content": user_content
                    })
                except Exception as e:
                    print(f"[LLM Web Search] 图像处理失败: {str(e)}")
                    # 如果图像处理失败，回退到纯文本
                    messages.append({
                        "role": "user",
                        "content": prompt
                    })
            else:
                # 纯文本消息
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
                "top_p": top_p
            }
            
            print(f"[LLM Web Search] 发送请求到: {url}")
            print(f"[LLM Web Search] 使用模型: {model}")
            
            # 发送请求
            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=60
            )
            
            print(f"[LLM Web Search] 响应状态码: {response.status_code}")
            
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
            result = response.json()
            full_response = json.dumps(result, ensure_ascii=False, indent=2)
            
            # 提取响应内容
            if "choices" in result and len(result["choices"]) > 0:
                response_text = result["choices"][0]["message"]["content"]
            else:
                response_text = "API未返回有效内容"
            
            # 提取使用信息
            usage_info = ""
            if "usage" in result:
                usage = result["usage"]
                usage_info = f"总tokens: {usage.get('total_tokens', 'N/A')}, "
                usage_info += f"输入tokens: {usage.get('prompt_tokens', 'N/A')}, "
                usage_info += f"输出tokens: {usage.get('completion_tokens', 'N/A')}"
            
            return (response_text, full_response, usage_info)
            
        except requests.exceptions.Timeout:
            raise Exception("API请求超时，请检查网络连接或稍后重试")
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求错误: {str(e)}")
        except Exception as e:
            raise Exception(f"调用LLM API时出错: {str(e)}")
    
    def call_llm_with_search(
        self,
        base_url: str,
        api_key: str,
        model: str,
        prompt: str,
        enable_search: bool,
        search_api: str,
        system_prompt: str = "你是一个有用的AI助手，能够根据搜索结果回答问题。",
        search_api_key: str = "",
        google_cx: str = "",
        num_results: int = 5,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        top_p: float = 1.0,
        image=None,
        detail_level: str = "auto"
    ) -> Tuple[str, str, str, str]:
        """
        执行网络搜索并调用LLM API
        """
        search_results = ""
        
        # 如果启用搜索，先执行搜索
        if enable_search:
            print(f"[LLM Web Search] 执行网络搜索: {prompt}")
            search_results = self.perform_search(
                prompt, 
                search_api, 
                search_api_key, 
                google_cx, 
                num_results
            )
            print(f"[LLM Web Search] 搜索结果:\n{search_results[:500]}...")
            
            # 将搜索结果整合到提示词中
            enhanced_prompt = f"""基于以下网络搜索结果，回答用户的问题：

搜索结果：
{search_results}

用户问题：{prompt}

请根据搜索结果提供准确、详细的回答。如果搜索结果中没有相关信息，请说明并基于你的知识回答。"""
        else:
            enhanced_prompt = prompt
        
        # 调用LLM API
        response_text, full_response, usage_info = self.call_llm_api(
            base_url=base_url,
            api_key=api_key,
            model=model,
            prompt=enhanced_prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            image=image,
            detail_level=detail_level
        )
        
        return (response_text, search_results, full_response, usage_info)


# 节点映射
NODE_CLASS_MAPPINGS = {
    "LLMWebSearchNode": LLMWebSearchNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LLMWebSearchNode": "LLM Web Search (XJ)"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

