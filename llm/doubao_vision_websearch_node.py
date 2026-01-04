"""
火山引擎多模态图片理解 + 联网搜索节点
基于火山引擎 API 实现的图片理解和联网搜索功能

API 文档:
- 豆包大模型1.8(最新): https://www.volcengine.com/docs/82379/2123228
- 图片理解: https://www.volcengine.com/docs/82379/1362931
- 联网搜索: https://www.volcengine.com/docs/82379/1756990
- 豆包助手参考: https://www.volcengine.com/docs/82379/1978533
"""

import torch
import numpy as np
from PIL import Image
import requests
import json
import base64
import os
import io


class DoubaoVisionWebSearchNode:
    """
    火山引擎多模态图片理解 + 联网搜索节点
    支持图片理解和可选的联网搜索功能
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_text": ("STRING", {
                    "multiline": True,
                    "default": "请描述这张图片"
                }),
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": os.getenv("ARK_API_KEY", "")
                }),
                "model": ("STRING", {
                    "multiline": False,
                    "default": "ep-20250208104337-4wr54"  # 通用模型 endpoint（从控制台获取）
                    # 推荐使用的 Endpoint ID（从控制台获取）：
                    # - ep-20250208104337-4wr54（通用模型，推荐用于文本+搜索）
                    # 
                    # 如果支持视觉理解，可尝试：
                    # - doubao-seed-1.8（豆包1.8，可能支持视觉）
                    # - doubao-vision-pro（视觉专业版）
                    # - doubao-seed-1.6-thinking（1.6思考版，支持视觉）
                    # 
                    # 获取 Endpoint ID：
                    # 控制台：https://console.volcengine.com/ark/region:ark+cn-beijing/endpoint
                    # 
                    # ⚠️ 重要提示：
                    # - 通用模型（如 ep-20250208104337-4wr54）通常只支持文本，不支持图片输入
                    # - 如需图片理解，必须使用支持视觉的模型或 endpoint
                    # - 如果报错"llm model received multi-modal messages"，说明模型不支持图片
                }),
                "enable_websearch": ("BOOLEAN", {
                    "default": False
                }),
            },
            "optional": {
                "input_image": ("IMAGE",),
                "api_url": ("STRING", {
                    "multiline": False,
                    "default": "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
                }),
                "temperature": ("FLOAT", {
                    "default": 0.7,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1
                }),
                "max_tokens": ("INT", {
                    "default": 2048,
                    "min": 1,
                    "max": 32768
                }),
                "system_prompt": ("STRING", {
                    "multiline": True,
                    "default": "你是一个专业的图像分析助手，擅长识别和理解图片内容。请用清晰、准确的语言描述图片中的内容。"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("response", "search_results", "full_response")
    FUNCTION = "process"
    CATEGORY = "xj_nodes/llm"
    
    def encode_image_to_base64(self, image_tensor):
        """将 ComfyUI 的 Tensor 格式图片编码为 Base64 字符串"""
        try:
            # 处理批次维度
            if len(image_tensor.shape) == 4:
                image_tensor = image_tensor[0]
            
            # 转换为 PIL Image
            i = 255. * image_tensor.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            
            # 编码为 Base64
            byte_arr = io.BytesIO()
            img.save(byte_arr, format='PNG')
            byte_arr = byte_arr.getvalue()
            base64_bytes = base64.b64encode(byte_arr)
            base64_string = base64_bytes.decode('utf-8')
            
            return f"data:image/png;base64,{base64_string}"
        except Exception as e:
            print(f"❌ 图像编码失败: {e}")
            return None
    
    def process(self, input_text, api_key, model, enable_websearch,
                input_image=None, api_url="https://ark.cn-beijing.volces.com/api/v3/chat/completions",
                temperature=0.7, max_tokens=2048, system_prompt=""):
        """
        执行图片理解和联网搜索
        """
        # 验证 API Key
        if not api_key or api_key.strip() == "":
            error_msg = "❌ 错误: 请设置 API Key（环境变量 ARK_API_KEY 或在节点中输入）"
            print(error_msg)
            return (error_msg, "", "")
        
        # 验证和修复 API URL
        if not api_url or not (api_url.startswith("http://") or api_url.startswith("https://")):
            error_msg = "❌ 错误: API URL 无效"
            print(error_msg)
            return (error_msg, "", "")
        
        # 自动补全 URL（如果用户只输入了基础 URL）
        if api_url.endswith("/api/v3") or api_url.endswith("/api/v3/"):
            api_url = api_url.rstrip("/") + "/chat/completions"
            print(f"💡 已自动补全 API URL: {api_url}")
        elif not api_url.endswith("/chat/completions"):
            # 如果 URL 不完整，尝试补全
            if "/api/v3" in api_url:
                api_url = api_url.rstrip("/") + "/chat/completions"
                print(f"💡 已自动补全 API URL: {api_url}")
            else:
                error_msg = f"""❌ 错误: API URL 格式不正确

