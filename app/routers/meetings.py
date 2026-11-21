"""会议路由：上传、列表、详情。"""

import os
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status

from app.config import settings
from app.deps import get_current_user
from app.models import Meeting, Transcription, User
from app.schemas import (
    MeetingListResponse,
    MeetingResponse,
    TodoItem,
    TranscriptionResponse,
    UploadResponse,
)

router = APIRouter()


# ==================== 工具函数 ====================


def _ensure_upload_dir() -> Path:
    """确保上传目录存在，不存在则递归创建。"""
    upload_path = Path(settings.upload_dir)
    upload_path.mkdir(parents=True, exist_ok=True)
    return upload_path


def _generate_stored_filename(original_filename: str) -> str:
    """生成唯一存储文件名：UUID + 原始后缀，避免冲突。"""
    suffix = Path(original_filename).suffix
    return f"{uuid.uuid4().hex}{suffix}"


def _build_transcription_response(transcription: Transcription) -> TranscriptionResponse:
    """将 ORM 模型转为 TranscriptionResponse。"""
    todos = [TodoItem(**t) for t in (transcription.todos or [])]
    return TranscriptionResponse(
        id=transcription.id,
        meeting_id=transcription.meeting_id,
        summary=transcription.summary,
        todos=todos,
        urgency=transcription.urgency,
        status=transcription.status,
        created_at=transcription.created_at,
    )


# ==================== 接口 ====================


@router.post("/upload", response_model=MeetingResponse, status_code=status.HTTP_201_CREATED)
async def upload_meeting(
    file: UploadFile,
    current_user: User = Depends(get_current_user),
):
    """上传会议文件，自动完成语音转文字和内容提炼。

    流水线：保存文件 → ASR 转写 → LLM 提炼（摘要/代办/紧急程度）→ 入库。

    - 需要 Bearer token 认证。
    - 文件大小限制由配置项 `max_upload_size` 控制（默认 100 MB）。
    - 返回完整的会议详情（含 transcription）。
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="未提供文件名",
        )

    # —— 1. 保存文件 ——
    content = await file.read()
    if len(content) > settings.max_upload_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"文件大小超过限制（最大 {settings.max_upload_size // (1024 * 1024)} MB）",
        )

    upload_dir = _ensure_upload_dir()
    stored_filename = _generate_stored_filename(file.filename)
    file_path = upload_dir / stored_filename
    file_path.write_bytes(content)

    # —— 2. 创建 Meeting 记录 ——
    meeting = await Meeting.create(
        filename=file.filename,
        file_path=str(file_path),
        file_size=len(content),
        content_type=file.content_type or "application/octet-stream",
        user=current_user,
    )

    # —— 3. ASR 语音转文字 ——
    from app.services.pipeline import TranscriptionPipeline

    meeting.status = Meeting.STATUS_TRANSCRIBING
    await meeting.save(update_fields=["status"])

    pipeline = TranscriptionPipeline(language="zh", enable_itn=True)
    asr_result = pipeline.run(str(file_path))

    if not asr_result.success:
        meeting.status = Meeting.STATUS_FAILED
        await meeting.save(update_fields=["status"])
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"语音转写失败: {asr_result.error}",
        )

    # —— 4. LLM 提炼分析 ——
    from app.agent_service import analyze_and_save

    meeting.status = Meeting.STATUS_TRANSCRIBED
    await meeting.save(update_fields=["status"])

    try:
        transcription = await analyze_and_save(
            meeting_id=meeting.id, text=asr_result.text
        )
    except Exception as e:
        meeting.status = Meeting.STATUS_FAILED
        await meeting.save(update_fields=["status"])
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"内容分析失败: {e}",
        )

    # —— 5. 返回完整结果 ——
    return MeetingResponse(
        id=meeting.id,
        filename=meeting.filename,
        file_size=meeting.file_size,
        content_type=meeting.content_type,
        status=meeting.status,
        created_at=meeting.created_at,
        transcription=_build_transcription_response(transcription),
    )


@router.get("/list_meetings", response_model=MeetingListResponse)
async def list_meetings(
    current_user: User = Depends(get_current_user),
):
    """获取当前用户的所有会议记录列表。

    - 需要 Bearer token 认证。
    - 按上传时间倒序排列。
    """
    meetings = (
        await Meeting.filter(user=current_user)
        .order_by("-created_at")
        .all()
    )

    meeting_list = [
        MeetingResponse(
            id=m.id,
            filename=m.filename,
            file_size=m.file_size,
            content_type=m.content_type,
            status=m.status,
            created_at=m.created_at,
        )
        for m in meetings
    ]

    return MeetingListResponse(total=len(meeting_list), meetings=meeting_list)


@router.get("/get_meeting/{meeting_id}", response_model=MeetingResponse)
async def get_meeting(
    meeting_id: int,
    current_user: User = Depends(get_current_user),
):
    """获取单条会议记录详情。

    - 需要 Bearer token 认证。
    - 只能查看自己上传的会议记录。
    """
    meeting = await Meeting.get_or_none(id=meeting_id, user=current_user)

    if meeting is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="会议记录不存在",
        )

    # 获取最新的转写分析记录
    transcription = await (
        Transcription.filter(meeting=meeting)
        .order_by("-created_at")
        .first()
    )

    transcription_data = None
    if transcription is not None:
        todos = [TodoItem(**t) for t in (transcription.todos or [])]
        transcription_data = TranscriptionResponse(
            id=transcription.id,
            meeting_id=transcription.meeting_id,
            summary=transcription.summary,
            todos=todos,
            urgency=transcription.urgency,
            status=transcription.status,
            created_at=transcription.created_at,
        )

    return MeetingResponse(
        id=meeting.id,
        filename=meeting.filename,
        file_size=meeting.file_size,
        content_type=meeting.content_type,
        status=meeting.status,
        created_at=meeting.created_at,
        transcription=transcription_data,
    )
