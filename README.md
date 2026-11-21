# 第二大脑 — 智能会议记录分析平台

> 打造你的 AI 外置记忆中枢：上传会议音频 → 语音转文字 → AI 提炼摘要/待办/紧急程度 → 随时回溯。

## 项目简介

**第二大脑**是一个智能会议记录分析平台，帮助你解决"开会太多记不住"的问题。上传会议录音后，系统自动通过 ASR（语音识别）将音频转为文字，再通过 LLM（大语言模型）提炼出会议摘要、待办事项和紧急程度，成为你的外置记忆中枢。

## 技术栈

| 层级 | 技术 |
|------|------|
| **后端框架** | FastAPI (Python 3.13) |
| **数据库** | MySQL 8.0 + Tortoise ORM |
| **语音识别** | 阿里云 DashScope Qwen3-ASR-Flash |
| **文本提炼** | DeepSeek (deepseek-v4-flash)，兼容 OpenAI 接口 |
| **认证** | JWT (HS256) + bcrypt 密码哈希 |
| **前端框架** | Vue 3 (Composition API + `<script setup>`) |
| **样式** | Tailwind CSS 3 |
| **构建工具** | Vite 5 |
| **包管理** | Python: uv / 前端: npm |
| **容器化** | Docker Compose (MySQL) |

## 项目结构

```
meeting agent/
├── main.py                  # FastAPI 应用入口
├── pyproject.toml           # Python 依赖
├── docker-compose.yml       # MySQL 8.0 容器
├── .env                     # 环境变量配置
├── app/                     # 后端核心代码
│   ├── config.py            # 配置管理（pydantic-settings）
│   ├── database.py          # Tortoise ORM 初始化
│   ├── models.py            # User / Meeting / Transcription 数据模型
│   ├── schemas.py           # Pydantic 请求/响应模型
│   ├── security.py          # JWT + bcrypt
│   ├── deps.py              # FastAPI 依赖注入
│   ├── agent_service.py     # LLM 提炼分析（调用 DeepSeek）
│   ├── routers/
│   │   ├── auth.py          # 认证路由（注册/登录）
│   │   └── meetings.py      # 会议路由（上传/列表/详情）
│   └── services/
│       ├── clients.py       # ASR 客户端工厂
│       ├── asr.py           # 语音转文字（Qwen3-ASR-Flash）
│       └── pipeline.py      # 转写流水线编排
├── frontend/                # 前端项目
│   ├── src/
│   │   ├── api/             # Axios 封装 + API 函数
│   │   ├── router/          # Vue Router + 导航守卫
│   │   ├── stores/          # Pinia 状态管理
│   │   ├── components/      # UI 组件
│   │   ├── views/           # 页面组件
│   │   ├── composables/     # 组合式函数
│   │   ├── types/           # TypeScript 类型
│   │   └── utils/           # 工具函数
│   └── vite.config.ts       # Vite 配置 + API 代理
├── uploads/                 # 上传文件存储
└── docs/                    # 文档
```

## 核心业务流程

```
上传会议音频 (mp3/wav/m4a/flac...)
         │
         ▼
   [1. 文件保存] ── 存入 uploads/meetings/
   状态: uploaded
         │
         ▼
   [2. ASR 语音转文字] ── Qwen3-ASR-Flash (DashScope)
   状态: transcribing → transcribed
         │
         ▼
   [3. LLM 内容提炼] ── DeepSeek (deepseek-v4-flash)
   状态: transcribed → analyzing
         │
         ▼
   [4. 结果入库] ── 摘要 + 待办 + 紧急程度
   状态: analyzing → completed
```

**状态流转**: `uploaded` → `transcribing` → `transcribed` → `analyzing` → `completed`（任意阶段出错 → `failed`）

## 数据模型

### User（用户）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | int (PK) | 自增主键 |
| username | varchar(50) | 唯一 |
| password_hash | varchar(128) | bcrypt 哈希 |
| email | varchar(100) | 可选 |
| created_at | datetime | 自动 |

### Meeting（会议记录）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | int (PK) | 自增主键 |
| filename | varchar(255) | 原始文件名 |
| file_path | varchar(500) | 服务器路径 |
| file_size | bigint | 字节数 |
| content_type | varchar(100) | MIME 类型 |
| status | varchar(20) | 处理状态 |
| user_id | FK → users | 上传用户 |
| created_at | datetime | 自动 |

