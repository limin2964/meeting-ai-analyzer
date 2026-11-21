"""Agent 服务 — 将转写文本提炼为摘要、代办事项和紧急标记并入库。

流程：原始文本 → LLM 结构化提取 → Transcription 模型入库
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from openai import OpenAI

from app.config import settings

if TYPE_CHECKING:
    from app.models import Transcription

logger = logging.getLogger(__name__)

# ==================== Prompt 模板 ====================

EXTRACTION_SYSTEM_PROMPT = (
    "你是一个专业的会议记录分析助手。"
    "你的任务是从会议转写文本中提取关键信息，并以严格的 JSON 格式返回。"
    "不要添加任何解释或额外文字，只返回 JSON。"
)

EXTRACTION_USER_TEMPLATE = """请分析以下会议转写文本，提取三部分信息：

1. **摘要** (summary)：2-5 句话概括会议的核心议题、讨论要点和结论。
2. **代办事项** (todos)：列出所有需要后续执行的任务，每项包含：
   - task: 具体任务描述
   - assignee: 负责人（若未提及则填 "未指定"）
   - deadline: 截止时间（若未提及则填 "未指定"）
3. **紧急程度** (urgency)：根据内容判断，值为：
   - "high" — 包含需要立即处理的紧急事项或明确的高优先级标记
   - "medium" — 有需要关注的事项但无紧急危机
   - "low" — 例行会议，无特别紧急内容

返回格式必须严格遵循以下 JSON Schema：
```json
{
  "summary": "会议摘要文本",
  "todos": [
    {"task": "任务描述", "assignee": "负责人", "deadline": "截止时间"}
  ],
  "urgency": "high | medium | low"
}
```

===== 会议转写文本 =====
{text}
===== 文本结束 =====

请输出 JSON："""


def _build_extraction_prompt(text: str) -> str:
    """构建完整的提取 prompt，使用 replace 避免花括号转义问题。"""
    return EXTRACTION_USER_TEMPLATE.replace("{text}", text)


# ==================== 数据模型 ====================


@dataclass
class ExtractionResult:
    """LLM 提炼的原始结果（未入库）。"""

    summary: str = ""
    todos: list[dict] = field(default_factory=list)
    urgency: str = "low"


# ==================== 客户端工厂 ====================


def _get_llm_client() -> OpenAI:
    """获取用于文本提炼的 LLM 客户端（基于 OpenAI 配置）。"""
    return OpenAI(
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
    )


# ==================== 核心方法 ====================


def extract_meeting_info(
    text: str,
    client: OpenAI | None = None,
) -> ExtractionResult:
    """调用 LLM 从会议转写文本中提取摘要、代办事项和紧急程度。

    Args:
        text: 会议转写的原始文本。
        client: 可选的 OpenAI 客户端，不传则根据配置自动创建。

    Returns:
        ExtractionResult: 包含 summary、todos、urgency 的结构化结果。

    Raises:
        ValueError: LLM 返回内容无法解析为有效 JSON 时抛出。
    """
    if client is None:
        client = _get_llm_client()

    user_message = _build_extraction_prompt(text)

    logger.info("开始提取会议信息，文本长度: %d 字符", len(text))

    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": EXTRACTION_SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.1,  # 低温度保证输出稳定
    )

    raw_output = response.choices[0].message.content.strip()
    logger.debug("LLM 原始输出: %s", raw_output[:500])

    # 尝试解析 JSON（处理可能的 markdown 代码块包裹）
    try:
        data = json.loads(raw_output)
    except json.JSONDecodeError:
        # 尝试提取 ```json ... ``` 代码块内容
        if "```json" in raw_output:
            raw_output = raw_output.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_output:
            raw_output = raw_output.split("```")[1].split("```")[0].strip()
        try:
            data = json.loads(raw_output)
        except json.JSONDecodeError as e:
            raise ValueError(f"LLM 返回内容无法解析为 JSON: {e}\n原始输出: {raw_output[:500]}") from e

    # 校验必需字段
    result = ExtractionResult(
        summary=data.get("summary", ""),
        todos=data.get("todos", []),
        urgency=data.get("urgency", "low"),
    )

    # 紧急程度做归一化处理
    if result.urgency not in ("high", "medium", "low"):
        logger.warning("未知的 urgency 值 %r，已重置为 low", result.urgency)
        result.urgency = "low"

    logger.info(
        "提取完成: summary=%d字, todos=%d项, urgency=%s",
        len(result.summary),
        len(result.todos),
        result.urgency,
    )

    return result


async def analyze_and_save(meeting_id: int, text: str) -> Transcription:
    """对转写文本执行 LLM 提炼分析，并将结果存入数据库。

    这是面向业务调用的主要入口：一条 meeting → 一条 transcription 记录。
    同时管理 Meeting 和 Transcription 的状态流转。

    Args:
        meeting_id: 关联的 Meeting 主键。
        text: 转写后的原始文本。

    Returns:
        创建好的 Transcription ORM 实例。

    Raises:
        ValueError: LLM 返回无法解析时抛出，状态已标记为 failed。
    """
    from app.models import Meeting, Transcription

    # 1. 更新 Meeting 状态 → analyzing
    meeting = await Meeting.get(id=meeting_id)
    meeting.status = Meeting.STATUS_ANALYZING
    await meeting.save(update_fields=["status"])

    # 2. 创建 Transcription 记录（processing）
    record = await Transcription.create(
        meeting_id=meeting_id,
        raw_text=text,
        summary="",
        todos=[],
        urgency="low",
        status=Transcription.STATUS_PROCESSING,
    )

    # 3. LLM 提炼
    try:
        extracted = extract_meeting_info(text)
    except Exception:
        # 提炼失败 → 标记 failed
        record.status = Transcription.STATUS_FAILED
        await record.save(update_fields=["status"])
        meeting.status = Meeting.STATUS_FAILED
        await meeting.save(update_fields=["status"])
        logger.exception("提炼失败: meeting_id=%d, transcription_id=%d", meeting_id, record.id)
        raise

    # 4. 入库结果，标记完成
    record.summary = extracted.summary
    record.todos = extracted.todos
    record.urgency = extracted.urgency
    record.status = Transcription.STATUS_COMPLETED
    await record.save(update_fields=["summary", "todos", "urgency", "status"])

    meeting.status = Meeting.STATUS_COMPLETED
    await meeting.save(update_fields=["status"])

    logger.info("转写分析已完成: id=%d, meeting_id=%d", record.id, meeting_id)

    return record
