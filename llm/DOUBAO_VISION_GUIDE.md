# 豆包视觉+搜索节点使用指南

## 📚 概述

豆包视觉+搜索节点是基于火山引擎多模态理解和联网搜索API开发的 ComfyUI 自定义节点，支持图片理解和可选的联网搜索功能。

**官方文档**：
- [豆包大模型1.8(最新)](https://www.volcengine.com/docs/82379/2123228) ⭐ 最新文档
- [图片理解 API](https://www.volcengine.com/docs/82379/1362931)
- [联网搜索 Web Search](https://www.volcengine.com/docs/82379/1756990)
- [豆包助手参考](https://www.volcengine.com/docs/82379/1978533)

**模型参考**：
- [豆包模型参考列表](./DOUBAO_MODELS.md) - 查看可能的模型名称和获取方法

## 🎯 主要功能

- ✅ **多模态理解** - 同时支持文本和图片输入
- ✅ **图片理解** - 深度分析图片内容、物体、场景等
- ✅ **联网搜索** - 可选启用火山引擎内置联网搜索
- ✅ **图片理解+联网搜索** - 理解图片后搜索相关网络信息（核心功能）
- ✅ **灵活组合** - 支持4种使用模式
- ✅ **高性能模型** - 支持 doubao-vision-pro 等多个模型
- ✅ **无需额外API** - 联网搜索使用火山引擎内置功能，无需额外搜索API密钥

## 💡 典型应用场景

### 场景1：图片理解+联网搜索（最强大）
**用例**：识别图片中的商品，并搜索最新价格和购买链接
```
input_text: "这是什么商品？帮我搜索一下它的价格和购买链接"
input_image: 连接商品图片
enable_websearch: True
model: doubao-seed-1.6-thinking（或其他支持视觉的模型）
```

### 场景2：图片理解+信息整合
**用例**：识别建筑并搜索历史文化信息
```
input_text: "这是什么建筑？搜索它的历史和文化价值"
input_image: 连接建筑图片
enable_websearch: True
```

### 场景3：纯图片理解
**用例**：分析图片内容
```
input_text: "详细描述这张图片"
input_image: 连接图片
enable_websearch: False
```

### 场景4：纯文本+联网搜索
**用例**：实时信息查询
```
input_text: "今天的热点新闻有哪些？"
input_image: 不连接
enable_websearch: True
```

## 🔧 使用方法

### 1. 获取 API Key

1. 访问 [火山引擎控制台](https://console.volcengine.com/)
2. 开通大模型服务平台
3. 创建 API Key
4. 将 API Key 设置为环境变量 `ARK_API_KEY` 或直接在节点中输入

### 2. 在 ComfyUI 中添加节点

1. 双击画布空白处，搜索 `豆包`
2. 选择 **"豆包视觉+搜索 (XJ)"** 节点
3. 或者通过菜单：右键 → `Add Node` → `xj_nodes/llm` → `豆包视觉+搜索 (XJ)`

### 3. 配置参数

#### 必需参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `input_text` | STRING | 输入文本/问题 |
| `api_key` | STRING | 火山引擎 ARK API 密钥 |
| `model` | STRING | 模型选择 |
| `enable_websearch` | BOOLEAN | 是否启用联网搜索 |

#### 可选参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `input_image` | IMAGE | None | 输入图片（⚠️ 需要支持视觉的模型）|
| `api_url` | STRING | 官方地址 | API 地址 |
| `temperature` | FLOAT | 0.7 | 温度参数（0.0-2.0） |
| `max_tokens` | INT | 2048 | 最大token数 |
| `system_prompt` | STRING | "" | 系统提示词 |

**⚠️ 图片输入重要提示**：
- 只有**支持视觉的模型**才能处理图片输入
- 推荐模型：`doubao-seed-1.6-thinking`、`doubao-vision-pro`
- 如果使用纯文本模型连接图片，会报错：`llm model received multi-modal messages`
- 要实现"图片理解+联网搜索"，必须使用支持视觉的模型

### 4. 模型选择（重要！）

**⚠️ 重要提示：不同账户的可用模型列表可能不同！**

节点默认使用 `ep-20241230110515-kg8wl`（豆包1.8-pro-32k），但如果这个模型在你的账户中不可用，你需要：

#### 步骤 1: 获取你的 Endpoint ID

1. 访问火山引擎控制台：
   ```
   https://console.volcengine.com/ark/region:ark+cn-beijing/endpoint
   ```

2. 登录你的账户

3. 在左侧菜单找到"推理接入点"或"Endpoint"

4. 查看你的推理接入点列表

5. 找到支持图片理解的模型（通常名称包含 "vision" 或 "多模态"）

6. 复制该接入点的 **Endpoint ID**（格式：`ep-xxxxxxxxxxxxx`）

#### 步骤 2: 在节点中输入 Endpoint ID

1. 在 ComfyUI 中找到"豆包视觉+搜索"节点

2. 在 `model` 参数中，删除默认值

3. 输入你从控制台复制的 endpoint ID

4. 保存并运行节点

#### 常见 Endpoint ID 格式示例

- `ep-20241230110515-kg8wl` - 豆包1.8-pro-32k（可能在某些账户中可用）
- `ep-20250101215047-n8lcv` - 豆包1.8-lite-32k（可能在某些账户中可用）
- `ep-xxxxxxxxxxxxx` - 你的账户专属 endpoint ID

**注意**：
- ✅ **必须使用 endpoint ID 格式**（以 `ep-` 开头）
- ❌ **不要使用模型名称格式**（如 `doubao-vision-pro-32k`）
- 🔍 **每个账户的可用模型列表不同**，请从控制台获取

## 📝 四种使用模式

### 模式 1: 纯文本问答

**配置**：
- `input_text`: "请介绍一下人工智能的发展历程"
- `enable_websearch`: False
- `input_image`: 不连接

**用途**：基础的文本问答，类似普通的 LLM 对话

### 模式 2: 图片理解

**配置**：
- `input_text`: "请详细描述这张图片中的内容"
- `enable_websearch`: False
- `input_image`: 连接图片

**用途**：分析图片内容、识别物体、理解场景

### 模式 3: 文本 + 联网搜索

**配置**：
- `input_text`: "2024年最新的AI技术进展有哪些？"
- `enable_websearch`: True
- `input_image`: 不连接

**用途**：获取最新信息、实时资讯查询

### 模式 4: 图片理解 + 联网搜索（最强大）

**配置**：
- `input_text`: "这张图片中的建筑是什么风格？请搜索相关历史背景"
- `enable_websearch`: True
- `input_image`: 连接图片

**用途**：结合图片分析和网络信息，提供全面深入的回答

## 🎨 使用示例

### 示例 1: 图片内容分析

```
input_text: "请详细描述这张图片，包括场景、物体、颜色、构图等"
model: ep-20241230110515-kg8wl
enable_websearch: False
input_image: [连接图片]
```

**预期输出**：详细的图片描述，包括视觉元素分析

### 示例 2: 图片中的文字识别

```
input_text: "请提取图片中的所有文字内容"
model: ep-20241230110515-kg8wl
enable_websearch: False
input_image: [连接图片]
```

**预期输出**：图片中的文字内容

### 示例 3: 图片+知识查询

```
input_text: "图片中的动物是什么？请搜索它的生活习性和分布区域"
model: ep-20241230110515-kg8wl
enable_websearch: True
input_image: [连接动物图片]
```

**预期输出**：识别动物 + 搜索到的详细信息

### 示例 4: 实时信息查询

```
input_text: "今天的天气如何？最新的科技新闻有哪些？"
model: ep-20241230110515-kg8wl
enable_websearch: True
input_image: 不连接
```

**预期输出**：搜索到的实时天气和新闻信息

### 示例 5: 图片内容扩展

```
input_text: "这张图片展示的是什么场景？请搜索相关的旅游信息和历史背景"
model: ep-20241230110515-kg8wl
enable_websearch: True
input_image: [连接风景图片]
```

**预期输出**：场景识别 + 旅游信息 + 历史背景

## 💡 提示词技巧

### 图片理解类提示词

✅ **具体明确**：
- "请描述图片中的主要物体和它们的位置关系"
- "识别图片中的所有文字并翻译成中文"
- "分析这张图片的构图和色彩运用"

✅ **分步骤**：
- "首先识别图片主题，然后描述细节，最后给出整体评价"

### 搜索增强类提示词

✅ **明确搜索意图**：
- "图片中的建筑是什么？请搜索它的建造年代和历史"
- "识别图片中的品牌，并搜索该品牌的最新产品信息"

✅ **结合分析**：
- "分析图片内容，并搜索相关的专业知识进行解释"

### 避免的提示词

❌ **过于模糊**：
- "看看这个"
- "说说"

❌ **没有明确任务**：
- "这是什么？"（可以更具体：这是什么建筑/动物/植物？）

## 🔄 工作流示例

### 基础工作流：图片分析

```
[LoadImage] → [豆包视觉+搜索] → [ShowText]
```

### 批量图片分析

```
                  ┌→ [豆包视觉+搜索] → [SaveText-1]
                  │
[LoadImage Batch] ┼→ [豆包视觉+搜索] → [SaveText-2]
                  │
                  └→ [豆包视觉+搜索] → [SaveText-3]
```

### 图片理解 + 后续处理

```
[LoadImage] → [豆包视觉+搜索] → [文本处理节点] → [其他LLM节点]
```

### 多模态流程

```
[LoadImage] → [豆包视觉+搜索] → [提取信息] → [Seedream图生图] → [SaveImage]
```

## ⚙️ 高级配置

### Temperature 参数

- **0.0 - 0.3**: 精确、确定性强，适合事实性回答
- **0.4 - 0.7**: 平衡，适合一般对话
- **0.8 - 1.0**: 创造性强，适合创意性任务
- **1.1 - 2.0**: 高度随机，实验性使用

### Max Tokens

- **512-1024**: 简短回答
- **1024-2048**: 中等长度（默认）
- **2048-4096**: 详细回答
- **4096+**: 长篇内容

### System Prompt 示例

```
你是一个专业的图像分析专家，擅长识别图片中的细节并提供准确的描述。
请用专业但易懂的语言回答问题。
```

## 📊 输出说明

节点有三个输出：

1. **response** (STRING): 模型的主要响应内容
2. **search_results** (STRING): 搜索结果（如果启用了搜索）
3. **full_response** (STRING): 完整的 JSON 响应，包含所有元数据

## ⚠️ 注意事项

1. **API 费用**: 调用火山引擎 API 会产生费用，图片理解和搜索都会计费
2. **处理时间**: 
   - 纯文本：约 1-5 秒
   - 图片理解：约 3-10 秒
   - 启用搜索：约 5-15 秒
3. **网络要求**: 需要稳定的网络连接
4. **图片大小**: 建议图片不超过 10MB，分辨率适中
5. **搜索限制**: 联网搜索功能可能受地区和网络限制

## 🐛 故障排查

### 问题 1: "❌ 错误: 请设置 API Key"

**解决方法**:
- 设置环境变量 `ARK_API_KEY`
- 或在节点的 `api_key` 参数中直接输入

### 问题 2: 图片无法识别

**可能原因**:
- 图片格式不支持
- 图片过大或过小
- 图片内容模糊

**解决方法**:
- 使用 PNG/JPG 格式
- 调整图片大小到合理范围（建议 512-2048px）
- 提高图片清晰度

### 问题 3: 模型不存在错误（最常见）

**错误示例**:
```
InvalidEndpointOrModel.NotFound: The model or endpoint ep-xxxxx does not exist
```

**原因**：
- 不同账户的可用模型列表不同
- 默认的 endpoint ID 可能在你的账户中不存在
- 需要从你自己的控制台获取可用的 endpoint ID

**解决方法**（按步骤操作）：

1. **访问控制台**：
   ```
   https://console.volcengine.com/ark/region:ark+cn-beijing/endpoint
   ```

2. **查看推理接入点**：
   - 登录后，在左侧菜单找到"推理接入点"
   - 查看你的接入点列表
   - 找到支持图片理解的模型（通常名称包含 "vision"、"多模态" 或 "doubao-vision"）

3. **复制 Endpoint ID**：
   - 点击接入点，查看详情
   - 复制 **Endpoint ID**（格式：`ep-xxxxxxxxxxxxx`）
   - 注意：不是模型名称，而是 endpoint ID

4. **在节点中输入**：
   - 打开 ComfyUI 中的"豆包视觉+搜索"节点
   - 在 `model` 参数中，删除默认值
   - 粘贴你复制的 endpoint ID
   - 保存并重新运行

5. **验证**：
   - 如果仍然报错，尝试列表中的其他 endpoint ID
   - 确保 endpoint ID 格式正确（以 `ep-` 开头）

**重要提示**：
- ✅ 每个账户的可用模型列表不同
- ✅ 必须使用 endpoint ID 格式（`ep-xxxxxxxxxxxxx`）
- ❌ 不要使用模型名称格式（如 `doubao-vision-pro-32k`）
- 🔍 如果控制台中没有可用的视觉模型，可能需要先创建推理接入点

### 问题 3: 多模态输入错误

**错误信息**: `llm model received multi-modal messages`

**原因**：
- 当前模型**不支持图片输入**（多模态）
- 你使用的是纯文本模型（如 `doubao-1-5-pro-32k-250115`）
- 但连接了图片到 `input_image`

**解决方法**：
1. **使用支持视觉的模型**（推荐）：
   - 在控制台查找包含 `vision` 或支持多模态的 endpoint
   - 推荐尝试：`doubao-seed-1.6-thinking`
   - 或查看控制台的"视觉模型"分类

2. **或者不连接图片**：
   - 如果只需要文本+联网搜索
   - 不要连接 `input_image` 输入

3. **验证模型能力**：
   - 在控制台查看模型详情
   - 确认模型支持"图片理解"或"多模态"功能

**实现"图片理解+联网搜索"的正确配置**：
```
✅ model: doubao-seed-1.6-thinking (或其他支持视觉的模型)
✅ input_image: 连接图片
✅ enable_websearch: True
✅ input_text: "这是什么？帮我搜索相关信息"
```

### 问题 4: 搜索功能无结果

**可能原因**:
- 网络问题
- 搜索服务暂时不可用
- 提示词不明确

**解决方法**:
- 检查网络连接
- 稍后重试
- 优化提示词，明确搜索意图

### 问题 5: 响应速度慢

**优化建议**:
- 使用 lite 版本模型（`ep-20250101215047-n8lcv`）
- 减小图片尺寸
- 降低 max_tokens
- 不使用搜索功能时关闭开关

## 🆚 与其他节点的对比

### vs. LLMVisionNode

| 特性 | 豆包视觉+搜索 | LLMVisionNode |
|------|--------------|---------------|
| 图片理解 | ✅ | ✅ |
| 联网搜索 | ✅（内置）| ❌ |
| 搜索API | 无需额外配置 | - |
| 专用优化 | 火山引擎专用 | 通用OpenAI兼容 |

### vs. LLMWebSearchNode

| 特性 | 豆包视觉+搜索 | LLMWebSearchNode |
|------|--------------|------------------|
| 图片理解 | ✅ | ✅ |
| 联网搜索 | ✅（内置）| ✅（需要外部API）|
| 搜索API密钥 | 不需要 | 需要 SerpAPI 等 |
| 搜索质量 | 火山引擎内置 | 多个搜索引擎选择 |

## 🎓 最佳实践

1. **图片预处理**: 使用合适的分辨率和格式
2. **清晰提示词**: 明确说明要分析什么、搜索什么
3. **合理使用搜索**: 只在需要最新信息时启用
4. **保存结果**: 将重要的分析结果保存下来
5. **批量处理**: 对于大量图片，考虑批量处理工作流

## 🔗 相关链接

- [豆包大模型1.8(最新)](https://www.volcengine.com/docs/82379/2123228) ⭐ 最新文档
- [火山引擎图片理解 API](https://www.volcengine.com/docs/82379/1362931)
- [火山引擎联网搜索](https://www.volcengine.com/docs/82379/1756990)
- [火山引擎控制台](https://console.volcengine.com/)
- [GitHub 仓库](https://github.com/xuanjian/xj_comfyui_nodes)

## 📮 反馈与支持

如有问题或建议，请通过 GitHub Issues 反馈：
https://github.com/xuanjian/xj_comfyui_nodes/issues
