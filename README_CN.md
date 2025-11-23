[项目源码地址](https://github.com/wwwzhouhui/nano_banana2)：

# 🍌 Nano Banana2 文生图插件

> 高质量 AI 文生图 Dify 插件，支持聚鑫 API 和 Gemai 公益站 API，使用 Gemini 3 Pro Image Preview 模型

## ✨ 特性

- 🎨 **Gemini 3 Pro**: 使用 Google Gemini 3 Pro Image Preview 模型生成高质量图像
- 🔄 **双 API 支持**: 支持聚鑫 API（付费）和 Gemai 公益站 API（免费）
- 🚫 **负向提示词**: 支持指定不想要的内容，提高生成质量
- 📐 **宽高比选择**: 支持多种宽高比（1:1, 16:9, 9:16, 4:3, 3:4）
- 🖌️ **风格控制**: 支持多种艺术风格（写实、动漫、油画、水彩、素描）
- 🔢 **批量生成**: 一次生成 1-4 张图像
- 🌡️ **创造力调节**: 通过 temperature 参数控制生成的随机性和创造性
- 🌐 **多语言**: 完整的中英文双语支持
- ⚡ **实时反馈**: 详细的生成进度和状态反馈
- 🛡️ **错误处理**: 完善的错误处理和用户友好的提示

## 🚀 快速开始

### 1. 获取 API Key

#### 方式一：聚鑫 API（付费）

1. 访问 [聚鑫 API 平台](https://api.jxincm.cn/register?aff=SeEB)
2. 创建账户并生成 API Key
3. 复制您的 API Key

#### 方式二：Gemai 公益站（免费）

1. 访问 [Gemai 公益站](https://api.gemai.cc/register?aff=ND9Y)
2. 获取免费的 API Key
3. 复制您的 API Key

**注意**: 您可以同时配置两个 API Key，在使用时选择其中一个

### 2. 安装插件

#### 在线安装（推荐）
在 Dify 插件市场搜索 "Nano Banana2" 并安装

#### 离线安装
1. 下载插件包（.difypkg 文件）
2. 在 Dify 中选择"离线安装"
3. 上传插件包文件

  ![img](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/QQ_1756601091330.png)

![image-20251123161755340](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20251123161755340.png)

### 3. 配置 API Key

安装完成后：
1. 点击插件右侧的"授权"按钮

2. 填写您的 API Key（可以只配置一个，也可以两个都配置）
   - **聚鑫 API Key**: 付费服务，质量稳定
   - **Gemai 公益站 API Key**: 免费服务

3. 点击保存

   ![image-20251123161838278](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20251123161838278.png)

### 4. 开始使用

在 Agent 或 Chatflow 中添加 Nano Banana2 文生图工具：
1. 选择 API 提供商（聚鑫 API 或 Gemai 公益站 API）
2. 输入图像描述即可生成图像

## 🎯 模型说明

本插件使用 **Gemini 3 Pro Image Preview** 模型：

- **模型名称**: gemini-3-pro-image-preview
- **特点**: 高质量图像生成，支持多种风格和宽高比
- **API 提供商**:
  - 聚鑫 API (https://api.jxincm.cn) - 付费服务，质量稳定
  - Gemai 公益站 (https://api.gemai.cc) - 免费服务

## 📖 使用示例

### 基础文生图

**提示词：**

```
2个螃蟹在打架
```

**参数设置：**
- API 提供商: 聚鑫 API 或 Gemai 公益站 API
- 宽高比: 16:9
- 风格: 动漫风格
- 创造力参数: 0.7

![image-20251123162024190](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20251123162024190.png)

最终的效果

![image-20251123162054877](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20251123162054877.png)

**提示词：**

```
创建一个解释[光合作用]的教育信息图。
视觉元素：展示关键组成部分：太阳、一株绿色植物、水（H2O）进入根部、二氧化碳（CO2）进入叶片，以及氧气（O2）被释放。
风格：简洁、扁平化的矢量插图，适合高中科学教科书。使用箭头表示能量和物质的流动。
标签：用简体中文清晰地标注每个元素。
```

**参数设置：**

- API 提供商: 聚鑫 API 或 Gemai 公益站 API
- 宽高比: 16:9
- 风格: 动漫风格
- 创造力参数: 0.7

最终的效果

![image-20251123181434849](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20251123181434849.png)

图片放大

![9cfdca73-8ef7-446c-ad44-6589eb721bea](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/9cfdca73-8ef7-446c-ad44-6589eb721bea.png)

### Agent 使用示例

在 Agent 中添加 Nano Banana2 工具：
1. 创建新的 Agent
2. 在工具列表中选择"Nano Banana2 文生图"
3. 在对话中直接描述想要生成的图像
4. Agent 会自动调用工具生成图像

### Chatflow 使用示例

在 Chatflow 中使用：
1. 添加"工具"节点
2. 选择"Nano Banana2 文生图"工具
3. 配置输入参数（提示词、风格等）
4. 连接到下一个节点

## 🛠️ 开发指南

### 项目结构

```
nano_banana2/
├── manifest.yaml              # 插件配置
├── main.py                   # 插件入口
├── requirements.txt          # 依赖管理
├── provider/                 # 聚鑫 API 服务提供者
│   ├── nano_banana2.yaml
│   └── nano_banana2_provider.py
├── tools/                    # 文生图工具
│   ├── text2image.yaml
│   └── text2image.py
├── README.md                 # 英文文档
├── README_CN.md              # 中文文档
└── PRIVACY.md                # 隐私政策
```

### 核心组件

1. **NanaBanana2Provider**: 管理聚鑫 API 认证和连接验证
2. **Text2ImageTool**: 实现文生图核心逻辑
3. **错误处理**: 完善的异常处理和用户提示

## 🔧 配置说明

### API Key 配置
- 在 Dify 插件配置中输入您的 API Key
- 可以同时配置聚鑫 API Key 和 Gemai API Key
- 使用时选择对应的 API 提供商
- 聚鑫 API 需要确保账户有足够额度
- Gemai 公益站 API 免费使用

### 参数详解

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| api_provider | select | 是 | juxin | API 提供商（juxin/gemai） |
| prompt | string | 是 | - | 图像描述文本（正向提示词） |
| negative_prompt | string | 否 | - | 负向提示词（不想要的内容） |
| num_images | number | 否 | 1 | 生成图像数量（1-4） |
| temperature | number | 否 | 0.7 | 创造力参数（0.0-1.0） |
| aspect_ratio | select | 否 | - | 宽高比（1:1, 16:9, 9:16, 4:3, 3:4） |
| style | select | 否 | - | 风格（realistic, anime, oil-painting, watercolor, sketch） |

### 提示词编写技巧

1. **详细描述**: 提供尽可能详细的场景描述
2. **使用负向提示词**: 排除不想要的元素，提高质量
3. **指定风格**: 明确选择艺术风格
4. **调整创造力**: 根据需求调整 temperature 参数
   - 0.0-0.3: 更稳定，一致性强
   - 0.4-0.7: 平衡创造力和质量（推荐）
   - 0.8-1.0: 更有创意，多样性强

## 📊 性能优化

- **超时设置**: 120 秒请求超时，适合图像生成任务
- **错误重试**: 智能错误处理和重试建议
- **内存管理**: 高效的图像数据处理
- **格式统一**: 统一输出 PNG 格式确保兼容性
- **响应格式兼容**: 支持多种 Gemini API 响应格式

## 🐛 故障排除

### 常见问题

1. **API Key 无效**
   - 检查 API Key 是否正确
   - 确认 API Key 未过期
   - 验证账户状态

2. **生成失败**
   - 检查提示词是否包含敏感内容
   - 简化提示词描述
   - 尝试调整参数设置
   - 检查账户额度是否充足

3. **网络问题**
   - 检查网络连接
   - 确认防火墙设置
   - 尝试稍后重试

4. **图像质量不满意**
   - 使用更详细的提示词
   - 添加负向提示词
   - 调整风格参数
   - 增加 temperature 值增强创造性

## 📝 更新日志

### v0.0.1 (2025-11-23)
- ✨ 初始版本发布
- 🔧 基于聚鑫 API 的完整实现
- 🎨 支持 Gemini 3 Pro Image Preview 模型
- 🚫 支持负向提示词
- 📐 支持多种宽高比和风格
- 🔢 支持批量生成（1-4 张）
- 📖 详细的文档和使用指南

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🔗 相关链接

- [聚鑫 API 平台](https://api.jxincm.cn/register?aff=SeEB)
- [Gemai 公益站](https://api.gemai.cc)
- [Dify 插件开发文档](https://docs.dify.ai/plugins)
- [Gemini API 文档](https://ai.google.dev/gemini-api/docs)

## ⚠️ 注意事项

1. **API Key 配置**: 至少需要配置一个 API Key（聚鑫或 Gemai）
2. **API 额度**: 聚鑫 API 使用需要有效的 API Key 和足够的额度，Gemai 公益站 API 免费使用
3. **API 选择**: 使用时需要选择对应的 API 提供商
4. **内容政策**: 请遵守 API 提供商的使用条款，不要生成违规内容
5. **使用限制**: 请注意 API 调用频率限制
6. **隐私保护**: 本插件不会存储您的提示词和生成的图像

## 💡 提示

- 首次使用建议先用简单提示词测试
- 批量生成时注意控制数量以节省额度
- 定期检查账户余额
- 遇到问题可查看详细的错误提示

---

**Nano Banana2** - 让 AI 图像生成变得简单而强大！ 🍌✨