当前 URL: {api_url}

✅ 正确的 URL 格式应该是：
https://ark.cn-beijing.volces.com/api/v3/chat/completions

💡 提示：
- 如果只输入了基础 URL（如 https://ark.cn-beijing.volces.com/api/v3），
  节点会自动补全为完整路径
- 或者直接使用默认值（推荐）"""
                print(error_msg)
                return (error_msg, "", "")
        
        # 验证 Model/Endpoint ID
        if not model or model.strip() == "" or "请从控制台获取" in model or "请从" in model:
            error_msg = """❌ 错误: 请设置有效的模型名称或 Endpoint ID

💡 可以使用的格式：
1. 模型名称格式（推荐先尝试）：
   - doubao-seed-1.8（豆包1.8通用版）
   - doubao-vision-pro（视觉专业版）
   - doubao-seed-1.6-thinking（1.6思考版）

2. Endpoint ID 格式（如果模型名称不可用）：
   - ep-xxxxxxxxxxxxx（从控制台获取）
   - 控制台：https://console.volcengine.com/ark/region:ark+cn-beijing/endpoint

⚠️ 注意：
- 不同账户的可用模型列表可能不同
- 如果模型名称不可用，请从控制台获取你的 Endpoint ID"""
            print(error_msg)
            return (error_msg, "", "")
        
        # 提前检测：如果连接了图片但使用的是已知不支持视觉的模型
        known_text_only_models = [
            "ep-20250208104337-4wr54",  # 通用模型，不支持视觉
        ]
        
        if input_image is not None and model in known_text_only_models:
            error_msg = f"""❌ 模型不支持图片输入

📝 当前使用的模型: {model}
🖼️  检测到图片输入: 已连接

💡 原因：
当前模型是通用模型，只支持文本输入，不支持图片理解（多模态）。

💡 解决方法（二选一）：

方法1：使用支持视觉的模型（推荐）
1. 访问控制台：https://console.volcengine.com/ark/region:ark+cn-beijing/endpoint
2. 查找支持"视觉理解"或"多模态"的模型
3. 复制对应的 Endpoint ID（格式：ep-xxxxxxxxxxxxx）
4. 在节点的 'model' 参数中输入该 Endpoint ID

推荐尝试的模型名称（如果可用）：
- doubao-seed-1.6-thinking（支持视觉理解）
- doubao-vision-pro（视觉专业版）
- doubao-seed-1.8（可能支持，需验证）

