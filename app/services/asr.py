"""ASR 服务 — 将本地音频文件转为 Base64 Data URL 并调用语音识别。"""

import base64
from pathlib import Path

from openai import OpenAI

from app.config import settings
from app.services.clients import get_asr_client

# ==================== MIME 类型映射 ====================

AUDIO_MIME_MAP: dict[str, str] = {
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".m4a": "audio/mp4",
    ".aac": "audio/aac",
    ".ogg": "audio/ogg",
    ".flac": "audio/flac",
    ".wma": "audio/x-ms-wma",
    ".webm": "audio/webm",
    ".opus": "audio/opus",
}


# ==================== 文件编码 ====================


def file_to_data_url(file_path: str) -> str:
    """将本地音频文件转换为 Base64 Data URL。

    Args:
        file_path: 本地音频文件的绝对路径。

    Returns:
        格式为 "data:{mime_type};base64,{base64_string}" 的 Data URL。

    Raises:
        ValueError: 文件后缀不在支持列表中时抛出。
    """
    path = Path(file_path)
    suffix = path.suffix.lower()

    mime_type = AUDIO_MIME_MAP.get(suffix)
    if mime_type is None:
        supported = ", ".join(AUDIO_MIME_MAP.keys())
        raise ValueError(f"不支持的音频格式: {suffix}，支持的格式: {supported}")

    base64_str = base64.b64encode(path.read_bytes()).decode()
    return f"data:{mime_type};base64,{base64_str}"


# ==================== 语音转文字 ====================


def transcribe_audio(
    file_path: str,
    language: str | None = None,
    enable_itn: bool = False,
    client: OpenAI | None = None,
) -> str:
    """对本地音频文件执行语音转文字（调用 Qwen3-ASR-Flash）。

    Args:
        file_path: 本地音频文件路径。
        language: 语言代码（如 "zh", "en", "ja"），None 表示自动检测。
        enable_itn: 是否启用逆文本正则化（将口语数字/日期标准化）。
        client: 可选的 OpenAI 客户端实例，不传则自动创建。

    Returns:
        识别出的文字内容。
    """
    if client is None:
        client = get_asr_client()

    data_url = file_to_data_url(file_path)

    # 构建 ASR 选项
    asr_options: dict = {"enable_itn": enable_itn}
    if language:
        asr_options["language"] = language

    completion = client.chat.completions.create(
        model=settings.asr_model,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_audio",
                        "input_audio": {"data": data_url},
                    }
                ],
            }
        ],
        extra_body={"asr_options": asr_options},
    )

    return completion.choices[0].message.content
