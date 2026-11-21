"""认证路由：注册、登录。"""

from fastapi import APIRouter, HTTPException, status

from app.models import User
from app.schemas import LoginRequest, RegisterRequest, RegisterResponse, TokenResponse
from app.security import create_access_token, hash_password, verify_password

router = APIRouter()


# ==================== 接口 ====================


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest):
    """注册新用户。

    - 用户名已存在时返回 409。
    - 密码经 bcrypt 哈希后存储，永不明文落库。
    """
    existing = await User.get_or_none(username=body.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="用户名已被注册",
        )

    user = await User.create(
        username=body.username,
        password_hash=hash_password(body.password),
        email=body.email,
    )

    return RegisterResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        created_at=user.created_at,
    )


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest):
    """用户登录，返回 JWT 访问令牌。

    - 用户名不存在或密码错误时返回 401。
    """
    user = await User.get_or_none(username=body.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )

    if not verify_password(body.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )

    token = create_access_token(user)
    return TokenResponse(access_token=token)
