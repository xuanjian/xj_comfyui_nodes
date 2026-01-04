# Seedream 图生图节点使用指南

## 📚 概述

Seedream 图生图节点是基于火山引擎 doubao-seedream-4.5 API 开发的 ComfyUI 自定义节点，支持将输入图像通过 AI 进行风格转换、内容编辑等图生图操作。

**API 官方文档**: [火山引擎 Seedream 4.5 API](https://www.volcengine.com/docs/82379/1541523)

## 🎯 主要功能

- ✅ **图像风格转换** - 将图片转换为不同的艺术风格
- ✅ **AI 重绘** - 根据提示词重新生成图像内容
- ✅ **可调强度** - 通过 strength 参数控制变化程度（0.0-1.0）
- ✅ **提示词优化** - 自动优化提示词质量（doubao-seedream-4.5 专属）
- ✅ **多种尺寸** - 支持 1K、2K、4K 等多种输出尺寸
- ✅ **随机种子** - 控制生成结果的可重复性

## 🔧 使用方法

### 1. 获取 API Key

1. 访问 [火山引擎控制台](https://console.volcengine.com/)
2. 开通大模型服务平台
3. 创建 API Key
4. 将 API Key 设置为环境变量 `ARK_API_KEY` 或直接在节点中输入

### 2. 在 ComfyUI 中添加节点

1. 双击画布空白处，搜索 `Seedream`
2. 选择 **"Seedream 图生图 (XJ)"** 节点
3. 或者通过菜单：右键 → `Add Node` → `xj_nodes/image` → `Seedream 图生图 (XJ)`

### 3. 配置参数

#### 必需参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `image` | IMAGE | 输入的原始图像 |
| `prompt` | STRING | 图像描述提示词，描述你想要生成的效果 |
| `api_key` | STRING | 火山引擎 ARK API 密钥 |

#### 可选参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `model` | STRING | doubao-seedream-4.5 | 模型选择 |
| `strength` | FLOAT | 0.5 | 变化强度（0.0-1.0），值越大变化越大 |
| `size` | STRING | auto | 输出尺寸，auto 为自动匹配输入图像 |
| `seed` | INT | -1 | 随机种子，-1 为随机生成 |
| `watermark` | BOOLEAN | False | 是否添加水印 |
| `api_url` | STRING | 官方地址 | API 地址，可自定义 |
| `optimize_prompt_mode` | STRING | disabled | 提示词优化模式 |

### 4. 模型选择

- **doubao-seedream-4.5** (推荐) - 最新版本，支持提示词优化
- **doubao-seedream-4-5-251128** - 4.5 的特定版本
- **doubao-seedream-4.0** - 稳定版本
- **doubao-seedream-4-0-250828** - 4.0 的特定版本

### 5. Strength 参数详解

`strength` 参数控制图像变化的程度：

- **0.0 - 0.3**: 轻微修改，保留大部分原图内容
- **0.3 - 0.5**: 中等修改，平衡原图和新内容
- **0.5 - 0.7**: 较大修改，更多创意变化
- **0.7 - 1.0**: 大幅修改，可能完全改变图像

### 6. 提示词优化模式

仅 **doubao-seedream-4.5** 支持：

- **disabled**: 不优化（默认）
- **standard**: 标准优化，质量更高但耗时较长
- **fast**: 快速优化，速度更快但质量一般

## 📝 使用示例

### 示例 1: 风格转换

```
输入图像: 一张普通的风景照片
Prompt: "将这张照片转换为水彩画风格，色彩柔和，笔触自然"
Strength: 0.6
Model: doubao-seedream-4.5
Optimize Prompt: standard
```

### 示例 2: 季节变换

```
输入图像: 夏天的树林
Prompt: "将场景改为冬天，树上覆盖白雪，地面有积雪"
Strength: 0.7
Model: doubao-seedream-4.5
```

### 示例 3: 光线调整

```
输入图像: 白天的城市街道
Prompt: "改为黄昏时分，温暖的金色阳光，长长的影子"
Strength: 0.5
Model: doubao-seedream-4.5
```

### 示例 4: 艺术风格化

```
输入图像: 普通人物照片
Prompt: "转换为梵高星空风格的油画，色彩鲜艳，笔触明显"
Strength: 0.8
Model: doubao-seedream-4.5
Optimize Prompt: standard
```

## 🎨 提示词编写技巧

### 好的提示词示例

✅ **具体描述**：
- "将图片转换为日本浮世绘风格，使用蓝色和橙色调，线条清晰"

✅ **包含风格元素**：
- "赛博朋克风格，霓虹灯光效果，未来主义建筑，紫色和粉色主调"

✅ **描述光线和氛围**：
- "电影级光线，戏剧性的明暗对比，神秘氛围，暖色调"

### 避免的提示词

❌ **过于简短**：
- "好看的"
- "艺术"

❌ **过于复杂矛盾**：
- "既要写实又要抽象，既要明亮又要黑暗..."

## 💡 最佳实践

1. **逐步调整 Strength**
   - 先从较低的值（0.3-0.5）开始测试
   - 根据效果逐步增加，找到最佳值

2. **使用固定 Seed**
   - 在找到满意的效果后，记录 seed 值
   - 可用于批量处理类似图片

3. **启用提示词优化**
   - 对于复杂的艺术风格，建议使用 standard 模式
   - 简单转换可以不启用或使用 fast 模式

4. **选择合适的尺寸**
   - `auto`: 保持输入图像尺寸（推荐）
   - `1K/2K/4K`: 标准尺寸输出
   - 特定尺寸: 如 `2048x2048`, `1440x2560` 等

## ⚠️ 注意事项

1. **API 费用**: 此节点调用火山引擎 API，会产生费用，请查看官方定价
2. **处理时间**: 根据图像大小和复杂度，生成可能需要 10-60 秒
3. **网络要求**: 需要稳定的网络连接访问火山引擎 API
4. **API Key 安全**: 不要将 API Key 分享给他人或提交到公共代码库

## 🐛 故障排查

### 问题 1: "❌ 错误: 请设置 API Key"

**解决方法**:
- 设置环境变量 `ARK_API_KEY`
- 或在节点的 `api_key` 参数中直接输入

### 问题 2: API 请求失败

**可能原因**:
- API Key 无效或过期
- 账户余额不足
- 网络连接问题
- API 地址错误

**解决方法**:
- 检查 ComfyUI 控制台的错误详情
- 验证 API Key 是否正确
- 检查网络连接

### 问题 3: 生成结果不理想

**优化建议**:
- 调整 `strength` 参数
- 改进提示词描述
- 启用提示词优化
- 尝试不同的 seed 值

## 📊 输出说明

节点有两个输出：

1. **image** (IMAGE): 生成的图像，可以连接到其他图像处理节点
2. **info** (STRING): 生成信息，包含：
   - 生成的图片数量
   - API 调用耗时
   - 错误信息（如果有）

## 🔗 相关链接

- [火山引擎 Seedream API 文档](https://www.volcengine.com/docs/82379/1541523)
- [火山引擎控制台](https://console.volcengine.com/)
- [GitHub 仓库](https://github.com/xuanjian/xj_comfyui_nodes)

## 📮 反馈与支持

如有问题或建议，请通过以下方式联系：
- GitHub Issues: https://github.com/xuanjian/xj_comfyui_nodes/issues
- 在使用过程中如果遇到 Bug，请提供：
  - 错误信息（控制台输出）
  - 使用的参数配置
  - ComfyUI 版本
