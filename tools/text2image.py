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
        Nano Banana2 文生图工具
        支持聚鑫 API 和 Gemai 公益站 API
        使用 Gemini 3 Pro Image Preview 模型

        Args:
            tool_parameters: 工具参数字典

        Yields:
            ToolInvokeMessage: 工具调用消息
        """
        # 1. 获取 API 提供商选择
        api_provider = tool_parameters.get("api_provider", "juxin")

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

        # 3. 根据 API 提供商选择不同的处理逻辑
        if api_provider == "gemai":
            yield from self._invoke_gemai_api(
                prompt, negative_prompt, num_images, temperature, aspect_ratio, style
            )
        else:
            yield from self._invoke_juxin_api(
                prompt, negative_prompt, num_images, temperature, aspect_ratio, style
            )

    def _invoke_juxin_api(
        self,
        prompt: str,
        negative_prompt: str,
        num_images: int,
        temperature: float,
        aspect_ratio: str,
        style: str
    ) -> Generator[ToolInvokeMessage, None, None]:
        """
        调用聚鑫 API 生成图像
        使用 Gemini generateContent 格式
        """
        # 获取 API 配置
        api_key = self.runtime.credentials.get("juxin_api_key")
        if not api_key:
            yield self.create_text_message("❌ 未配置聚鑫 API Key")
            yield self.create_text_message("💡 请在插件设置中配置聚鑫 API Key")
            return

        base_url = "https://api.jxincm.cn"
        model = "gemini-3-pro-image-preview"
        endpoint = f"{base_url}/v1beta/models/{model}:generateContent"

        # 构建请求头
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

            # 构建消息内容
            content_parts = [{"text": prompt}]

            # 添加负向提示词
            if negative_prompt:
                yield self.create_text_message(f"🚫 负向提示词: {negative_prompt[:100]}{'...' if len(negative_prompt) > 100 else ''}")
                content_parts.append({"text": f"Negative prompt: {negative_prompt}"})

            # 构建请求载荷
            payload = {
                "contents": [{"parts": content_parts}],
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

            # 发送请求
            response = requests.post(endpoint, headers=headers, json=payload, timeout=120)

            if response.status_code != 200:
                yield self.create_text_message(f"🔧 API 响应状态码: {response.status_code}")
                yield self.create_text_message(f"🔧 响应内容: {response.text[:300]}")

            response.raise_for_status()
            response_data = response.json()

            # 处理 Gemini 格式响应
            yield from self._process_juxin_response(response_data)

        except requests.exceptions.HTTPError as e:
            yield from self._handle_http_error(e, "聚鑫")
        except requests.exceptions.Timeout:
            yield self.create_text_message("❌ 请求超时,请检查网络连接或稍后重试")
        except requests.exceptions.RequestException as e:
            yield self.create_text_message(f"❌ 网络请求错误: {str(e)}")
        except Exception as e:
            yield self.create_text_message(f"❌ 生成图像时出现错误: {str(e)}")

    def _invoke_gemai_api(
        self,
        prompt: str,
        negative_prompt: str,
        num_images: int,
        temperature: float,
        aspect_ratio: str,
        style: str
    ) -> Generator[ToolInvokeMessage, None, None]:
        """
        调用 Gemai 公益站 API 生成图像
        使用 OpenAI Chat Completions 格式
        """
        # 获取 API 配置
        api_key = self.runtime.credentials.get("gemai_api_key")
        if not api_key:
            yield self.create_text_message("❌ 未配置 Gemai API Key")
            yield self.create_text_message("💡 请在插件设置中配置 Gemai 公益站 API Key")
            return

        base_url = "https://api.gemai.cc"
        model = "gemini-3-pro-image-preview"
        endpoint = f"{base_url}/v1/chat/completions"

        # 构建请求头
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }

        try:
            yield self.create_text_message("🍌 Nano Banana2 正在启动图像生成...")
            yield self.create_text_message("🚀 正在连接 Gemai 公益站 API...")
            yield self.create_text_message(f"🤖 使用模型: {model}")
            yield self.create_text_message(f"📝 提示词: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")

            # 构建完整提示词
            full_prompt = prompt

            # 添加风格参数到提示词
            if style:
                style_map = {
                    "realistic": "photorealistic style",
                    "anime": "anime style",
                    "oil-painting": "oil painting style",
                    "watercolor": "watercolor painting style",
                    "sketch": "sketch drawing style"
                }
                style_text = style_map.get(style, style)
                full_prompt = f"{prompt}, {style_text}"
                yield self.create_text_message(f"🎨 风格: {style}")

            # 添加宽高比参数到提示词
            if aspect_ratio:
                full_prompt = f"{full_prompt}, aspect ratio {aspect_ratio}"
                yield self.create_text_message(f"📐 宽高比: {aspect_ratio}")

            # 添加负向提示词
            if negative_prompt:
                yield self.create_text_message(f"🚫 负向提示词: {negative_prompt[:100]}{'...' if len(negative_prompt) > 100 else ''}")
                full_prompt = f"{full_prompt}\n\nNegative prompt: {negative_prompt}"

            # 构建 OpenAI 格式请求载荷
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": full_prompt}],
                "temperature": temperature,
                "max_tokens": 4096
            }

            # 添加多图参数
            if num_images > 1:
                payload["n"] = num_images

            yield self.create_text_message(f"🔢 生成数量: {num_images}")
            yield self.create_text_message(f"🌡️ 创造力参数: {temperature}")
            yield self.create_text_message("⏳ 正在生成图像,请稍候...")

            # 发送请求
            response = requests.post(endpoint, headers=headers, json=payload, timeout=120)

            if response.status_code != 200:
                yield self.create_text_message(f"🔧 API 响应状态码: {response.status_code}")
                yield self.create_text_message(f"🔧 响应内容: {response.text[:300]}")

            response.raise_for_status()
            response_data = response.json()

            # 处理 OpenAI 格式响应
            yield from self._process_gemai_response(response_data)

        except requests.exceptions.HTTPError as e:
            yield from self._handle_http_error(e, "Gemai")
        except requests.exceptions.Timeout:
            yield self.create_text_message("❌ 请求超时,请检查网络连接或稍后重试")
        except requests.exceptions.RequestException as e:
            yield self.create_text_message(f"❌ 网络请求错误: {str(e)}")
        except Exception as e:
            yield self.create_text_message(f"❌ 生成图像时出现错误: {str(e)}")

    def _process_juxin_response(self, response_data: dict) -> Generator[ToolInvokeMessage, None, None]:
        """
        处理聚鑫 API (Gemini 格式) 响应
        """
        candidates = response_data.get("candidates", [])
        if not candidates:
            yield self.create_text_message("❌ API 响应中没有找到生成结果")
            return

        yield self.create_text_message(f"✅ API 返回了 {len(candidates)} 个候选结果")

        image_count = 0
        for candidate_idx, candidate in enumerate(candidates):
            if "content" not in candidate:
                continue

            parts = candidate["content"].get("parts", [])
            for part_idx, part in enumerate(parts):
                image_data = None
                mime_type = "image/png"

                # 格式 A: inlineData
                if "inlineData" in part:
                    image_data = part["inlineData"]["data"]
                    mime_type = part["inlineData"].get("mimeType", "image/png")
                # 格式 B: inline_data
                elif "inline_data" in part:
                    image_data = part["inline_data"]["data"]
                    mime_type = part["inline_data"].get("mimeType", "image/png")
                # 格式 C: text 字段包含图片
                elif "text" in part:
                    text = part["text"]
                    # 尝试从 Markdown 格式提取
                    match = re.search(r'!\[.*?\]\(data:image/([^;]+);base64,([^)]+)\)', text)
                    if match:
                        image_data = match.group(2)
                    else:
                        # 尝试直接匹配 data URL
                        match = re.search(r'data:image/([^;]+);base64,(.+)', text, re.DOTALL)
                        if match:
                            image_data = match.group(2).strip()

                if image_data:
                    try:
                        image_bytes = base64.b64decode(image_data.strip())
                        image = Image.open(BytesIO(image_bytes))
                        img_byte_arr = BytesIO()
                        image.save(img_byte_arr, format='PNG')
                        img_byte_arr = img_byte_arr.getvalue()

                        yield self.create_blob_message(
                            blob=img_byte_arr,
                            meta={"mime_type": "image/png"}
                        )
                        image_count += 1
                        yield self.create_text_message(f"✅ 第 {image_count} 张图像生成完成！")
                    except Exception as e:
                        yield self.create_text_message(f"❌ 处理图像失败: {str(e)}")

        if image_count == 0:
            yield self.create_text_message("❌ 没有生成任何图像")
            return

        yield self.create_text_message(f"🎉 成功生成 {image_count} 张图像！")
        yield self.create_text_message("🍌 Nano Banana2 图像生成任务完成！")

    def _process_gemai_response(self, response_data: dict) -> Generator[ToolInvokeMessage, None, None]:
        """
        处理 Gemai API (OpenAI 格式) 响应
        """
        choices = response_data.get("choices", [])
        if not choices:
            yield self.create_text_message("❌ API 响应中没有找到生成结果")
            return

        yield self.create_text_message(f"✅ API 返回了 {len(choices)} 个选择")

        image_count = 0
        for choice_idx, choice in enumerate(choices):
            message = choice.get("message", {})
            content = message.get("content", "")

            if not isinstance(content, str):
                continue

            # 从内容中提取图片
            images_data = []

            # 方式1: Markdown 格式
            markdown_pattern = r'!\[.*?\]\(data:image/([^;]+);base64,([^)]+)\)'
            matches = re.findall(markdown_pattern, content)
            if matches:
                for image_format, base64_data in matches:
                    images_data.append(base64_data.strip())
            else:
                # 方式2: 直接 data URL
                data_url_pattern = r'data:image/([^;]+);base64,([A-Za-z0-9+/=\n\r]+)'
                matches = re.findall(data_url_pattern, content, re.DOTALL)
                if matches:
                    for image_format, base64_data in matches:
                        clean_data = base64_data.replace('\n', '').replace('\r', '').strip()
                        images_data.append(clean_data)

            # 处理提取的图片
            for image_data in images_data:
                try:
                    image_bytes = base64.b64decode(image_data)
                    image = Image.open(BytesIO(image_bytes))
                    img_byte_arr = BytesIO()
                    image.save(img_byte_arr, format='PNG')
                    img_byte_arr = img_byte_arr.getvalue()

                    yield self.create_blob_message(
                        blob=img_byte_arr,
                        meta={"mime_type": "image/png"}
                    )
                    image_count += 1
                    yield self.create_text_message(f"✅ 第 {image_count} 张图像生成完成！")
                except Exception as e:
                    yield self.create_text_message(f"❌ 处理图像失败: {str(e)}")

        if image_count == 0:
            yield self.create_text_message("❌ 没有生成任何图像")
            return

        yield self.create_text_message(f"🎉 成功生成 {image_count} 张图像！")
        yield self.create_text_message("🍌 Nano Banana2 图像生成任务完成！")

    def _handle_http_error(self, e, provider_name: str) -> Generator[ToolInvokeMessage, None, None]:
        """
        处理 HTTP 错误
        """
        if e.response.status_code == 401:
            yield self.create_text_message(f"❌ {provider_name} API Key 无效,请检查您的 API Key")
        elif e.response.status_code == 403:
            yield self.create_text_message(f"❌ {provider_name} API Key 无权限访问该服务")
        elif e.response.status_code == 429:
            yield self.create_text_message("❌ API 调用频率过高,请稍后再试")
        elif e.response.status_code == 500:
            yield self.create_text_message(f"❌ {provider_name} API 服务器内部错误")
        else:
            yield self.create_text_message(f"❌ HTTP 错误: {e.response.status_code}")
            if hasattr(e.response, 'text'):
                yield self.create_text_message(f"🔧 错误详情: {e.response.text[:200]}")