方法2：不连接图片（纯文本模式）
- 断开 input_image 连接
- 只使用文本输入 + 联网搜索
- 当前模型 {model} 支持文本理解和联网搜索"""
            print(f"\n{error_msg}\n")
            return (error_msg, "", "")
        
        print(f"\n{'='*60}")
        print(f"🤖 火山引擎多模态理解 + 联网搜索")
        print(f"{'='*60}")
        print(f"📝 输入文本: {input_text[:100]}...")
        print(f"🔍 模型: {model}")
        print(f"🌐 联网搜索: {'启用' if enable_websearch else '禁用'}")
        if input_image is not None:
            print(f"🖼️  图片输入: 已提供")
        
        # 构建消息内容
        messages = []
        
        # 添加系统提示词
        if system_prompt and system_prompt.strip():
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        # 构建用户消息
        # 根据是否有图片，选择不同的 content 格式
        if input_image is not None:
            # 有图片时，使用多模态数组格式
            user_message = {
                "role": "user",
                "content": []
            }
            
            # 添加文本内容
            user_message["content"].append({
                "type": "text",
                "text": input_text
            })
            
            # 添加图片内容
            print(f"🔄 正在编码输入图像...")
            base64_image = self.encode_image_to_base64(input_image)
            
            if not base64_image:
                error_msg = "❌ 图像编码失败"
                print(error_msg)
                return (error_msg, "", "")
            
            user_message["content"].append({
                "type": "image_url",
                "image_url": {
                    "url": base64_image
                }
            })
        else:
            # 纯文本时，使用字符串格式
            user_message = {
                "role": "user",
                "content": input_text
            }
        
        messages.append(user_message)
        
        # 构建请求头
        # 处理 API Key：如果已经包含 "Bearer " 前缀，直接使用；否则添加前缀
        auth_key = api_key.strip()
        if not auth_key.startswith("Bearer "):
            auth_key = f"Bearer {auth_key}"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": auth_key
        }
        
        # 构建请求体
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        # 添加联网搜索工具（如果启用）
        # 根据官方示例：https://www.volcengine.com/docs/82379/1338552
        # 使用正确的工具格式：{"type": "web_search", "web_search": {}}
        if enable_websearch:
            payload["tools"] = [
                {
                    "type": "web_search",  # 固定值，指定联网搜索工具
                    "web_search": {}  # 无额外配置，空字典即可
                }
            ]
            payload["tool_choice"] = "auto"  # 模型自动判断是否需要联网
            print(f"✨ 已启用联网搜索工具")
        
        # 发送请求
        try:
            print(f"📤 正在发送请求到 API...")
            import time
            start_time = time.time()
            
            response = requests.post(
                api_url,
                headers=headers,
                data=json.dumps(payload),
                timeout=180
            )
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            print(f"⏱️  API 响应状态码: {response.status_code}, 耗时: {elapsed_time:.2f}秒")
            
            response.raise_for_status()
            result = response.json()
            
            # 解析结果
            if "choices" in result and len(result["choices"]) > 0:
                choice = result["choices"][0]
                message = choice.get("message", {})
                content = message.get("content", "")
                
                # 提取搜索结果（如果有）
                search_results = ""
                if "tool_calls" in message:
                    tool_calls = message["tool_calls"]
                    search_info = []
                    for tool_call in tool_calls:
                        if tool_call.get("type") == "web_search":
                            function = tool_call.get("function", {})
                            arguments = function.get("arguments", "{}")
                            try:
                                args_dict = json.loads(arguments)
                                search_info.append(json.dumps(args_dict, indent=2, ensure_ascii=False))
                            except:
                                search_info.append(arguments)
                    
                    if search_info:
                        search_results = "\n\n".join(search_info)
                        print(f"🔍 搜索结果已提取")
                
                # 使用信息
                usage = result.get("usage", {})
                usage_info = f"输入tokens: {usage.get('prompt_tokens', 0)}, 输出tokens: {usage.get('completion_tokens', 0)}, 总计: {usage.get('total_tokens', 0)}"
                
                info_msg = f"✅ 处理成功，耗时 {elapsed_time:.2f}秒\n{usage_info}"
                print(f"\n{info_msg}")
                print(f"{'='*60}\n")
                
                # 返回结果
                full_response = json.dumps(result, indent=2, ensure_ascii=False)
                return (content, search_results, full_response)
            else:
                error_msg = f"❌ API 返回数据异常: {json.dumps(result, ensure_ascii=False)}"
                print(error_msg)
                return (error_msg, "", json.dumps(result, indent=2, ensure_ascii=False))
        
        except requests.exceptions.RequestException as e:
            error_msg = f"❌ API 请求失败: {str(e)}"
            print(f"\n{error_msg}")
            
            if hasattr(e, 'response') and e.response is not None:
                status_code = e.response.status_code
                print(f"状态码: {status_code}")
                
                # 特殊处理 404 错误（URL 不正确）
                if status_code == 404:
                    print(f"\n{'='*60}")
                    print(f"⚠️  API 地址未找到 (404)")
                    print(f"{'='*60}")
                    print(f"❌ 请求的 URL: {api_url}")
                    print(f"\n💡 可能的原因：")
                    print(f"1. API URL 不完整（缺少 /chat/completions 路径）")
                    print(f"2. API URL 格式错误")
                    print(f"\n💡 解决方法：")
                    print(f"1. 使用默认的 API URL（推荐）：")
                    print(f"   https://ark.cn-beijing.volces.com/api/v3/chat/completions")
                    print(f"\n2. 或者确保 URL 以 /chat/completions 结尾")
                    print(f"\n3. 检查节点中的 'api_url' 参数是否正确")
                    print(f"{'='*60}\n")
                    
                    error_msg = f"""❌ API 地址未找到 (404)

