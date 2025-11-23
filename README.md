[中文](./README_CN.md) ｜ English

[Project Source Code](https://github.com/wwwzhouhui/nano_banana2):

# 🍌 Nano Banana2 Juxin API Text-to-Image Plugin

> High-quality AI text-to-image Dify plugin based on Juxin API, using Gemini 3 Pro Image Preview model

## ✨ Features

- 🎨 **Gemini 3 Pro**: Uses Google Gemini 3 Pro Image Preview model for high-quality image generation
- 🚫 **Negative Prompts**: Supports specifying unwanted content to improve generation quality
- 📐 **Aspect Ratio Selection**: Supports multiple aspect ratios (1:1, 16:9, 9:16, 4:3, 3:4)
- 🖌️ **Style Control**: Supports various artistic styles (realistic, anime, oil-painting, watercolor, sketch)
- 🔢 **Batch Generation**: Generate 1-4 images at once
- 🌡️ **Creativity Control**: Control randomness and creativity through temperature parameter
- 🌐 **Multilingual**: Complete bilingual support in Chinese and English
- ⚡ **Real-time Feedback**: Detailed generation progress and status feedback
- 🛡️ **Error Handling**: Comprehensive error handling with user-friendly prompts

## 🚀 Quick Start

### 1. Get Juxin API Key

1. Visit [Juxin API Platform](https://api.jxincm.cn/register?aff=SeEB)
2. Create an account and generate an API Key
3. Copy your API Key

### 2. Install Plugin

#### Online Installation (Recommended)
Search for "Nano Banana2" in the Dify plugin marketplace and install

#### Offline Installation
1. Download the plugin package (.difypkg file)
2. Select "Offline Installation" in Dify
3. Upload the plugin package file

  ![img](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/QQ_1756601091330.png)

![image-20251123161755340](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20251123161755340.png)

### 3. Configure API Key

After installation:
1. Click the "Authorize" button on the right side of the plugin

2. Fill in your Juxin API Key

3. Click Save

   ![image-20251123161838278](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20251123161838278.png)

### 4. Start Using

Add the Nano Banana2 text-to-image tool in Agent or Chatflow to start using it

## 🎯 Model Information

This plugin uses the **Gemini 3 Pro Image Preview** model provided by Juxin API:

- **Model Name**: gemini-3-pro-image-preview
- **Features**: High-quality image generation, supports multiple styles and aspect ratios
- **API Provider**: Juxin API (https://api.jxincm.cn)

## 📖 Usage Examples

### Basic Text-to-Image

**Prompt:**
```
Two crabs fighting
```

**Parameter Settings:**
- Aspect Ratio: 16:9
- Style: anime
- Temperature: 0.7

![image-20251123162024190](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20251123162024190.png)

Final Result:

![image-20251123162054877](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20251123162054877.png)

### Agent Usage Example

Adding Nano Banana2 tool in Agent:
1. Create a new Agent
2. Select "Nano Banana2 Text-to-Image" from the tools list
3. Describe the desired image directly in the conversation
4. Agent will automatically call the tool to generate images

### Chatflow Usage Example

Using in Chatflow:
1. Add a "Tool" node
2. Select "Nano Banana2 Text-to-Image" tool
3. Configure input parameters (prompt, style, etc.)
4. Connect to the next node

## 🛠️ Development Guide

### Project Structure

```
nano_banana2/
├── manifest.yaml              # Plugin configuration
├── main.py                   # Plugin entry point
├── requirements.txt          # Dependency management
├── provider/                 # Juxin API provider
│   ├── nano_banana2.yaml
│   └── nano_banana2_provider.py
├── tools/                    # Text-to-image tool
│   ├── text2image.yaml
│   └── text2image.py
├── README.md                 # English documentation
├── README_CN.md              # Chinese documentation
└── PRIVACY.md                # Privacy policy
```

### Core Components

1. **NanaBanana2Provider**: Manages Juxin API authentication and connection validation
2. **Text2ImageTool**: Implements core text-to-image logic
3. **Error Handling**: Comprehensive exception handling and user prompts

## 🔧 Configuration Guide

### API Key Configuration
- Enter your Juxin API Key in the Dify plugin configuration
- Ensure your account has sufficient credits

### Parameter Details

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| prompt | string | Yes | - | Image description text (positive prompt) |
| negative_prompt | string | No | - | Negative prompt (unwanted content) |
| num_images | number | No | 1 | Number of images to generate (1-4) |
| temperature | number | No | 0.7 | Creativity parameter (0.0-1.0) |
| aspect_ratio | select | No | - | Aspect ratio (1:1, 16:9, 9:16, 4:3, 3:4) |
| style | select | No | - | Style (realistic, anime, oil-painting, watercolor, sketch) |

### Prompt Writing Tips

1. **Detailed Description**: Provide as detailed a scene description as possible
2. **Use Negative Prompts**: Exclude unwanted elements to improve quality
3. **Specify Style**: Clearly choose an artistic style
4. **Adjust Creativity**: Adjust temperature parameter based on needs
   - 0.0-0.3: More stable, consistent
   - 0.4-0.7: Balanced creativity and quality (recommended)
   - 0.8-1.0: More creative, diverse

## 📊 Performance Optimization

- **Timeout Settings**: 120-second request timeout suitable for image generation tasks
- **Error Retry**: Intelligent error handling and retry suggestions
- **Memory Management**: Efficient image data processing
- **Format Standardization**: Unified PNG output format for compatibility
- **Response Format Compatibility**: Supports multiple Gemini API response formats

## 🐛 Troubleshooting

### Common Issues

1. **Invalid API Key**
   - Check if the API Key is correct
   - Confirm the API Key hasn't expired
   - Verify account status

2. **Generation Failure**
   - Check if prompts contain sensitive content
   - Simplify prompt descriptions
   - Try adjusting parameter settings
   - Check if account has sufficient credits

3. **Network Issues**
   - Check network connection
   - Confirm firewall settings
   - Try again later

4. **Unsatisfactory Image Quality**
   - Use more detailed prompts
   - Add negative prompts
   - Adjust style parameters
   - Increase temperature value for more creativity

## 📝 Changelog

### v0.0.1 (2025-11-23)
- ✨ Initial release
- 🔧 Complete implementation based on Juxin API
- 🎨 Support for Gemini 3 Pro Image Preview model
- 🚫 Support for negative prompts
- 📐 Support for multiple aspect ratios and styles
- 🔢 Support for batch generation (1-4 images)
- 📖 Detailed documentation and usage guide

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 📄 License

MIT License

## 🔗 Related Links

- [Juxin API Platform](https://api.jxincm.cn/register?aff=SeEB)
- [Dify Plugin Development Documentation](https://docs.dify.ai/plugins)
- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)

## ⚠️ Important Notes

1. **API Credits**: Using this plugin requires a valid Juxin API Key and sufficient credits
2. **Content Policy**: Please comply with Juxin API's terms of use, do not generate prohibited content
3. **Usage Limits**: Be aware of API call rate limits
4. **Privacy Protection**: This plugin does not store your prompts and generated images

## 💡 Tips

- For first-time use, test with simple prompts first
- Control the quantity when batch generating to save credits
- Regularly check account balance
- Refer to detailed error messages when encountering problems

---

**Nano Banana2** - Making AI image generation simple and powerful! 🍌✨
