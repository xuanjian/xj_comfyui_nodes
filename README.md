# XJ Nodes - ComfyUI 自定义节点

一个为ComfyUI设计的自定义节点集合，包含数学运算、图像处理和大语言模型API调用节点。

## 节点功能

### 数学运算节点

#### 1. MaxNode - 最大值节点
- **功能**: 返回两个数字中的最大值
- **输入**: input1 (整数/浮点数), input2 (整数/浮点数)
- **输出**: max_value (最大值)
- **显示名**: "Max (XJ)"
- **分类**: "XJ Nodes/Math"

#### 2. MinNode - 最小值节点
- **功能**: 返回两个数字中的最小值
- **输入**: input1 (整数/浮点数), input2 (整数/浮点数)
- **输出**: min_value (最小值)
- **显示名**: "Min (XJ)"
- **分类**: "XJ Nodes/Math"

#### 3. AverageNode - 平均值节点
- **功能**: 返回两个数字的平均值
- **输入**: input1 (整数/浮点数), input2 (整数/浮点数)
- **输出**: average_value (平均值，浮点数)
- **显示名**: "Average (XJ)"
- **分类**: "XJ Nodes/Math"

#### 4. DifferenceNode - 差值节点
- **功能**: 返回两个数字的差值（绝对值）
- **输入**: input1 (整数/浮点数), input2 (整数/浮点数)
- **输出**: difference_value (差值)
- **显示名**: "Difference (XJ)"
- **分类**: "XJ Nodes/Math"

### 图像处理节点

#### 5. ImageUrlLoaderNode - 图片URL加载节点
- **功能**: 从URL地址加载图片
- **输入**: image_url (字符串，图片URL地址)
- **输出**: image (图片对象)
- **显示名**: "Image URL Loader (XJ)"
- **分类**: "XJ Nodes/Image"
- **特性**: 支持HTTP/HTTPS协议，自动转换图片格式为RGB，包含错误处理

#### 6. QwenImageEditNode - Qwen图像编辑节点
- **功能**: 调用阿里云百炼平台的Qwen图像编辑模型进行图像编辑
- **输入**:
  - image (图像，要编辑的图像)
  - edit_instruction (字符串，编辑指令)
  - api_key (字符串，阿里云百炼API密钥)
  - model_name (字符串，模型名称，可选)
  - negative_prompt (字符串，负面提示词，可选)
  - watermark (布尔值，是否添加水印，可选)
  - seed (整数，随机种子，可选)
- **输出**: edited_image (编辑后的图像)
- **显示名**: "Qwen图像编辑"
- **分类**: "XJ Nodes/Image"
- **支持功能**: 图像编辑、风格迁移、物体增删、文字编辑、细节增强

#### 7. WanxImageGenerationNode - 万相图像生成节点 ⭐新增
- **功能**: 调用阿里云万相API进行AI绘画，支持文生图和图生图
- **输入**:
  - prompt (字符串，图像描述)
  - api_key (字符串，阿里云DashScope API密钥)
  - reference_image (图像，参考图片，可选)
  - model (字符串，模型选择：wanx-v1/wanx-style-repaint-v1)
  - size (字符串，图像尺寸：1024*1024/720*1280/1280*720)
  - negative_prompt (字符串，负面提示词，可选)
  - n (整数，生成数量1-4，可选)
  - seed (整数，随机种子，可选)
  - ref_strength (浮点数，参考图片影响强度0-1，可选)
  - ref_mode (字符串，参考模式：repaint/refonly，可选)
- **输出**: images (生成的图像)
- **显示名**: "万相图像生成"
- **分类**: "XJ Nodes/Image"
- **支持功能**: 文本生成图像、参考图片生成、多种尺寸和风格、负面提示词、批量生成
- **详细文档**: [WANX_API_GUIDE.md](image/WANX_API_GUIDE.md)
- **使用示例**: [wanx_image_generation_example.md](examples/wanx_image_generation_example.md)

### 大语言模型节点

### 大语言模型节点

