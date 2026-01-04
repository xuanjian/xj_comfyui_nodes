# 更新日志

## 2025-01-XX - 豆包视觉+搜索节点发布

### 🎉 新功能

#### 豆包视觉+搜索节点 (DoubaoVisionWebSearchNode)

**核心功能：图片理解 + 联网搜索**

- ✅ **多模态理解** - 同时支持文本和图片输入
- ✅ **图片理解** - 深度分析图片内容、物体、场景等
- ✅ **联网搜索** - 可选启用火山引擎内置联网搜索
- ✅ **图片理解+联网搜索** - 理解图片后搜索相关网络信息（核心功能）

### 📝 主要特性

1. **智能模型兼容性检测**
   - 提前检测模型是否支持图片输入
   - 友好的错误提示和解决建议
   - 避免不必要的 API 调用

2. **完善的错误处理**
   - API URL 自动补全
   - 404 错误详细提示
   - 多模态输入错误提前检测
   - 模型不存在错误处理

3. **联网搜索工具**
   - 使用官方标准格式
   - 支持自动工具调用
   - 无需额外搜索 API

4. **完整文档**
   - QUICK_START.md - 5分钟快速入门
   - DOUBAO_VISION_GUIDE.md - 详细使用指南
   - DOUBAO_MODELS.md - 模型参考列表

### 🔧 技术改进

- 联网搜索工具格式修复（符合官方 API 规范）
- Authorization 头自动处理（支持带/不带 Bearer 前缀）
- 工具调用格式优化（添加 tool_choice: "auto"）
- 错误提示优化（更详细的错误信息和解决步骤）

### 📚 文档更新

- 更新 README.md - 添加节点详细说明
- 新增 QUICK_START.md - 快速入门指南
- 新增 DOUBAO_VISION_GUIDE.md - 完整使用指南
- 新增 DOUBAO_MODELS.md - 模型参考列表

### 🐛 修复的问题

- ✅ 修复 MissingParameter: tools.function 错误
- ✅ 修复 404 API URL 错误
- ✅ 修复多模态输入错误提示
- ✅ 修复模型兼容性检测

### 📦 文件结构

```
xj_nodes/
├── llm/
│   ├── doubao_vision_websearch_node.py  # 主节点文件
│   ├── QUICK_START.md                   # 快速入门
│   ├── DOUBAO_VISION_GUIDE.md          # 详细指南
│   └── DOUBAO_MODELS.md                 # 模型参考
├── README.md                             # 项目说明
└── CHANGELOG.md                          # 更新日志
```

### 🚀 使用方法

1. 在 ComfyUI 中搜索 "豆包视觉+搜索 (XJ)"
2. 配置 API Key 和模型
3. 连接图片（可选）
4. 启用联网搜索（可选）
5. 运行节点

### 📖 相关链接

- [快速入门](llm/QUICK_START.md)
- [详细指南](llm/DOUBAO_VISION_GUIDE.md)
- [模型参考](llm/DOUBAO_MODELS.md)
- [火山引擎文档](https://www.volcengine.com/docs/82379/1338552)

---

**注意**：此节点需要火山引擎 API Key，请从控制台获取。
