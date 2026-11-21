"""数据模型定义 —— User 模型 和 Meeting 模型。"""

from tortoise import fields
from tortoise.models import Model


class User(Model):
    """用户模型，密码使用 bcrypt 哈希存储。"""

    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True, description="用户名")
    password_hash = fields.CharField(max_length=128, description="bcrypt 密码哈希")
    email = fields.CharField(max_length=100, null=True, description="邮箱")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")

    class Meta:
        table = "users"


class Meeting(Model):
    """会议记录模型，存储上传的会议文件元信息。

    状态流转：uploaded → transcribing → transcribed → analyzing → completed
             任意阶段出错 → failed
    """

    # 状态常量
    STATUS_UPLOADED = "uploaded"
    STATUS_TRANSCRIBING = "transcribing"
    STATUS_TRANSCRIBED = "transcribed"
    STATUS_ANALYZING = "analyzing"
    STATUS_COMPLETED = "completed"
    STATUS_FAILED = "failed"

    id = fields.IntField(pk=True)
    filename = fields.CharField(max_length=255, description="原始文件名")
    file_path = fields.CharField(max_length=500, description="服务器存储路径")
    file_size = fields.BigIntField(description="文件大小（字节）")
    content_type = fields.CharField(max_length=100, description="MIME 类型")
    status = fields.CharField(
        max_length=20, default=STATUS_UPLOADED, description="处理状态"
    )
    user = fields.ForeignKeyField("models.User", related_name="meetings", description="上传用户")
    created_at = fields.DatetimeField(auto_now_add=True, description="上传时间")

    class Meta:
        table = "meetings"


class Transcription(Model):
    """转写分析结果 — 存储从会议音频转写并提炼后的结构化信息。"""

    # 状态常量
    STATUS_PENDING = "pending"
    STATUS_PROCESSING = "processing"
    STATUS_COMPLETED = "completed"
    STATUS_FAILED = "failed"

    id = fields.IntField(pk=True)
    meeting = fields.ForeignKeyField(
        "models.Meeting", related_name="transcriptions", description="关联的会议记录"
    )
    raw_text = fields.TextField(description="原始转写文本")
    summary = fields.TextField(description="会议摘要")
    todos = fields.JSONField(default=list, description="代办事项列表")
    urgency = fields.CharField(max_length=20, description="紧急程度：high / medium / low")
    status = fields.CharField(
        max_length=20, default=STATUS_PENDING, description="处理状态"
    )
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")

    class Meta:
        table = "transcriptions"
