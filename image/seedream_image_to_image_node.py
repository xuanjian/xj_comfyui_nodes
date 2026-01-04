"""
Seedream 4.5 图生图节点
基于火山引擎 API 实现的 doubao-seedream-4.5 图生图功能
API 文档: https://www.volcengine.com/docs/82379/1541523
"""

import torch
import numpy as np
from PIL import Image
import requests
import json
import base64
import time
import os
import io


class SeedreamImageToImageNode:
    """
    Seedream 4.5 图生图节点
    支持将输入图像通过 AI 进行风格转换、内容编辑等图生图操作
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),  # 输入图像
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "描述你想要生成的图像内容"
                }),
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": os.getenv("ARK_API_KEY", "")
                }),
                "model": ([
                    "doubao-seedream-4.5",
                    "doubao-seedream-4-5-251128",
                    "doubao-seedream-4.0",
                    "doubao-seedream-4-0-250828"
                ], {
                    "default": "doubao-seedream-4.5"
                }),
                "strength": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                    "display": "slider"
                }),
                "size": ([
                    "auto",
                    "1:1",
                    "1:2",
                    "2:1",
                    "4:5",
                    "5:4",
                    "16:9",
                    "9:16"
                ], {
                    "default": "auto"
                }),
                "seed": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 2147483647
                }),
                "watermark": ("BOOLEAN", {
                    "default": False
                }),
            },
            "optional": {
                "api_url": ("STRING", {
                    "multiline": False,
                    "default": "https://ark.cn-beijing.volces.com/api/v3/images/generations"
                }),
                "optimize_prompt_mode": ([
                    "disabled",
                    "standard",
                    "fast"
                ], {
                    "default": "disabled"
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("image", "info")
    FUNCTION = "generate"
    CATEGORY = "xj_nodes/image"
    
    def encode_image_to_base64(self, image_tensor):
        """将 ComfyUI 的 Tensor 格式图片编码为 Base64 字符串"""
        try:
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
    
    def decode_base64_to_tensor(self, base64_string):
        """将 Base64 字符串解码为 ComfyUI 的 Tensor 格式"""
        try:
            # 移除 data URI 前缀
            if ',' in base64_string:
                base64_string = base64_string.split(',', 1)[1]
            
            # 解码 Base64
            img_data = base64.b64decode(base64_string)
            img = Image.open(io.BytesIO(img_data)).convert("RGB")
            
            # 转换为 Tensor
            np_image = np.array(img).astype(np.float32) / 255.0
            tensor = torch.from_numpy(np_image)[None,]
            
            return tensor
        except Exception as e:
            print(f"❌ 图像解码失败: {e}")
            return None
    
    def download_image_from_url(self, url):
        """从 URL 下载图片并转换为 Tensor"""
        try:
            print(f"📥 正在下载图片: {url[:80]}...")
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            
            img = Image.open(io.BytesIO(response.content)).convert("RGB")
            np_image = np.array(img).astype(np.float32) / 255.0
            tensor = torch.from_numpy(np_image)[None,]
            
            return tensor
        except Exception as e:
            print(f"❌ 图片下载失败: {e}")
            return None
    
    def convert_aspect_ratio_to_size(self, aspect_ratio):
        """
        将宽高比转换为具体的像素尺寸
        返回格式: "WIDTHxHEIGHT"
        """
        aspect_ratio_map = {
            "1:1": "1024x1024",
            "1:2": "1024x2048",      # 竖版
            "2:1": "2048x1024",      # 横版
            "4:5": "1024x1280",      # 竖版
            "5:4": "1280x1024",      # 横版
            "16:9": "1920x1080",     # 横版
            "9:16": "1080x1920"      # 竖版
        }
        
        return aspect_ratio_map.get(aspect_ratio, aspect_ratio)
    
    def generate(self, image, prompt, api_key, model, strength, size, seed, watermark,
                 api_url="https://ark.cn-beijing.volces.com/api/v3/images/generations",
                 optimize_prompt_mode="disabled"):
        """
        执行图生图生成
        """
        # 验证 API Key
        if not api_key or api_key.strip() == "":
            error_msg = "❌ 错误: 请设置 API Key（环境变量 ARK_API_KEY 或在节点中输入）"
            print(error_msg)
            return (image, error_msg)
        
        # 验证 API URL
        if not api_url or not (api_url.startswith("http://") or api_url.startswith("https://")):
            error_msg = "❌ 错误: API URL 无效"
            print(error_msg)
            return (image, error_msg)
        
        print(f"\n{'='*60}")
        print(f"🎨 Seedream 图生图开始")
        print(f"{'='*60}")
        print(f"📝 Prompt: {prompt[:100]}...")
        print(f"🤖 Model: {model}")
        print(f"💪 Strength: {strength}")
        print(f"📐 Size: {size}")
        print(f"🎲 Seed: {seed}")
        
        # 处理输入图像
        # image 的 shape 是 [batch, height, width, channels]
        if len(image.shape) == 4:
            # 批量处理，取第一张图
            input_image = image[0]
        else:
            input_image = image
        
        # 编码图像为 Base64
        print(f"🔄 正在编码输入图像...")
        base64_image = self.encode_image_to_base64(input_image)
        
        if not base64_image:
            error_msg = "❌ 图像编码失败"
            print(error_msg)
            return (image, error_msg)
        
        # 构建请求
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        payload = {
            "model": model,
            "prompt": prompt,
            "image": base64_image,
            "strength": strength,
            "response_format": "b64_json",
            "watermark": watermark
        }
        
        # 添加可选参数
        if seed != -1:
            payload["seed"] = seed
        
        if size != "auto":
            # 如果是宽高比格式，转换为像素尺寸
            if ":" in size:
                actual_size = self.convert_aspect_ratio_to_size(size)
                print(f"📐 宽高比 {size} 转换为像素尺寸: {actual_size}")
                payload["size"] = actual_size
            else:
                payload["size"] = size
        
        # 提示词优化（仅 4.5 支持）
        if optimize_prompt_mode != "disabled" and "4.5" in model or "4-5" in model:
            payload["optimize_prompt_options"] = {
                "mode": optimize_prompt_mode
            }
            print(f"✨ 提示词优化模式: {optimize_prompt_mode}")
        
        # 发送请求
        try:
            print(f"📤 正在发送请求到 API...")
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
            if "data" in result and len(result["data"]) > 0:
                generated_images = []
                
                for idx, item in enumerate(result["data"]):
                    print(f"🖼️  处理第 {idx + 1} 张生成的图片...")
                    
                    # 优先使用 b64_json
                    if "b64_json" in item and item["b64_json"]:
                        tensor = self.decode_base64_to_tensor(item["b64_json"])
                        if tensor is not None:
                            generated_images.append(tensor)
                    # 其次使用 URL
                    elif "url" in item and item["url"]:
                        tensor = self.download_image_from_url(item["url"])
                        if tensor is not None:
                            generated_images.append(tensor)
                
                if generated_images:
                    # 合并所有生成的图片
                    output_batch = torch.cat(generated_images, dim=0)
                    
                    info_msg = f"✅ 成功生成 {len(generated_images)} 张图片，耗时 {elapsed_time:.2f}秒"
                    print(f"\n{info_msg}")
                    print(f"{'='*60}\n")
                    
                    return (output_batch, info_msg)
                else:
                    error_msg = "❌ 无法处理 API 返回的图片数据"
                    print(error_msg)
                    return (image, error_msg)
            else:
                error_msg = f"❌ API 返回数据异常: {json.dumps(result, ensure_ascii=False)}"
                print(error_msg)
                return (image, error_msg)
        
        except requests.exceptions.RequestException as e:
            error_msg = f"❌ API 请求失败: {str(e)}"
            print(f"\n{error_msg}")
            
            if hasattr(e, 'response') and e.response is not None:
                print(f"状态码: {e.response.status_code}")
                try:
                    error_detail = e.response.json()
                    print(f"错误详情: {json.dumps(error_detail, indent=2, ensure_ascii=False)}")
                    error_msg += f"\n{json.dumps(error_detail, ensure_ascii=False)}"
                except:
                    print(f"响应内容: {e.response.text}")
                    error_msg += f"\n{e.response.text}"
            
            print(f"{'='*60}\n")
            return (image, error_msg)
        
        except Exception as e:
            error_msg = f"❌ 未知错误: {str(e)}"
            print(f"\n{error_msg}")
            print(f"{'='*60}\n")
            return (image, error_msg)


# 节点注册
NODE_CLASS_MAPPINGS = {
    "SeedreamImageToImageNode": SeedreamImageToImageNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SeedreamImageToImageNode": "Seedream 图生图 (XJ)"
}
