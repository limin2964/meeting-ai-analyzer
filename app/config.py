from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ========== 数据库 ==========
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = ""
    db_name: str = "meeting_agent"

    # ========== OpenAI ==========
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o"

    # ========== DashScope 语音转文字（Qwen3-ASR-Flash）==========
    dashscope_api_key: str = ""
    dashscope_workspace_id: str = ""
    asr_model: str = "qwen3-asr-flash"

    # ========== 阿里云语音转文字（旧版，待废弃）==========
    alibaba_access_key_id: str = ""
    alibaba_access_key_secret: str = ""
    alibaba_stt_app_key: str = ""

    # ========== 文件上传 ==========
    upload_dir: str = "./uploads/meetings"
    max_upload_size: int = 100 * 1024 * 1024  # 100 MB

    # ========== JWT 认证 ==========
    jwt_secret_key: str = ""
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    @property
    def db_url(self) -> str:
        return (
            f"mysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


settings = Settings()
