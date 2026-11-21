from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from tortoise import Tortoise

from app.database import close_db, init_db
from app.deps import get_current_user
from app.models import User
from app.routers.auth import router as auth_router
from app.routers.meetings import router as meetings_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # 启动：初始化数据库连接
    await init_db()
    yield
    # 关闭：释放数据库连接
    await close_db()


app = FastAPI(lifespan=lifespan)

# 注册认证路由
app.include_router(auth_router, prefix="/auth", tags=["认证"])

# 注册会议路由
app.include_router(meetings_router, prefix="/meetings", tags=["会议"])


@app.get("/health")
async def health():
    """健康检查：验证 API 与数据库连通性。"""
    try:
        conn = Tortoise.get_connection("default")
        await conn.execute_query("SELECT 1")
    except Exception:
        return {"status": "unhealthy", "database": "unreachable"}

    return {"status": "healthy", "database": "connected"}


@app.get("/me", tags=["用户"])
async def me(current_user: User = Depends(get_current_user)):
    """获取当前登录用户信息（需 Bearer token）。"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "created_at": current_user.created_at.isoformat(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
