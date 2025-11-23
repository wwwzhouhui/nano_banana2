from typing import Any
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from dify_plugin import ToolProvider

class NanaBanana2Provider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        验证 API 凭据有效性

        采用简化验证策略：只检查 API Key 格式
        支持聚鑫 API 和 Gemai 公益站 API
        至少需要配置一个 API Key

        Args:
            credentials: 包含 API key 的字典

        Raises:
            ToolProviderCredentialValidationError: 当凭据验证失败时
        """
        try:
            # 获取两种 API Key
            juxin_api_key = credentials.get("juxin_api_key", "")
            gemai_api_key = credentials.get("gemai_api_key", "")

            # 检查至少配置了一个 API Key
            if not juxin_api_key and not gemai_api_key:
                raise ToolProviderCredentialValidationError(
                    "请至少配置一个 API Key（聚鑫 API Key 或 Gemai 公益站 API Key）"
                )

            # 验证聚鑫 API Key 格式（如果提供）
            if juxin_api_key:
                self._validate_api_key_format(juxin_api_key, "聚鑫")

            # 验证 Gemai API Key 格式（如果提供）
            if gemai_api_key:
                self._validate_api_key_format(gemai_api_key, "Gemai")

            # 验证通过
            # 注意：实际的 API Key 有效性将在首次调用图片生成时验证
            # 这样可以避免在授权阶段消耗用户额度

        except ToolProviderCredentialValidationError:
            # 重新抛出已知的验证错误
            raise
        except Exception as e:
            raise ToolProviderCredentialValidationError(
                f"API 凭据验证失败: {str(e)}"
            )

    def _validate_api_key_format(self, api_key: str, provider_name: str) -> None:
        """
        验证 API Key 格式

        Args:
            api_key: API Key 字符串
            provider_name: 提供商名称（用于错误提示）

        Raises:
            ToolProviderCredentialValidationError: 当格式验证失败时
        """
        # 检查是否为字符串类型
        if not isinstance(api_key, str):
            raise ToolProviderCredentialValidationError(
                f"{provider_name} API key 格式不正确"
            )

        # 检查长度
        api_key_stripped = api_key.strip()
        if len(api_key_stripped) < 10:
            raise ToolProviderCredentialValidationError(
                f"{provider_name} API key 长度不正确，请检查是否完整复制"
            )

        # 检查是否包含无效字符
        if any(char in api_key_stripped for char in [' ', '\n', '\t', '\r']):
            raise ToolProviderCredentialValidationError(
                f"{provider_name} API key 包含无效字符，请重新复制"
            )
