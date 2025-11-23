from dify_plugin import Plugin, DifyPluginEnv

# 配置插件环境
# 聚鑫 API 图像生成可能需要较长时间,设置 120 秒超时
plugin = Plugin(DifyPluginEnv(MAX_REQUEST_TIMEOUT=120))

if __name__ == '__main__':
    plugin.run()
