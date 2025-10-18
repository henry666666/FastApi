from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db
from models import UserRegistrationRequest, UserResponse, UserStatus, Token
from service.user_service import UserService
from config import settings
from utils.password_util import verify_password

router = APIRouter(prefix="/api/users", tags=["users"])

# 登录请求模型
class LoginRequest(BaseModel):
    username: str
    password: str

def create_access_token(data: dict, expires_delta: timedelta = None):
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

@router.post("/login", response_model=Token)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    用户登录接口
    """
    # 通过用户名查找用户
    user = UserService.get_user_by_username(db, login_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 验证密码
    if not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 创建访问令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    获取当前用户信息
    """
    # 直接从请求头获取Authorization
    auth_header = request.headers.get("Authorization")
    
    # 检查Authorization头是否存在
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 检查Bearer前缀
    if not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 提取token
    token = auth_header[7:]
    
    # 验证token
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 查找用户
        user = UserService.get_user_by_username(db, username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 创建并返回UserResponse对象
        return UserResponse(
            id=user.id,
            username=user.username,
            role=user.role,
            phone=user.phone,
            status=user.status,
            created_at=user.created_at
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# 保留其他API端点的简单实现
@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(
    request: UserRegistrationRequest,
    db: Session = Depends(get_db)
):
    """
    用户注册接口
    """
    return UserService.register_user(db, request)

@router.get("/{id}", response_model=UserResponse)
def get_user_by_id(
    id: int,
    db: Session = Depends(get_db)
):
    """
    根据ID查询用户
    """
    return UserService.get_user_by_id(db, id)

@router.get("/username/{username}", response_model=UserResponse)
def get_user_by_username(
    username: str,
    db: Session = Depends(get_db)
):
    """
    根据用户名查询用户
    """
    user = UserService.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with username {username} not found")
    return user

@router.get("", response_model=List[UserResponse])
def get_all_users(
    db: Session = Depends(get_db)
):
    """
    查询所有用户
    """
    return UserService.get_all_users(db)

@router.put("/{id}/status", response_model=UserResponse)
def update_user_status(
    id: int,
    status: UserStatus,
    db: Session = Depends(get_db)
):
    """
    更新用户状态
    """
    return UserService.update_user_status(db, id, status)

@router.delete("/{id}", status_code=204)
def delete_user(
    id: int,
    db: Session = Depends(get_db)
):
    """
    删除用户
    """
    UserService.delete_user(db, id)
    return None