#### 8. LLMApiNode - LLM API调用节点
- **功能**: 调用OpenAI兼容的大语言模型API
- **输入**: 
  - base_url (字符串，API基础URL)
  - api_key (字符串，API密钥)
  - model (字符串，模型名称)
  - prompt (字符串，用户提示词)
  - system_prompt (字符串，系统提示词，可选)
  - temperature (浮点数，温度参数，可选)
  - max_tokens (整数，最大token数，可选)
  - top_p (浮点数，top_p参数，可选)
  - stream (布尔值，是否流式输出，可选)
- **输出**: 
  - response (字符串，响应内容)
  - full_response (字符串，完整响应JSON)
  - usage_info (字符串，使用信息)
- **显示名**: "LLM API (XJ)"
- **分类**: "XJ Nodes/LLM"
- **支持的API**: OpenAI、阿里云通义千问、智谱GLM、百度文心一言、DeepSeek等

#### 9. LLMVisionNode - LLM视觉API调用节点
- **功能**: 调用支持图像输入的多模态大语言模型API
- **输入**: 
  - base_url (字符串，API基础URL)
  - api_key (字符串，API密钥)
  - model (字符串，视觉模型名称)
  - prompt (字符串，用户提示词)
  - image (图像，输入图像，可选)
  - system_prompt (字符串，系统提示词，可选)
  - temperature (浮点数，温度参数，可选)
  - max_tokens (整数，最大token数，可选)
  - detail_level (字符串，图像分析详细程度，可选)
- **输出**: 
  - response (字符串，响应内容)
  - full_response (字符串，完整响应JSON)
  - usage_info (字符串，使用信息)
- **显示名**: "LLM Vision (XJ)"
- **分类**: "XJ Nodes/LLM"
- **支持的模型**: GPT-4V、Qwen-VL、GLM-4V等

#### 10. LLMConfigNode - LLM配置节点
- **功能**: 管理LLM API配置，支持预设配置
- **输入**: 
  - config_preset (字符串，预设配置名称)
  - api_key (字符串，API密钥)
  - custom_base_url (字符串，自定义base_url，可选)
  - custom_model (字符串，自定义模型名称，可选)
  - save_as_new_preset (字符串，保存为新预设，可选)
- **输出**: 
  - base_url (字符串，API基础URL)
  - api_key (字符串，API密钥)
  - model (字符串，模型名称)
  - config_info (字符串，配置信息)
- **显示名**: "LLM Config (XJ)"
- **分类**: "XJ Nodes/LLM"
- **预设配置**: OpenAI、阿里云通义千问、智谱GLM、百度文心一言、DeepSeek

#### 11. LLMConfigManagerNode - LLM配置管理节点
- **功能**: 管理预设配置，包括添加、删除、查看配置
- **输入**: 
  - action (字符串，操作类型)
  - preset_name (字符串，预设名称，可选)
  - base_url (字符串，API基础URL，可选)
  - model (字符串，模型名称，可选)
  - description (字符串，配置描述，可选)
- **输出**: 
  - result (字符串，操作结果)
- **显示名**: "LLM Config Manager (XJ)"
- **分类**: "XJ Nodes/LLM"

#### 10. LLMWebSearchNode - LLM网络搜索节点
- **功能**: 支持在调用LLM之前先进行Google搜索，然后将搜索结果作为上下文提供给LLM。支持图像+文本+搜索的多模态查询
- **输入**: 
  - base_url (字符串，API基础URL)
  - api_key (字符串，API密钥)
  - model (字符串，模型名称)
  - prompt (字符串，用户提示词)
  - enable_search (布尔值，是否启用网络搜索)
  - search_api (字符串，搜索引擎API选择：serpapi/google_custom/duckduckgo)
  - image (图像，输入图像，可选) - **新增：支持图像输入**
  - system_prompt (字符串，系统提示词，可选)
  - search_api_key (字符串，搜索引擎API密钥，可选)
  - google_cx (字符串，Google Custom Search Engine ID，可选)
  - num_results (整数，搜索结果数量，1-10，默认5)
  - temperature (浮点数，温度参数，可选)
  - max_tokens (整数，最大token数，可选)
  - top_p (浮点数，top_p参数，可选)
  - detail_level (字符串，图像分析详细程度：low/high/auto，可选) - **新增：图像分析详细程度**
