"""FastAPI 依赖注入：从 JWT Bearer token 解析当前用户。"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.models import User
from app.security import decode_access_token

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    """从 Authorization header 的 Bearer token 中解析并返回当前用户。

    用法：
        @router.get("/me")
        async def me(current_user: User = Depends(get_current_user)):
            return {"username": current_user.username}
    """
    token = credentials.credentials
    payload = decode_access_token(token)

    user = await User.get_or_none(id=int(payload["sub"]))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
        )

    return user
