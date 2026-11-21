"""Pydantic 请求/响应模型 —— 供路由使用。"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


# ==================== 认证相关 ====================


class RegisterRequest(BaseModel):
    """注册请求体。"""

    username: str = Field(..., min_length=2, max_length=50, description="用户名")
    password: str = Field(..., min_length=6, max_length=100, description="密码")
    email: str | None = Field(default=None, max_length=100, description="邮箱")


class LoginRequest(BaseModel):
    """登录请求体。"""

    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class TokenResponse(BaseModel):
    """JWT 令牌响应。"""

    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field(default="bearer", description="令牌类型")


class RegisterResponse(BaseModel):
    """注册成功响应。"""

    id: int
    username: str
    email: str | None = None
    created_at: datetime


# ==================== 会议相关 ====================


class MeetingResponse(BaseModel):
    """单条会议记录响应，含转写分析内容（如有）。"""

    id: int
    filename: str
    file_size: int
    content_type: str
    status: str = Field(..., description="处理状态：uploaded / transcribing / transcribed / analyzing / completed / failed")
    created_at: datetime
    # 转写分析（可能为空，取决于是否已完成分析）
    transcription: TranscriptionResponse | None = None


class MeetingListResponse(BaseModel):
    """会议列表响应。"""

    total: int
    meetings: list[MeetingResponse]


class UploadResponse(BaseModel):
    """上传成功响应。"""

    id: int
    filename: str
    file_size: int
    content_type: str
    status: str = Field(..., description="处理状态")
    created_at: datetime
    message: str = "上传成功"


# ==================== 转写分析相关 ====================


class TodoItem(BaseModel):
    """单条代办事项。"""

    task: str = Field(..., description="任务描述")
    assignee: str = Field(default="未指定", description="负责人")
    deadline: str = Field(default="未指定", description="截止时间")


class TranscriptionResponse(BaseModel):
    """转写分析结果响应。"""

    id: int
    meeting_id: int
    summary: str = Field(..., description="会议摘要")
    todos: list[TodoItem] = Field(default_factory=list, description="代办事项列表")
    urgency: str = Field(..., description="紧急程度：high / medium / low")
    status: str = Field(..., description="处理状态：pending / processing / completed / failed")
    created_at: datetime


class AnalyzeRequest(BaseModel):
    """分析请求体。"""

    text: str = Field(..., description="待分析的转写文本")


class AnalyzeResponse(BaseModel):
    """分析结果响应（未入库）。"""

    summary: str
    todos: list[TodoItem] = Field(default_factory=list)
    urgency: str
