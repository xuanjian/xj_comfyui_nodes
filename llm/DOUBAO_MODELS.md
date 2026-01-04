# 豆包模型参考列表

## 📋 最新豆包模型信息

根据[火山引擎豆包大模型1.8文档](https://www.volcengine.com/docs/82379/2123228)，以下是可能的模型名称格式：

### 模型名称格式（可能可用）

#### 豆包1.8系列（最新）
- `doubao-seed-1.8` - 豆包1.8通用版本
- `doubao-seed-1.8-pro` - 豆包1.8专业版
- `doubao-seed-1.8-lite` - 豆包1.8轻量版
- `doubao-seed-1.8-vision` - 豆包1.8视觉版（如果支持）

#### 豆包1.6系列
- `doubao-seed-1.6-thinking` - 豆包1.6思考版（支持视觉理解）
- `doubao-seed-1.6-flash` - 豆包1.6快速版（支持视觉理解）

#### 视觉模型（可能可用）
- `doubao-vision-pro` - 豆包视觉专业版
- `doubao-vision-pro-32k` - 豆包视觉专业版（32K上下文）
- `doubao-vision-pro-256k` - 豆包视觉专业版（256K上下文）
- `doubao-vision-lite` - 豆包视觉轻量版
- `doubao-vision-lite-32k` - 豆包视觉轻量版（32K上下文）

### Endpoint ID 格式（推荐使用）

格式：`ep-xxxxxxxxxxxxx`

**已验证的 Endpoint ID**（从控制台获取）：
- `ep-20250208104337-4wr54` - **通用模型**（推荐用于文本+联网搜索）
  - ✅ 支持文本理解
  - ✅ 支持联网搜索
  - ⚠️ **不支持图片输入**（纯文本模型）
  - 📍 控制台：https://console.volcengine.com/ark/region:ark+cn-beijing/endpoint/detail?Id=ep-20250208104337-4wr54

**其他示例**（这些是示例，实际ID可能不同）：
- `ep-20241230110515-kg8wl` - 可能是豆包1.8-pro
- `ep-20250101215047-n8lcv` - 可能是豆包1.8-lite
- `ep-20250102000000-xxxxx` - 可能是更新的版本

## ⚠️ 重要提示

1. **不同账户的可用模型列表不同**
   - 每个账户可能有不同的模型访问权限
   - 必须从你自己的控制台获取可用的模型列表

2. **推荐使用 Endpoint ID**
   - Endpoint ID 格式（`ep-` 开头）更稳定可靠
   - 模型名称格式可能在不同账户中不可用

3. **如何获取你的模型列表**

   **方法1：通过控制台**
   ```
   1. 访问：https://console.volcengine.com/ark/region:ark+cn-beijing/endpoint
   2. 登录你的账户
   3. 查看"推理接入点"列表
   4. 找到支持图片理解的模型
   5. 复制 Endpoint ID
   ```

   **方法2：通过API查询**
   ```python
   import requests
   
   headers = {
       "Authorization": f"Bearer YOUR_API_KEY"
   }
   
   # 查询可用的模型列表
   response = requests.get(
       "https://ark.cn-beijing.volces.com/api/v3/models",
       headers=headers
   )
   
   print(response.json())
   ```

## 🔍 查找支持图片理解的模型

在控制台中查找模型时，注意以下特征：

1. **模型名称包含**：
   - `vision` - 视觉模型
   - `多模态` - 多模态模型
   - `doubao-vision` - 豆包视觉模型
   - `doubao-seed-1.8` - 豆包1.8（可能支持视觉）

2. **模型能力说明**：
   - 支持图片理解
   - 支持多模态输入
   - 支持图像+文本

3. **模型类型**：
   - 视觉理解模型
   - 多模态大模型

## 📝 使用建议

1. **优先使用 Endpoint ID**
   - 格式：`ep-xxxxxxxxxxxxx`
   - 从控制台获取你自己的 Endpoint ID

2. **如果 Endpoint ID 不可用，尝试模型名称**
   - 先尝试 `doubao-seed-1.8`
   - 再尝试 `doubao-vision-pro`
   - 最后尝试其他格式

3. **验证模型是否可用**
   - 在节点中输入模型名称或 Endpoint ID
   - 运行节点测试
   - 如果报错"模型不存在"，尝试其他模型

## 🔗 相关链接

- [豆包大模型1.8文档](https://www.volcengine.com/docs/82379/2123228)
- [图片理解API文档](https://www.volcengine.com/docs/82379/1362931)
- [火山引擎控制台](https://console.volcengine.com/ark/region:ark+cn-beijing/endpoint)
- [豆包产品页面](https://www.volcengine.com/product/doubao/)

## 💡 快速测试

如果你想快速测试哪些模型可用，可以尝试以下顺序：

### 文本 + 联网搜索（推荐使用）
1. `ep-20250208104337-4wr54` - **已验证的通用模型**（节点默认值）
   - ✅ 支持文本理解
   - ✅ 支持联网搜索
   - ❌ 不支持图片输入

### 图片理解 + 联网搜索
1. `doubao-seed-1.8` - 最新通用版本（可能支持视觉）
2. `doubao-vision-pro` - 视觉专业版
3. `doubao-seed-1.6-thinking` - 1.6思考版（支持视觉）
4. 从控制台获取支持视觉的 Endpoint ID

**注意**：
- 通用模型（如 `ep-20250208104337-4wr54`）只支持文本，不能连接图片
- 如需图片理解，必须使用支持视觉的模型或 endpoint
- 如果都不可用，必须从控制台获取你自己的 Endpoint ID
