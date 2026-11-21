"""DashScope 客户端工厂 — 获取 OpenAI 兼容客户端连接云服务。"""

from openai import OpenAI

from app.config import settings


def get_asr_client() -> OpenAI:
    """创建并返回配置好的 DashScope ASR 客户端（OpenAI 兼容模式）。

    从全局配置读取 dashscope_api_key 和 dashscope_workspace_id，
    拼接 DashScope 兼容模式 Base URL。

    Returns:
        OpenAI: 配置了 DashScope base_url 和 api_key 的客户端实例。
    """
    base_url = (
        f"https://{settings.dashscope_workspace_id}"
        f".cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    )
    return OpenAI(
        api_key=settings.dashscope_api_key,
        base_url=base_url,
    )
