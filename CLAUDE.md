# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# 中文回答设置
请始终使用中文回答用户的所有问题和请求。无论用户使用什么语言提问，都应该用中文进行回复。

## 语言规则
- 所有回答都使用简体中文
- 技术术语可以保留英文，但要提供中文解释
- 代码注释使用中文
- 错误信息和提示使用中文
- 文档和说明使用中文

## 例外情况
- 代码本身（变量名、函数名等）可以使用英文
- 命令行指令保持原样
- 配置文件内容根据实际需要决定语言

## Project

"meeting-agent" — FastAPI web service with MySQL 8.0. Python 3.13, managed with `uv`.

## Commands

```bash
uv sync                        # Install dependencies
uv run uvicorn main:app --reload  # Dev server (port 8000, hot reload)
docker compose up -d --wait    # Start MySQL, block until healthy
docker compose exec mysql mysql -uroot -p123456 meeting_agent  # Connect to DB
docker compose down            # Stop MySQL (keeps data volume)
```

## Architecture

- **[main.py](main.py)** — 应用入口，定义 FastAPI app、lifespan、`/health` 健康检查接口。
- **[app/](app/)** — 应用核心模块。
  - `config.py` — `pydantic-settings` 加载 `.env`，集中管理数据库、OpenAI、阿里 STT 参数。
  - `database.py` — `init_db()` / `close_db()`，封装 Tortoise ORM 的初始化和关闭。
  - `models.py` — Tortoise 数据模型（待添加）。
- **[docker-compose.yml](docker-compose.yml)** — MySQL 8.0 on port 3306。数据库 `meeting_agent`，字符集 `utf8mb4`/`utf8mb4_unicode_ci`，凭证 root/123456。数据持久化到命名卷 `meeting_agent_mysql_data`。Healthcheck 通过 `mysqladmin ping`。
- **Dependencies** — FastAPI + Tortoise ORM + uvicorn + pydantic-settings（[pyproject.toml](pyproject.toml)），包管理器 `uv`。
