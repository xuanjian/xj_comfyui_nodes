import json
import os
from typing import Dict, Any, Tuple

class LLMConfigNode:
    """
    LLM配置节点
    用于管理和存储LLM API的配置信息
    支持多个预设配置，方便快速切换不同的API服务
    """
    
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__), "llm_configs.json")
        self.load_configs()
    
    def load_configs(self):
        """
        加载配置文件
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.configs = json.load(f)
            else:
                # 默认配置
                self.configs = {
                    "OpenAI": {
                        "base_url": "https://api.openai.com/v1",
                        "model": "gpt-3.5-turbo",
                        "description": "OpenAI官方API"
                    },
                    "阿里云通义千问": {
                        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
                        "model": "qwen-turbo",
                        "description": "阿里云通义千问API"
                    },
                    "智谱GLM": {
                        "base_url": "https://open.bigmodel.cn/api/paas/v4",
                        "model": "glm-4",
                        "description": "智谱GLM API"
                    },
                    "百度文心一言": {
                        "base_url": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop",
                        "model": "ernie-bot-turbo",
                        "description": "百度文心一言API"
                    },
                    "DeepSeek": {
                        "base_url": "https://api.deepseek.com/v1",
                        "model": "deepseek-chat",
                        "description": "DeepSeek API"
                    }
                }
                self.save_configs()
        except Exception as e:
            print(f"[LLM Config] 加载配置失败: {str(e)}")
            self.configs = {}
    
    def save_configs(self):
        """
        保存配置文件
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.configs, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[LLM Config] 保存配置失败: {str(e)}")
    
    @classmethod
    def INPUT_TYPES(cls):
        """
        定义节点的输入类型
        """
        # 创建临时实例来获取配置列表
        temp_instance = cls()
        config_names = list(temp_instance.configs.keys()) if temp_instance.configs else ["OpenAI"]
        
        return {
            "required": {
                "config_preset": (config_names, {
                    "default": config_names[0] if config_names else "OpenAI",
                    "tooltip": "选择预设配置"
                }),
                "api_key": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "tooltip": "API密钥"
                }),
            },
            "optional": {
                "custom_base_url": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "tooltip": "自定义base_url（留空使用预设）"
                }),
                "custom_model": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "tooltip": "自定义模型名称（留空使用预设）"
                }),
                "save_as_new_preset": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "tooltip": "保存为新预设的名称（留空不保存）"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("base_url", "api_key", "model", "config_info")
    FUNCTION = "get_config"
    CATEGORY = "XJ Nodes/LLM"
    
    def get_config(
        self,
        config_preset: str,
        api_key: str,
        custom_base_url: str = "",
        custom_model: str = "",
        save_as_new_preset: str = ""
    ) -> Tuple[str, str, str, str]:
        """
        获取LLM配置信息
        
        Args:
            config_preset: 预设配置名称
            api_key: API密钥
            custom_base_url: 自定义base_url
            custom_model: 自定义模型名称
            save_as_new_preset: 保存为新预设的名称
            
        Returns:
            Tuple[str, str, str, str]: (base_url, api_key, model, config_info)
        """
        try:
            # 重新加载配置以获取最新数据
            self.load_configs()
            
            # 获取预设配置
            if config_preset in self.configs:
                preset_config = self.configs[config_preset]
                base_url = custom_base_url if custom_base_url.strip() else preset_config.get("base_url", "")
                model = custom_model if custom_model.strip() else preset_config.get("model", "")
                description = preset_config.get("description", "")
            else:
                # 如果预设不存在，使用自定义值或默认值
                base_url = custom_base_url if custom_base_url.strip() else "https://api.openai.com/v1"
                model = custom_model if custom_model.strip() else "gpt-3.5-turbo"
                description = "自定义配置"
            
            # 验证必要参数
            if not api_key.strip():
                raise ValueError("API密钥不能为空")
            
            if not base_url.strip():
                raise ValueError("base_url不能为空")
            
            if not model.strip():
                raise ValueError("模型名称不能为空")
            
            # 保存为新预设
            if save_as_new_preset.strip():
                new_preset_name = save_as_new_preset.strip()
                self.configs[new_preset_name] = {
                    "base_url": base_url,
                    "model": model,
                    "description": f"用户自定义配置 - {new_preset_name}"
                }
                self.save_configs()
                print(f"[LLM Config] 已保存新预设: {new_preset_name}")
            
            # 构建配置信息
            config_info = f"配置: {config_preset}\n描述: {description}\nURL: {base_url}\n模型: {model}"
            
            print(f"[LLM Config] 使用配置: {config_preset}")
            print(f"[LLM Config] Base URL: {base_url}")
            print(f"[LLM Config] Model: {model}")
            
            return (base_url, api_key, model, config_info)
            
        except Exception as e:
            error_msg = f"获取配置时发生错误: {str(e)}"
            print(f"[LLM Config] 错误: {error_msg}")
            return ("", "", "", error_msg)

