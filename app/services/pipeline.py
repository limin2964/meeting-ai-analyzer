"""语音转写流水线 — 编排完整的转写流程：验证 → 编码 → ASR → 结果。"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from app.services.asr import transcribe_audio
from app.services.clients import get_asr_client

logger = logging.getLogger(__name__)


# ==================== 结果模型 ====================


@dataclass
class TranscriptionResult:
    """单次转写结果，统一封装成功与失败两种状态。

    调用方无需 try/except，直接检查 success 字段即可。
    """

    file_path: str
    """输入文件路径。"""
    text: str = ""
    """识别文本，成功时非空。"""
    success: bool = True
    """True 表示转写成功。"""
    error: str | None = None
    """失败时的错误描述，成功时为 None。"""


# ==================== 流水线 ====================


class TranscriptionPipeline:
    """语音转写流水线。

    封装完整的转写流程：
    1. 验证文件存在性
    2. 将音频文件转为 Base64 Data URL
    3. 调用 Qwen3-ASR-Flash API
    4. 返回结构化结果

    支持单文件和批量转写，所有错误均通过 TranscriptionResult 返回，不抛异常。
    """

    def __init__(self, language: str | None = None, enable_itn: bool = False):
        """初始化流水线。

        Args:
            language: 目标语言代码，None 为自动检测。
            enable_itn: 是否启用逆文本正则化。
        """
        self.language = language
        self.enable_itn = enable_itn
        self._client: "OpenAI | None" = None  # 惰性初始化，避免无凭证时构造失败

    @property
    def client(self) -> "OpenAI":
        """惰性获取 ASR 客户端（首次访问时创建）。"""
        if self._client is None:
            self._client = get_asr_client()
        return self._client

    def run(self, file_path: str) -> TranscriptionResult:
        """对单个文件执行语音转写。

        Args:
            file_path: 音频文件路径（绝对或相对路径）。

        Returns:
            TranscriptionResult：成功时 text 字段为识别文本，失败时 error 字段包含原因。
        """
        path = Path(file_path)

        # —— 文件验证 ——
        if not path.exists():
            logger.warning("文件不存在: %s", file_path)
            return TranscriptionResult(
                file_path=file_path,
                success=False,
                error=f"文件不存在: {file_path}",
            )

        if not path.is_file():
            logger.warning("路径不是文件: %s", file_path)
            return TranscriptionResult(
                file_path=file_path,
                success=False,
                error=f"路径不是文件: {file_path}",
            )

        # —— 调用 ASR ——
        logger.info("开始转写: %s", file_path)

        try:
            text = transcribe_audio(
                file_path=str(path),
                language=self.language,
                enable_itn=self.enable_itn,
                client=self.client,
            )
            logger.info("转写完成: %s → %d 字符", file_path, len(text))
            return TranscriptionResult(
                file_path=file_path,
                text=text,
                success=True,
            )
        except Exception as e:
            logger.error("转写失败: %s — %s", file_path, e)
            return TranscriptionResult(
                file_path=file_path,
                success=False,
                error=str(e),
            )

    def run_batch(self, file_paths: list[str]) -> list[TranscriptionResult]:
        """批量转写多个文件（顺序执行）。

        Args:
            file_paths: 音频文件路径列表。

        Returns:
            TranscriptionResult 列表，与输入顺序一一对应。
        """
        results: list[TranscriptionResult] = []
        for fp in file_paths:
            result = self.run(fp)
            results.append(result)
        return results