### Transcription（转写分析）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | int (PK) | 自增主键 |
| meeting_id | FK → meetings | 关联会议 |
| raw_text | text | 原始转写文本 |
| summary | text | AI 摘要 |
| todos | json | 待办事项列表 |
| urgency | varchar(20) | high/medium/low |
| status | varchar(20) | 处理状态 |
| created_at | datetime | 自动 |

## API 接口

所有接口前缀在生产环境由反向代理处理，开发环境通过 Vite proxy 转发（`/api` → `http://localhost:8000`）。

### 公开接口

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `/health` | 健康检查（API + 数据库） |
| `POST` | `/auth/register` | 用户注册 |
| `POST` | `/auth/login` | 用户登录，返回 JWT |

### 认证接口（需 Bearer Token）

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `/me` | 获取当前用户信息 |
| `POST` | `/meetings/upload` | 上传会议音频（multipart） |
| `GET` | `/meetings/list_meetings` | 会议列表（按时间倒序） |
| `GET` | `/meetings/get_meeting/{id}` | 会议详情（含转录分析） |

### 请求/响应示例

**注册：**
```json
POST /auth/register
{ "username": "alice", "password": "123456", "email": "alice@example.com" }
→ 201 { "id": 1, "username": "alice", "email": "alice@example.com", "created_at": "..." }
```

**登录：**
```json
POST /auth/login
{ "username": "alice", "password": "123456" }
→ 200 { "access_token": "eyJ...", "token_type": "bearer" }
```

**上传会议（form-data, file 字段）：**
```json
POST /meetings/upload
→ 201 {
  "id": 1, "filename": "meeting.mp3", "file_size": 1448690, "status": "completed",
  "transcription": {
    "summary": "会议讨论了Q3产品路线图...",
    "todos": [{"task": "制定Q3计划", "assignee": "张三", "deadline": "2026-07-28"}],
    "urgency": "high"
  }
}
```

## 快速开始

### 环境要求

- Python 3.13+
- Node.js 20+
- Docker Desktop（运行 MySQL）
- Windows / macOS / Linux

### 1. 克隆项目

```bash
git clone <repo-url> && cd "meeting agent"
```

### 2. 配置环境变量

编辑 `.env` 文件，填入你的 API 密钥：

```bash
# 数据库
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=123456
DB_NAME=meeting_agent

# LLM（DeepSeek）
OPENAI_API_KEY=sk-your-deepseek-key
OPENAI_BASE_URL=https://api.deepseek.com
OPENAI_MODEL=deepseek-v4-flash

# 语音转文字（DashScope）
DASHSCOPE_API_KEY=sk-your-dashscope-key
DASHSCOPE_WORKSPACE_ID=your-workspace-id
ASR_MODEL=qwen3-asr-flash

# JWT
JWT_SECRET_KEY=your-secret-key-change-in-production
```

### 3. 启动后端

```bash
# 安装依赖
uv sync

# 启动 MySQL
docker compose up -d --wait

# 启动 API 服务（http://localhost:8000）
uv run uvicorn main:app --reload
```

### 4. 启动前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
# → http://localhost:3000
```

### 5. 使用

1. 浏览器打开 `http://localhost:3000`
2. 注册账号 → 登录
3. 上传会议音频文件 → 等待自动分析
4. 查看会议详情（摘要、待办、紧急程度）

## 配置项说明

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `db_host` | localhost | MySQL 主机 |
| `db_port` | 3306 | MySQL 端口 |
| `db_name` | meeting_agent | 数据库名 |
| `openai_api_key` | - | LLM API Key（DeepSeek） |
| `openai_base_url` | https://api.deepseek.com | LLM API 地址 |
| `openai_model` | deepseek-v4-flash | LLM 模型 |
| `dashscope_api_key` | - | 阿里云 DashScope Key |
| `asr_model` | qwen3-asr-flash | ASR 模型 |
| `upload_dir` | ./uploads/meetings | 上传目录 |
| `max_upload_size` | 104857600 (100MB) | 上传限制 |
| `jwt_expire_minutes` | 60 | Token 过期时间 |

## 支持的上传格式

.mp3 .wav .m4a .aac .ogg .flac .wma .webm .opus