class LLMConfigManagerNode:
    """
    LLM配置管理节点
    用于管理预设配置，包括添加、删除、编辑配置
    """
    
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__), "llm_configs.json")
    
    @classmethod
    def INPUT_TYPES(cls):
        """
        定义节点的输入类型
        """
        return {
            "required": {
                "action": (["添加配置", "删除配置", "查看所有配置"], {
                    "default": "查看所有配置",
                    "tooltip": "选择操作类型"
                }),
            },
            "optional": {
                "preset_name": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "tooltip": "预设名称（添加/删除时使用）"
                }),
                "base_url": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "tooltip": "API基础URL（添加时使用）"
                }),
                "model": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "tooltip": "默认模型名称（添加时使用）"
                }),
                "description": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "tooltip": "配置描述（添加时使用）"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("result",)
    FUNCTION = "manage_config"
    CATEGORY = "XJ Nodes/LLM"
    
    def load_configs(self):
        """
        加载配置文件
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {}
        except Exception as e:
            print(f"[LLM Config Manager] 加载配置失败: {str(e)}")
            return {}
    
    def save_configs(self, configs):
        """
        保存配置文件
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(configs, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"[LLM Config Manager] 保存配置失败: {str(e)}")
            return False
    
    def manage_config(
        self,
        action: str,
        preset_name: str = "",
        base_url: str = "",
        model: str = "",
        description: str = ""
    ) -> Tuple[str]:
        """
        管理LLM配置
        
        Args:
            action: 操作类型
            preset_name: 预设名称
            base_url: API基础URL
            model: 模型名称
            description: 配置描述
            
        Returns:
            Tuple[str]: (操作结果)
        """
        try:
            configs = self.load_configs()
            
            if action == "查看所有配置":
                if not configs:
                    return ("暂无配置",)
                
                result = "当前所有配置:\n\n"
                for name, config in configs.items():
                    result += f"名称: {name}\n"
                    result += f"URL: {config.get('base_url', 'N/A')}\n"
                    result += f"模型: {config.get('model', 'N/A')}\n"
                    result += f"描述: {config.get('description', 'N/A')}\n"
                    result += "-" * 40 + "\n"
                
                return (result,)
            
            elif action == "添加配置":
                if not preset_name.strip():
                    return ("错误: 预设名称不能为空",)
                
                if not base_url.strip():
                    return ("错误: base_url不能为空",)
                
                if not model.strip():
                    return ("错误: 模型名称不能为空",)
                
                configs[preset_name.strip()] = {
                    "base_url": base_url.strip(),
                    "model": model.strip(),
                    "description": description.strip() if description.strip() else f"用户添加的配置 - {preset_name}"
                }
                
                if self.save_configs(configs):
                    return (f"成功添加配置: {preset_name}",)
                else:
                    return ("保存配置失败",)
            
            elif action == "删除配置":
                if not preset_name.strip():
                    return ("错误: 预设名称不能为空",)
                
                if preset_name.strip() not in configs:
                    return (f"错误: 配置 '{preset_name}' 不存在",)
                
                del configs[preset_name.strip()]
                
                if self.save_configs(configs):
                    return (f"成功删除配置: {preset_name}",)
                else:
                    return ("保存配置失败",)
            
            else:
                return (f"未知操作: {action}",)
            
        except Exception as e:
            error_msg = f"管理配置时发生错误: {str(e)}"
            print(f"[LLM Config Manager] 错误: {error_msg}")
            return (error_msg,)

# 节点映射
NODE_CLASS_MAPPINGS = {
    "LLMConfigNode": LLMConfigNode,
    "LLMConfigManagerNode": LLMConfigManagerNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LLMConfigNode": "LLM配置",
    "LLMConfigManagerNode": "LLM配置管理"
}