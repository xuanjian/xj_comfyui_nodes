import requests
import base64
import io
from PIL import Image
import numpy as np
import torch
import json
import time

class WanxImageGenerationNode:
    """
    阿里云万相图像生成节点
    调用wanx模型进行AI绘画，支持文生图和图生图
    
    支持功能：
    - 文本生成图像
    - 参考图片生成（图生图）
    - 多种尺寸和风格
    - 负面提示词
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
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "一幅美丽的风景画",
                    "tooltip": "描述要生成的图像内容，支持中英文"
                }),
                "size": (["1:1", "4:3", "3:4", "16:9", "9:16", "3:2", "2:3", "21:9"], {
                    "default": "1:1",
                    "tooltip": "生成图像的尺寸比例"
                }),
                "api_baseurl": ("STRING", {
                    "default": "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis",
                    "tooltip": "API基础URL"
                }),
                "api_key": ("STRING", {
                    "default": "your-api-key-here",
                    "tooltip": "阿里云DashScope API密钥"
                }),
                "model": ("STRING", {
                    "default": "wanx-v1",
                    "tooltip": "模型名称，如：wanx-v1, wanx-style-repaint-v1"
                }),
            },
            "optional": {
                "image": ("IMAGE", {
                    "tooltip": "参考图片（可选），用于图生图"
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "generate_image"
    CATEGORY = "XJ_Nodes/Image"
    
    # 尺寸比例映射表（符合API要求：768*768到1440*1440之间）
    SIZE_MAP = {
        "1:1": "1280*1280",
        "4:3": "1280*960",
        "3:4": "960*1280",
        "16:9": "1280*720",
        "9:16": "720*1280",
        "3:2": "1200*800",
        "2:3": "800*1200",
        "21:9": "1344*576",
    }
    
    def tensor_to_base64(self, tensor_image):
        """
        将tensor图像转换为base64编码
        
        Args:
            tensor_image: 输入的tensor图像，形状为[B,H,W,C]或[H,W,C]
            
        Returns:
            str: base64编码的图像字符串
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
            
            # 转换为base64
            buffer = io.BytesIO()
            pil_image.save(buffer, format='PNG', quality=95, optimize=True)
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
    
    def download_image_from_url(self, image_url):
        """
        从URL下载图片并转换为base64字符串
        
        Args:
            image_url: 图片URL
            
        Returns:
            base64编码的图像字符串
        """
        try:
            response = requests.get(image_url, timeout=60)
            response.raise_for_status()
            
            # 将图片数据转换为base64
            image_base64 = base64.b64encode(response.content).decode('utf-8')
            return image_base64
            
        except Exception as e:
            raise Exception(f"下载图片失败: {str(e)}")
    
    def call_wanx_api(self, prompt, api_key, api_baseurl, model="wanx-v1", size="1024*1024", 
                      reference_image_base64=None):
        """
        调用阿里云万相API生成图像
        
        Args:
            prompt (str): 图像描述
            api_key (str): API密钥
            api_baseurl (str): API基础URL
            model (str): 模型名称
            size (str): 图像尺寸
            reference_image_base64 (str): 参考图片的base64编码
            
        Returns:
            list: 生成的图像base64字符串列表
        """
        # 验证输入参数
        if not api_key or api_key == "your-api-key-here":
            raise Exception("请设置有效的API密钥")
        
        if not prompt.strip():
            raise Exception("提示词不能为空")
        
        # API端点
        url = api_baseurl
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "X-DashScope-Async": "enable"  # 启用异步模式
        }
        
        # 构建请求数据
        data = {
            "model": model,
            "input": {
                "prompt": prompt.strip()
            },
            "parameters": {
                "size": size,
                "n": 1
            }
        }
        
        # 添加参考图片
        if reference_image_base64:
            data["input"]["ref_img"] = f"data:image/png;base64,{reference_image_base64}"
        
        try:
            print(f"正在调用万相API: {model}")
            print(f"提示词: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
            if reference_image_base64:
                print(f"使用参考图片进行图生图")
            
            # 提交任务
            response = requests.post(url, json=data, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            # 检查是否成功提交任务
            if "output" in result and "task_id" in result["output"]:
                task_id = result["output"]["task_id"]
                print(f"任务已提交，任务ID: {task_id}")
                
                # 轮询任务状态
                return self.wait_for_task_completion(task_id, api_key)
            else:
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
    
    def wait_for_task_completion(self, task_id, api_key, max_wait_time=300, poll_interval=2):
        """
        等待任务完成
        
        Args:
            task_id (str): 任务ID
            api_key (str): API密钥
            max_wait_time (int): 最大等待时间（秒）
            poll_interval (int): 轮询间隔（秒）
            
        Returns:
            list: 生成的图像base64字符串列表
        """
        url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        start_time = time.time()
        
        while True:
            if time.time() - start_time > max_wait_time:
                raise Exception(f"任务超时，等待时间超过 {max_wait_time} 秒")
            
            try:
                response = requests.get(url, headers=headers, timeout=30)
                response.raise_for_status()
                
                result = response.json()
                
                # 检查任务状态
                if "output" in result:
                    task_status = result["output"].get("task_status", "")
                    
                    if task_status == "SUCCEEDED":
                        print("任务完成！")
                        # 获取生成的图像
                        results = result["output"].get("results", [])
                        if not results:
                            raise Exception("未找到生成的图像")
                        
                        # 下载所有图像
                        image_base64_list = []
                        for i, item in enumerate(results):
                            image_url = item.get("url")
                            if image_url:
                                print(f"正在下载第 {i+1}/{len(results)} 张图片...")
                                img_base64 = self.download_image_from_url(image_url)
                                image_base64_list.append(img_base64)
                        
                        return image_base64_list
                    
                    elif task_status == "FAILED":
                        error_msg = result["output"].get("message", "任务失败")
                        raise Exception(f"任务失败: {error_msg}")
                    
                    elif task_status in ["PENDING", "RUNNING"]:
                        print(f"任务进行中... (状态: {task_status})")
                        time.sleep(poll_interval)
                    
                    else:
                        raise Exception(f"未知任务状态: {task_status}")
                
                else:
                    # 检查错误信息
                    if "code" in result:
                        error_msg = result.get("message", "未知错误")
                        raise Exception(f"API返回错误 {result['code']}: {error_msg}")
                    
                    raise Exception(f"API响应格式异常: {json.dumps(result, ensure_ascii=False)[:200]}")
            
            except requests.exceptions.RequestException as e:
                raise Exception(f"查询任务状态失败: {str(e)}")
    
    def generate_image(self, prompt, size, api_baseurl, api_key, model, image=None):
        """
        生成图像的主函数
        
        Args:
            prompt (str): 图像描述
            size (str): 图像尺寸比例
            api_baseurl (str): API基础URL
            api_key (str): API密钥
            model (str): 模型名称
            image (torch.Tensor): 参考图片（可选）
            
        Returns:
            tuple: 包含生成图像tensor的元组
        """
        try:
            print(f"开始图像生成任务...")
            print(f"提示词: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
            
            # 验证API密钥
            if not api_key or api_key == "your-api-key-here":
                raise Exception("请设置有效的API密钥")
            
            # 验证提示词
            if not prompt.strip():
                raise Exception("提示词不能为空")
            
            # 转换尺寸比例为实际像素尺寸
            actual_size = self.SIZE_MAP.get(size, "1280*1280")
            print(f"图像尺寸: {size} -> {actual_size}")
            
            # 处理参考图片
            reference_image_base64 = None
            if image is not None:
                print("正在处理参考图片...")
                reference_image_base64 = self.tensor_to_base64(image)
            
            # 调用API生成图像
            print(f"正在调用万相API生成图像...")
            result_base64_list = self.call_wanx_api(
                prompt=prompt.strip(),
                api_key=api_key,
                api_baseurl=api_baseurl,
                model=model,
                size=actual_size,
                reference_image_base64=reference_image_base64
            )
            
            # 将所有结果转换为tensor
            print(f"正在转换结果图像... (共 {len(result_base64_list)} 张)")
            result_tensors = []
            for i, base64_str in enumerate(result_base64_list):
                tensor = self.base64_to_tensor(base64_str)
                result_tensors.append(tensor)
                print(f"  图片 {i+1}/{len(result_base64_list)}: {tensor.shape}")
            
            # 合并所有tensor
            if len(result_tensors) == 1:
                final_tensor = result_tensors[0]
            else:
                final_tensor = torch.cat(result_tensors, dim=0)
            
            print(f"图像生成完成！最终输出尺寸: {final_tensor.shape}")
            return (final_tensor,)
            
        except Exception as e:
            error_msg = f"图像生成失败: {str(e)}"
            print(error_msg)
            raise Exception(error_msg)


# 节点映射
NODE_CLASS_MAPPINGS = {
    "WanxImageGenerationNode": WanxImageGenerationNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WanxImageGenerationNode": "万相图像生成"
}