- **输出**: 
  - response (字符串，LLM响应内容)
  - search_results (字符串，搜索结果)
  - full_response (字符串，完整响应JSON)
  - usage_info (字符串，使用信息)
- **显示名**: "LLM Web Search (XJ)"
- **分类**: "XJ Nodes/LLM"
- **支持的搜索引擎**:
  - **SerpAPI**: 需要注册 https://serpapi.com/ 获取API密钥（推荐，稳定可靠）
  - **Google Custom Search**: 需要Google Cloud Console API密钥和自定义搜索引擎ID
  - **DuckDuckGo**: 免费，无需API密钥（可能在某些地区受限）
- **使用场景**:
  - 文本查询 + 网络搜索：查询最新信息并基于搜索结果回答
  - 图像 + 文本 + 网络搜索：分析图像内容，搜索相关信息，综合回答（需要支持视觉的模型，如GPT-4V、Qwen-VL等）

#### 使用方法

##### 数学运算节点使用
1. 在ComfyUI中找到 "XJ Nodes/Math" 分类
2. 根据需要选择对应的节点：
   - "Max (XJ)" - 最大值节点
   - "Min (XJ)" - 最小值节点
   - "Average (XJ)" - 平均值节点
   - "Difference (XJ)" - 差值节点
3. 设置两个输入数字
4. 连接输出到其他节点

##### 图像处理节点使用
1. 在ComfyUI中找到 "XJ Nodes/Image" 分类
2. 选择 "Image URL Loader (XJ)" 节点
3. 输入图片URL地址
4. 连接输出的图像到其他节点

##### LLM节点使用
1. 在ComfyUI中找到 "XJ Nodes/LLM" 分类
2. 首先使用 "LLM Config (XJ)" 节点配置API信息：
   - 选择预设配置或自定义配置
   - 输入API密钥
   - 可选择自定义base_url和模型名称
3. 使用 "LLM API (XJ)" 节点进行文本生成：
   - 连接配置节点的输出
   - 输入提示词
   - 调整生成参数（可选）
4. 使用 "LLM Vision (XJ)" 节点进行图像分析：
   - 连接配置节点的输出
   - 连接图像输入
   - 输入分析提示词
5. 使用 "LLM Config Manager (XJ)" 节点管理预设配置：
   - 添加、删除或查看配置
   - 管理多个API提供商的配置

#### 安装方法

1. 将此文件夹复制到ComfyUI的 `custom_nodes` 目录下
2. 重启ComfyUI
3. 在节点菜单中找到 "XJ Nodes" 分类

#### 示例

**MaxNode:**
- 输入: input1=10, input2=5
- 输出: max_value=10

**MinNode:**
- 输入: input1=10, input2=5
- 输出: min_value=5

**AverageNode:**
- 输入: input1=10, input2=5
- 输出: average_value=7.5

**DifferenceNode:**
- 输入: input1=10, input2=5
- 输出: difference_value=5

**ImageUrlLoaderNode:**
- 输入: image_url="https://example.com/image.jpg"
- 输出: image=图像对象

**LLMApiNode:**
- 输入: prompt="请介绍一下人工智能", model="gpt-3.5-turbo"
- 输出: response="人工智能是..."

**LLMVisionNode:**
- 输入: prompt="描述这张图片", image=图像对象, model="gpt-4-vision-preview"
- 输出: response="这张图片显示了..."

**LLMWebSearchNode:**
- 文本搜索: prompt="最新的AI技术发展", enable_search=True, search_api="serpapi", search_api_key="your_key"
- 输出: response="基于搜索结果的回答...", search_results="搜索结果内容..."
- 图像+搜索: prompt="这张图片中的建筑是什么风格？", image=图像对象, enable_search=True
- 输出: response="结合图像分析和搜索结果的综合回答..."

## 版本信息

- 版本: 2.0.0
- 作者: XJ
- 兼容: ComfyUI
- 更新: 将原来的单一比较节点拆分为四个独立的专用节点

## comfyUI 安装
comfyui 的 custom_nodes 路径是  /Users/xj/Documents/ComfyUI/custom_nodes
将 xj_nodes 文件夹复制到 custom_nodes 目录下
运行 python install.py