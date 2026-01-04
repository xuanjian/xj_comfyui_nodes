# 豆包视觉+搜索节点快速入门

## 🚀 核心功能

**实现"图片理解 + 联网搜索"**：识别图片内容并搜索相关网络信息

参考文档：[联网内容插件](https://www.volcengine.com/docs/82379/1338552)

## ✅ 正确配置示例

### 场景1：识别商品并搜索价格

```
model: doubao-seed-1.6-thinking  ✅ 支持视觉的模型
input_text: "这是什么商品？帮我搜索它的价格和购买链接"
input_image: 连接商品图片
enable_websearch: True
```

### 场景2：识别建筑并搜索历史

```
model: doubao-vision-pro  ✅ 支持视觉的模型
input_text: "这是什么建筑？搜索它的历史和文化"
input_image: 连接建筑图片
enable_websearch: True
```

### 场景3：纯文本+联网搜索（推荐配置）

```
model: ep-20250208104337-4wr54  ✅ 已验证的通用模型（节点默认值）
input_text: "今天有什么热点新闻？"
input_image: 不连接
enable_websearch: True
```

**说明**：`ep-20250208104337-4wr54` 是已验证的通用模型，支持文本理解和联网搜索，但不支持图片输入。

### 场景4：纯图片理解（不搜索）

```
model: doubao-seed-1.6-thinking  ✅ 支持视觉的模型
input_text: "详细描述这张图片"
input_image: 连接图片
enable_websearch: False
```

## ❌ 常见错误

### 错误1：多模态输入错误

```
❌ 错误配置：
model: doubao-1-5-pro-32k-250115  ❌ 不支持视觉
input_image: 连接了图片
```

**错误信息**：`llm model received multi-modal messages`

**原因**：模型不支持图片输入

**解决**：
1. 使用支持视觉的模型：`doubao-seed-1.6-thinking`、`doubao-vision-pro`
2. 或者不连接图片

### 错误2：模型不存在

```
❌ 错误信息：
InvalidEndpointOrModel.NotFound
```

**解决**：
1. 访问控制台：https://console.volcengine.com/ark/region:ark+cn-beijing/endpoint
2. 复制你的 endpoint ID（格式：`ep-xxxxxxxxxxxxx`）
3. 在节点的 `model` 参数中输入

### 错误3：模型名称格式错误

```
❌ 错误：doubao-seed-1-8-251215  (使用了连字符)
✅ 正确：doubao-seed-1.8  (使用点号)
```

## 🔑 获取 API Key

1. 访问 [火山引擎控制台](https://console.volcengine.com/)
2. 开通大模型服务平台
3. 创建 API Key
4. 在节点中输入 API Key

## 📚 支持的模型

### 支持视觉（图片理解）的模型

- ✅ `doubao-seed-1.6-thinking` - 推荐，支持思考链
- ✅ `doubao-vision-pro` - 视觉专业版
- ✅ `doubao-seed-1.8` - 可能支持，需验证

### 纯文本模型（不支持图片）

- ❌ `ep-20250208104337-4wr54` - 通用模型，仅文本（节点默认值）
- ❌ `doubao-1-5-pro-32k-250115` - 仅文本
- ❌ 其他不带 `vision` 或 `seed` 的模型

### 🔍 如何找到支持视觉的模型？

**方法1：从控制台查找（推荐）**

1. 访问控制台：https://console.volcengine.com/ark/region:ark+cn-beijing/endpoint
2. 登录你的账户
3. 查看"推理接入点"列表
4. **查找包含以下关键词的模型**：
   - `vision` - 视觉模型
   - `多模态` - 多模态模型
   - `doubao-vision` - 豆包视觉模型
   - `doubao-seed-1.6` - 可能支持视觉
5. 查看模型详情，确认支持"图片理解"或"多模态输入"
6. 复制对应的 Endpoint ID（格式：`ep-xxxxxxxxxxxxx`）
7. 在节点的 `model` 参数中输入该 Endpoint ID

**方法2：尝试模型名称**

如果模型名称可用，可以尝试：
- `doubao-seed-1.6-thinking` - 支持视觉理解
- `doubao-vision-pro` - 视觉专业版
- `doubao-seed-1.8` - 可能支持，需验证

**⚠️ 重要提示**：
- 不同账户的可用模型列表可能不同
- 必须从你自己的控制台获取可用的模型
- 通用模型（如 `ep-20250208104337-4wr54`）不支持图片输入

## 💡 最佳实践

### 图片理解+搜索提示词模板

```
"这张图片中的[对象]是什么？请搜索：
1. 详细介绍
2. 价格信息
3. 购买链接
4. 用户评价"
```

### 联网搜索提示词技巧

- ✅ 明确搜索意图："搜索价格"、"查找资料"
- ✅ 分点列出需求：1. xx 2. xx
- ✅ 指定信息类型：价格、评价、历史等
- ❌ 避免模糊："了解一下"

## 🎯 工作流程

```
1. 图片输入 → 模型识别图片内容
2. 启用搜索 → 自动搜索相关网络信息
3. 整合结果 → 结合图片理解和搜索结果
4. 输出答案 → 完整、准确的回答
```

## 🔗 相关资源

- [详细使用指南](./DOUBAO_VISION_GUIDE.md)
- [模型参考列表](./DOUBAO_MODELS.md)
- [官方文档：联网内容插件](https://www.volcengine.com/docs/82379/1338552)
- [官方文档：图片理解 API](https://www.volcengine.com/docs/82379/1362931)

## 🆘 获取帮助

遇到问题？按顺序检查：

1. ✅ 模型是否支持视觉？→ 使用 `doubao-seed-1.6-thinking`
2. ✅ API Key 是否有效？→ 在控制台验证
3. ✅ Endpoint ID 是否正确？→ 从控制台复制
4. ✅ 图片是否正常连接？→ 检查 ComfyUI 连接
5. ✅ 搜索开关是否正确？→ True/False

---

**提示**：第一次使用建议从**场景1**开始测试，验证图片理解和联网搜索都正常工作。