请求的 URL: {api_url}

💡 解决方法：
1. 使用默认的 API URL（推荐）：
   https://ark.cn-beijing.volces.com/api/v3/chat/completions

2. 确保 URL 以 /chat/completions 结尾

3. 如果只输入了基础 URL，节点会自动补全"""
                    
                    print(f"{'='*60}\n")
                    return (error_msg, "", "")
                
                try:
                    error_detail = e.response.json()
                    error_code = error_detail.get("error", {}).get("code", "")
                    error_message = error_detail.get("error", {}).get("message", "")
                    
                    # 特殊处理多模态错误
                    if "multi-modal" in error_message.lower() or "multimodal" in error_message.lower():
                        print(f"\n{'='*60}")
                        print(f"⚠️  多模态输入错误")
                        print(f"{'='*60}")
                        print(f"❌ 错误信息: {error_message}")
                        print(f"📝 当前使用的模型: {model}")
                        print(f"\n💡 原因：")
                        print(f"  当前模型不支持图片输入（多模态），只支持纯文本")
                        print(f"\n💡 解决方法：")
                        print(f"1. 使用支持图片理解的模型（推荐）：")
                        print(f"   - doubao-seed-1.6-thinking（支持视觉理解）")
                        print(f"   - doubao-vision-pro（视觉专业版）")
                        print(f"   - doubao-seed-1.8（可能支持，需验证）")
                        print(f"\n2. 或者不连接图片输入（纯文本模式）")
                        print(f"\n3. 实现图片理解+联网搜索：")
                        print(f"   - 使用支持视觉的模型")
                        print(f"   - 连接图片到 input_image")
                        print(f"   - 启用 enable_websearch")
                        print(f"   - 在提示词中要求搜索相关信息")
                        print(f"{'='*60}\n")
                        
                        error_msg = f"❌ 多模态输入错误: {error_message}\n\n"
                        error_msg += f"📝 当前使用的模型: {model}\n\n"
                        error_msg += "💡 原因：当前模型不支持图片输入\n\n"
                        error_msg += "💡 解决方法：\n"
                        error_msg += "1. 使用支持图片理解的模型：\n"
                        error_msg += "   - doubao-seed-1.6-thinking\n"
                        error_msg += "   - doubao-vision-pro\n\n"
                        error_msg += "2. 或者不连接图片（纯文本模式）"
                    
                    # 特殊处理模型不存在错误
                    elif "InvalidEndpointOrModel.NotFound" in error_code or "NotFound" in error_code:
                        print(f"\n{'='*60}")
                        print(f"⚠️  模型或 Endpoint 不存在错误")
                        print(f"{'='*60}")
                        print(f"❌ 错误信息: {error_message}")
                        print(f"📝 当前使用的模型: {model}")
                        
                        # 检查模型名称格式，提供修正建议
                        format_suggestions = []
                        if "1-8" in model or "1_8" in model:
                            format_suggestions.append("• 模型名称格式错误：使用了横线或下划线")
                            format_suggestions.append("• 正确格式应该是：doubao-seed-1.8（使用点号，不是横线）")
                            format_suggestions.append("• 请尝试：doubao-seed-1.8")
                        elif not model.startswith("ep-") and not model.startswith("doubao-"):
                            format_suggestions.append("• 模型名称格式可能不正确")
                            format_suggestions.append("• 正确格式：doubao-seed-1.8 或 ep-xxxxxxxxxxxxx")
                        
                        print(f"\n💡 解决方法:")
                        if format_suggestions:
                            print(f"\n📌 模型名称格式建议:")
                            for suggestion in format_suggestions:
                                print(f"  {suggestion}")
                            print(f"\n")
                        
                        print(f"1. 尝试使用正确的模型名称格式:")
                        print(f"   - doubao-seed-1.8（豆包1.8通用版，推荐）")
                        print(f"   - doubao-vision-pro（视觉专业版）")
                        print(f"   - doubao-seed-1.6-thinking（1.6思考版）")
                        print(f"\n2. 如果模型名称都不可用，使用 Endpoint ID:")
                        print(f"   - 访问控制台: https://console.volcengine.com/ark/region:ark+cn-beijing/endpoint")
                        print(f"   - 查看'推理接入点'列表")
                        print(f"   - 复制你的 endpoint ID（格式: ep-xxxxxxxxxxxxx）")
                        print(f"   - 在节点的 'model' 参数中输入该 endpoint ID")
                        print(f"\n3. 注意：不同账户的可用模型列表可能不同")
                        print(f"{'='*60}\n")
                        
                        # 构建错误消息
                        error_msg = f"❌ 模型不存在: {error_message}\n\n📝 当前使用的模型: {model}\n\n"
                        if format_suggestions:
                            error_msg += "📌 模型名称格式建议:\n"
                            for suggestion in format_suggestions:
                                error_msg += f"{suggestion}\n"
                            error_msg += "\n"
                        error_msg += "💡 解决方法:\n"
                        error_msg += "1. 尝试使用正确的模型名称:\n"
                        error_msg += "   - doubao-seed-1.8（推荐）\n"
                        error_msg += "   - doubao-vision-pro\n"
                        error_msg += "   - doubao-seed-1.6-thinking\n\n"
                        error_msg += "2. 如果都不可用，从控制台获取 Endpoint ID:\n"
                        error_msg += "   https://console.volcengine.com/ark/region:ark+cn-beijing/endpoint"
                    else:
                        print(f"错误详情: {json.dumps(error_detail, indent=2, ensure_ascii=False)}")
                        error_msg += f"\n{json.dumps(error_detail, ensure_ascii=False)}"
                except:
                    print(f"响应内容: {e.response.text}")
                    error_msg += f"\n{e.response.text}"
            
            print(f"{'='*60}\n")
            return (error_msg, "", "")
        
        except Exception as e:
            error_msg = f"❌ 未知错误: {str(e)}"
            print(f"\n{error_msg}")
            print(f"{'='*60}\n")
            return (error_msg, "", "")


# 节点注册
NODE_CLASS_MAPPINGS = {
    "DoubaoVisionWebSearchNode": DoubaoVisionWebSearchNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DoubaoVisionWebSearchNode": "豆包视觉+搜索 (XJ)"
}
