import requests
import json
import base64
import re
from collections.abc import Generator
from PIL import Image
from io import BytesIO
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin import Tool

class Text2ImageTool(Tool):
    def _invoke(
        self, tool_parameters: dict
    ) -> Generator[ToolInvokeMessage, None, None]:
        """
        基于聚鑫 API 的 Nano Banana2 文生图工具
        使用 Gemini 3 Pro Image Preview 模型

        Args:
            tool_parameters: 工具参数字典,包含 prompt、negative_prompt 等参数

        Yields:
            ToolInvokeMessage: 工具调用消息,包括进度反馈和最终图像结果
        """
        # 1. 获取 API 配置
        api_key = self.runtime.credentials.get("api_key")
        base_url = "https://api.jxincm.cn"
        model = "gemini-3-pro-image-preview"
        endpoint = f"{base_url}/v1beta/models/{model}:generateContent"

        # 2. 获取和验证参数
        prompt = tool_parameters.get("prompt", "")
        if not prompt:
            yield self.create_text_message("❌ 请输入图像生成提示词")
            return

        negative_prompt = tool_parameters.get("negative_prompt", "")
        num_images = tool_parameters.get("num_images", 1)
        temperature = tool_parameters.get("temperature", 0.7)
        aspect_ratio = tool_parameters.get("aspect_ratio", "")
        style = tool_parameters.get("style", "")

        # 3. 构建请求头
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
            'x-api-key': api_key
        }

        try:
            yield self.create_text_message("🍌 Nano Banana2 正在启动图像生成...")
            yield self.create_text_message("🚀 正在连接聚鑫 API...")
            yield self.create_text_message(f"🤖 使用模型: {model}")
            yield self.create_text_message(f"📝 提示词: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")

            # 4. 构建消息内容
            content_parts = [
                {
                    "text": prompt
                }
            ]

            # 添加负向提示词
            if negative_prompt:
                yield self.create_text_message(f"🚫 负向提示词: {negative_prompt[:100]}{'...' if len(negative_prompt) > 100 else ''}")
                content_parts.append({
                    "text": f"Negative prompt: {negative_prompt}"
                })

            # 5. 构建请求载荷
            payload = {
                "contents": [
                    {
                        "parts": content_parts
                    }
                ],
                "generationConfig": {
                    "temperature": temperature,
                    "candidateCount": num_images
                }
            }

            # 添加可选配置
            if aspect_ratio:
                payload["generationConfig"]["aspectRatio"] = aspect_ratio
                yield self.create_text_message(f"📐 宽高比: {aspect_ratio}")

            if style:
                payload["generationConfig"]["style"] = style
                yield self.create_text_message(f"🎨 风格: {style}")

            yield self.create_text_message(f"🔢 生成数量: {num_images}")
            yield self.create_text_message(f"🌡️ 创造力参数: {temperature}")
            yield self.create_text_message("⏳ 正在生成图像,请稍候...")
            yield self.create_text_message("🎨 AI 正在发挥创意...")

            # 6. 发送请求
            response = requests.post(
                endpoint,
                headers=headers,
                json=payload,
                timeout=120  # 图片生成可能需要较长时间
            )

            # 7. 检查响应状态
            if response.status_code != 200:
                yield self.create_text_message(f"🔧 API 响应状态码: {response.status_code}")
                yield self.create_text_message(f"🔧 响应内容: {response.text[:300]}")

            response.raise_for_status()

            # 8. 解析响应数据
            response_data = response.json()

            # 检查响应结构 - Gemini 标准格式
            candidates = response_data.get("candidates", [])
            if not candidates:
                yield self.create_text_message("❌ API 响应中没有找到生成结果")
                yield self.create_text_message(f"🔧 响应数据: {json.dumps(response_data, indent=2, ensure_ascii=False)[:500]}")
                return

            yield self.create_text_message(f"✅ API 返回了 {len(candidates)} 个候选结果")

            # 9. 处理生成的图像
            image_count = 0
            for candidate_idx, candidate in enumerate(candidates):
                yield self.create_text_message(f"🔍 正在处理第 {candidate_idx + 1} 个候选结果...")

                if "content" not in candidate:
                    yield self.create_text_message(f"⚠️ 候选结果 {candidate_idx + 1} 没有 content 字段")
                    continue

                parts = candidate["content"].get("parts", [])
                if not parts:
                    yield self.create_text_message(f"⚠️ 候选结果 {candidate_idx + 1} 没有 parts 字段")
                    continue

                for part_idx, part in enumerate(parts):
                    # 格式 A: inlineData(驼峰命名)
                    if "inlineData" in part:
                        yield self.create_text_message(f"🎨 找到 inlineData 格式的图片(候选 {candidate_idx + 1}, 部分 {part_idx + 1})")
                        image_data = part["inlineData"]["data"]
                        mime_type = part["inlineData"].get("mimeType", "image/png")

                        success = yield from self._save_image_from_base64(image_data, image_count, mime_type)
                        if success:
                            image_count += 1
                            yield self.create_text_message(f"✅ 第 {image_count} 张图像生成完成！")

                    # 格式 B: inline_data(下划线命名)
                    elif "inline_data" in part:
                        yield self.create_text_message(f"🎨 找到 inline_data 格式的图片(候选 {candidate_idx + 1}, 部分 {part_idx + 1})")
                        image_data = part["inline_data"]["data"]
                        mime_type = part["inline_data"].get("mimeType", "image/png")

                        success = yield from self._save_image_from_base64(image_data, image_count, mime_type)
                        if success:
                            image_count += 1
                            yield self.create_text_message(f"✅ 第 {image_count} 张图像生成完成！")

                    # 格式 C: text 字段包含 Markdown 格式的 data URL
                    elif "text" in part:
                        text = part["text"]
                        yield self.create_text_message(f"📝 找到 text 字段(候选 {candidate_idx + 1}, 部分 {part_idx + 1})")

                        # 尝试从 Markdown 图片格式中提取
                        # 格式: ![image](data:image/png;base64,BASE64_DATA)
                        match = re.search(r'!\[.*?\]\(data:image/([^;]+);base64,([^)]+)\)', text)
                        if match:
                            image_format = match.group(1)
                            image_data = match.group(2)
                            yield self.create_text_message(f"🎨 从 Markdown 格式中提取到图片(格式: {image_format})")

                            success = yield from self._save_image_from_base64(image_data, image_count, f"image/{image_format}")
                            if success:
                                image_count += 1
                                yield self.create_text_message(f"✅ 第 {image_count} 张图像生成完成！")
                        else:
                            # 尝试直接匹配 data URL
                            match = re.search(r'data:image/([^;]+);base64,(.+)', text, re.DOTALL)
                            if match:
                                image_format = match.group(1)
                                image_data = match.group(2).strip()
                                yield self.create_text_message(f"🎨 从 data URL 中提取到图片(格式: {image_format})")

                                success = yield from self._save_image_from_base64(image_data, image_count, f"image/{image_format}")
                                if success:
                                    image_count += 1
                                    yield self.create_text_message(f"✅ 第 {image_count} 张图像生成完成！")
                            else:
                                # 显示文本内容摘要
                                text_preview = text[:200] + ('...' if len(text) > 200 else '')
                                yield self.create_text_message(f"ℹ️ text 字段不包含图片,内容预览: {text_preview}")

            if image_count == 0:
                yield self.create_text_message("❌ 没有生成任何图像")
                yield self.create_text_message("💡 可能的原因:")
                yield self.create_text_message("1. 提示词包含敏感内容")
                yield self.create_text_message("2. API 返回格式不符合预期")
                yield self.create_text_message("3. 模型暂时不可用")
                return

            yield self.create_text_message(f"🎉 成功生成 {image_count} 张图像！")
            yield self.create_text_message("🍌 Nano Banana2 图像生成任务完成！")
            yield self.create_text_message("🎉 感谢使用 Nano Banana2 文生图服务！")

        except requests.exceptions.HTTPError as e:
            # HTTP 错误处理
            if e.response.status_code == 401:
                yield self.create_text_message("❌ 聚鑫 API Key 无效,请检查您的 API Key")
                yield self.create_text_message("💡 请前往 https://api.jxincm.cn 获取有效的 API Key")
            elif e.response.status_code == 403:
                yield self.create_text_message("❌ 聚鑫 API Key 无权限访问该服务")
                yield self.create_text_message("💡 请检查您的 API Key 权限设置")
            elif e.response.status_code == 429:
                yield self.create_text_message("❌ API 调用频率过高,请稍后再试")
                yield self.create_text_message("💡 建议等待几分钟后重试")
            elif e.response.status_code == 500:
                yield self.create_text_message("❌ 聚鑫 API 服务器内部错误")
                yield self.create_text_message("💡 可能的解决方案:")
                yield self.create_text_message("1. 检查提示词是否包含敏感内容")
                yield self.create_text_message("2. 稍后重试")
            else:
                yield self.create_text_message(f"❌ HTTP 错误: {e.response.status_code}")
                if hasattr(e.response, 'text'):
                    yield self.create_text_message(f"🔧 错误详情: {e.response.text[:200]}")

        except requests.exceptions.Timeout:
            yield self.create_text_message("❌ 请求超时,请检查网络连接或稍后重试")
            yield self.create_text_message("💡 建议检查网络连接状态")

        except requests.exceptions.RequestException as e:
            yield self.create_text_message(f"❌ 网络请求错误: {str(e)}")
            yield self.create_text_message("💡 请检查网络连接是否正常")

        except json.JSONDecodeError as e:
            yield self.create_text_message(f"❌ API 响应解析错误: {str(e)}")
            yield self.create_text_message("🔧 这可能是聚鑫 API 返回了非 JSON 格式的响应")

        except Exception as e:
            yield self.create_text_message(f"❌ 生成图像时出现未知错误: {str(e)}")
            yield self.create_text_message("🔧 请联系技术支持或查看详细日志")
            # 在开发环境中可以添加详细的错误信息
            import traceback
            yield self.create_text_message(f"🔧 调试信息: {traceback.format_exc()}")

    def _save_image_from_base64(self, base64_data: str, image_index: int, mime_type: str = "image/png") -> Generator[ToolInvokeMessage, None, bool]:
        """
        从 base64 数据保存图像并返回给 Dify

        Args:
            base64_data: base64 编码的图像数据
            image_index: 图像索引
            mime_type: MIME 类型

        Yields:
            ToolInvokeMessage: 包含图像数据的消息

        Returns:
            bool: 是否成功保存
        """
        try:
            # 移除可能的空白字符
            base64_data = base64_data.strip()

            # 解码 base64
            image_bytes = base64.b64decode(base64_data)

            # 验证图像数据
            image = Image.open(BytesIO(image_bytes))

            # 转换为 PNG 格式(统一格式)
            img_byte_arr = BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            # 返回图像给 Dify
            yield self.create_blob_message(
                blob=img_byte_arr,
                meta={"mime_type": "image/png"}
            )

            return True

        except Exception as e:
            yield self.create_text_message(f"❌ 处理图像时出错: {str(e)}")
            return False
