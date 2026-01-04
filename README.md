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

#### 7. WanxImageGenerationNode - 万相图像生成节点
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

#### 8. SeedreamImageToImageNode - Seedream 图生图节点 ⭐新增
- **功能**: 调用火山引擎 doubao-seedream-4.5 API 进行图生图，支持图像风格转换、内容编辑等
- **API文档**: [火山引擎 Seedream 4.5 API](https://www.volcengine.com/docs/82379/1541523)
- **输入**:
  - image (图像，输入的原始图像，必需)
  - prompt (字符串，图像描述提示词)
  - api_key (字符串，火山引擎 ARK API 密钥)
  - model (字符串，模型选择：doubao-seedream-4.5/doubao-seedream-4.0)
  - strength (浮点数，变化强度0.0-1.0，默认0.5)
  - size (字符串，输出尺寸：auto/1K/2K/4K等)
  - seed (整数，随机种子，-1为随机)
  - watermark (布尔值，是否添加水印)
  - api_url (字符串，API地址，可选)
  - optimize_prompt_mode (字符串，提示词优化：disabled/standard/fast，可选)
- **输出**: 
  - image (生成的图像)
  - info (生成信息，包括耗时等)
- **显示名**: "Seedream 图生图 (XJ)"
- **分类**: "xj_nodes/image"
- **支持功能**: 图像风格转换、AI 重绘、提示词优化、多种尺寸输出、随机种子控制
- **特点**: 
  - 支持 doubao-seedream-4.5 最新模型
  - 可调节图像变化强度（strength参数）
  - 支持提示词自动优化（4.5专属）
  - 自动处理 Base64 图像编码
  - 详细的日志输出和错误提示

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

#### 11. DoubaoVisionWebSearchNode - 豆包视觉+搜索节点 ⭐核心功能
- **功能**: 集成火山引擎的图片理解和联网搜索功能，**支持图片理解后搜索网络信息**
- **核心特性**: 
  - ✅ **图片理解 + 联网搜索**：识别图片内容并搜索相关网络信息（如商品价格、建筑历史等）
  - ✅ **无需额外API**：联网搜索使用火山引擎内置功能，无需SerpAPI等额外服务
  - ✅ **多模态输入**：支持文本+图片的组合输入
  - ✅ **灵活配置**：可选择是否启用联网搜索
- **API文档**: 
  - [联网内容插件](https://www.volcengine.com/docs/82379/1338552) ⭐ 核心功能文档
  - [豆包大模型1.8](https://www.volcengine.com/docs/82379/2123228)
  - [图片理解API](https://www.volcengine.com/docs/82379/1362931)
  - [联网搜索](https://www.volcengine.com/docs/82379/1756990)
- **快速入门**: [QUICK_START.md](llm/QUICK_START.md) ⚡ 5分钟快速上手
- **详细指南**: [DOUBAO_VISION_GUIDE.md](llm/DOUBAO_VISION_GUIDE.md) 📚 完整使用指南
- **模型参考**: [DOUBAO_MODELS.md](llm/DOUBAO_MODELS.md) 📋 模型列表
- **输入**:
  - input_text (字符串，输入文本/问题，必需)
  - api_key (字符串，火山引擎 ARK API 密钥，必需)
  - model (字符串，模型选择，必需，⚠️ 需要支持视觉的模型才能处理图片)
  - enable_websearch (布尔值，是否启用联网搜索，必需)
  - input_image (图像，输入图片，可选，⚠️ 需要支持视觉的模型)
  - api_url (字符串，API地址，可选)
  - temperature (浮点数，温度参数0.0-2.0，可选)
  - max_tokens (整数，最大token数，可选)
  - system_prompt (字符串，系统提示词，可选)
- **输出**: 
  - response (字符串，模型响应内容)
  - search_results (字符串，搜索结果，如果启用了搜索)
  - full_response (字符串，完整响应JSON)
- **显示名**: "豆包视觉+搜索 (XJ)"
- **分类**: "xj_nodes/llm"
- **支持的模型**:
  - ⚠️ **重要**: 必须使用支持视觉功能的模型才能处理图片输入！
  - ✅ **推荐模型**:
    - `doubao-seed-1.6-thinking` - 支持视觉理解和思考链
    - `doubao-vision-pro` - 视觉专业版
    - `doubao-seed-1.8` - 可能支持，需验证
  - ❌ **不支持图片的模型**:
    - `doubao-1-5-pro-32k-250115` 等纯文本模型
  - 💡 **获取可用模型**:
    1. 访问控制台：https://console.volcengine.com/ark/region:ark+cn-beijing/endpoint
    2. 查看"推理接入点"列表，找到支持图片理解的模型
    3. 复制你的 endpoint ID（格式：`ep-xxxxxxxxxxxxx`）
    4. 在节点的 `model` 参数中输入该 endpoint ID
- **典型应用场景**:
  - **图片理解 + 联网搜索**（核心功能）：
    - 识别商品并搜索价格、购买链接
    - 识别建筑并搜索历史文化信息
    - 识别植物/动物并搜索百科知识
  - **纯文本 + 联网搜索**：
    - 查询最新新闻、热点事件
    - 搜索实时天气、股票信息
  - **纯图片理解**：
    - 详细分析图片内容
    - 图片中的文字识别
  - **纯文本问答**：
    - 常规文本问答（不需要最新信息）
- **常见错误和解决**:
  - ❌ **错误**: `llm model received multi-modal messages`
    - **原因**: 使用了不支持视觉的模型但连接了图片
    - **解决**: 使用 `doubao-seed-1.6-thinking` 等支持视觉的模型
  - ❌ **错误**: `InvalidEndpointOrModel.NotFound`
    - **原因**: 模型或 endpoint ID 不存在
    - **解决**: 从控制台获取正确的 endpoint ID
  - ❌ **错误**: 模型名称格式错误（如 `doubao-seed-1-8-251215`）
    - **原因**: 使用了错误的模型名称格式
    - **解决**: 使用正确格式（如 `doubao-seed-1.8`）或 endpoint ID
- **特点**:
  - 原生支持火山引擎联网搜索工具
  - 无需额外的搜索API密钥（使用火山引擎内置搜索）
  - 支持 performance_first 搜索模式
  - 多模态输入，灵活组合
  - 详细的日志输出和错误处理

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