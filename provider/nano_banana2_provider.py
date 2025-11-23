from typing import Any
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from dify_plugin import ToolProvider

class NanaBanana2Provider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        验证聚鑫 API 凭据有效性

        采用简化验证策略：只检查 API Key 格式
        实际的 API Key 有效性将在首次使用时验证
        这样可以避免验证时消耗用户额度或遇到网络问题

        Args:
            credentials: 包含聚鑫 API key 的字典

        Raises:
            ToolProviderCredentialValidationError: 当凭据验证失败时
        """
        try:
            # 1. 检查 API key 是否存在
            api_key = credentials.get("api_key")
            if not api_key:
                raise ToolProviderCredentialValidationError(
                    "聚鑫 API key 不能为空"
                )

            # 2. 检查 API key 是否为字符串类型
            if not isinstance(api_key, str):
                raise ToolProviderCredentialValidationError(
                    "聚鑫 API key 格式不正确"
                )

            # 3. 检查 API key 长度（基本格式验证）
            api_key_stripped = api_key.strip()
            if len(api_key_stripped) < 10:
                raise ToolProviderCredentialValidationError(
                    "聚鑫 API key 长度不正确，请检查是否完整复制"
                )

            # 4. 检查是否包含明显的错误字符
            if any(char in api_key_stripped for char in [' ', '\n', '\t', '\r']):
                raise ToolProviderCredentialValidationError(
                    "聚鑫 API key 包含无效字符，请重新复制"
                )

            # 验证通过
            # 注意：实际的 API Key 有效性将在首次调用图片生成时验证
            # 这样可以避免在授权阶段消耗用户额度

        except ToolProviderCredentialValidationError:
            # 重新抛出已知的验证错误
            raise
        except Exception as e:
            raise ToolProviderCredentialValidationError(
                f"聚鑫 API 凭据验证失败: {str(e)}"
            )
