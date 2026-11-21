"""数据库初始化与关闭，供 lifespan 调用。"""

from tortoise import Tortoise

from app.config import settings


async def init_db() -> None:
    """初始化 Tortoise ORM，建立数据库连接池。"""
    await Tortoise.init(
        db_url=settings.db_url,
        modules={"models": ["app.models"]},
        _enable_global_fallback=True,
    )
    # 开发阶段自动建表（生产环境应使用 aerich 迁移）
    await Tortoise.generate_schemas(safe=True)

    # 开发阶段自动补齐缺失列（生产环境应使用 aerich 迁移）
    await _ensure_columns()


async def close_db() -> None:
    """关闭所有数据库连接。"""
    await Tortoise.close_connections()


async def _ensure_columns() -> None:
    """安全地补齐已有表中缺失的列（仅开发阶段使用）。

    通过查询 INFORMATION_SCHEMA 判断列是否存在，避免 ALTER TABLE 重复执行报错。
    """
    conn = Tortoise.get_connection("default")

    # meetings 表：添加 status 列
    result = await conn.execute_query(
        "SELECT COUNT(*) AS cnt FROM INFORMATION_SCHEMA.COLUMNS "
        "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'meetings' "
        "AND COLUMN_NAME = 'status'"
    )
    if result[1][0]["cnt"] == 0:
        await conn.execute_query(
            "ALTER TABLE meetings ADD COLUMN status VARCHAR(20) "
            "NOT NULL DEFAULT 'uploaded'"
        )
        print("[init_db] meetings.status 列已添加")

    # transcriptions 表：添加 status 列
    result = await conn.execute_query(
        "SELECT COUNT(*) AS cnt FROM INFORMATION_SCHEMA.COLUMNS "
        "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'transcriptions' "
        "AND COLUMN_NAME = 'status'"
    )
    if result[1][0]["cnt"] == 0:
        await conn.execute_query(
            "ALTER TABLE transcriptions ADD COLUMN status VARCHAR(20) "
            "NOT NULL DEFAULT 'pending'"
        )
        print("[init_db] transcriptions.status 列已添加")
