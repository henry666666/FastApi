from typing import List, Optional
from sqlalchemy.orm import Session
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import User, UserRole, UserStatus, UserRegistrationRequest, UserResponse
from repository.user_repository import UserRepository
from utils.password_util import hash_password
from utils.validation_util import validate_username, validate_password, validate_phone
from exceptions import DuplicateResourceException

class UserService:
    """
    用户业务逻辑层
    """
    
    @staticmethod
    def register_user(db: Session, request: UserRegistrationRequest) -> UserResponse:
        """
        注册用户
        
        Args:
            db: 数据库会话
            request: 用户注册请求
            
        Returns:
            用户响应对象
            
        Raises:
            DuplicateResourceException: 用户名已存在
        """
        # 验证输入
        validate_username(request.username)
        validate_password(request.password)
        validate_phone(request.phone)
        
        # 检查用户名是否已存在
        if UserRepository.exists_by_username(db, request.username):
            raise DuplicateResourceException("User", "username", request.username)
        
        # 创建用户
        user = User(
            username=request.username,
            password=hash_password(request.password),
            phone=request.phone,
            role=UserRole.CUSTOMER,
            status=UserStatus.ACTIVE
        )
        
        # 保存用户
        saved_user = UserRepository.save(db, user)
        
        # 返回响应对象
        return UserResponse.model_validate(saved_user)
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> UserResponse:
        """
        根据ID获取用户
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            
        Returns:
            用户响应对象
        """
        user = UserRepository.find_by_id(db, user_id)
        return UserResponse.model_validate(user)
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[UserResponse]:
        """
        根据用户名获取用户
        
        Args:
            db: 数据库会话
            username: 用户名
            
        Returns:
            用户响应对象，如果不存在则返回None
        """
        user = UserRepository.find_by_username(db, username)
        if user:
            return UserResponse.model_validate(user)
        return None
    
    @staticmethod
    def get_all_users(db: Session) -> List[UserResponse]:
        """
        获取所有用户
        
        Args:
            db: 数据库会话
            
        Returns:
            用户响应对象列表
        """
        users = UserRepository.find_all(db)
        return [UserResponse.model_validate(user) for user in users]
    
    @staticmethod
    def update_user_status(db: Session, user_id: int, status: UserStatus) -> UserResponse:
        """
        更新用户状态
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            status: 新状态
            
        Returns:
            更新后的用户响应对象
        """
        updated_user = UserRepository.update_status(db, user_id, status)
        return UserResponse.model_validate(updated_user)
    
    @staticmethod
    def get_user_by_username(db: Session, username: str):
        """
        通过用户名获取用户
        """
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def delete_user(db: Session, user_id: int) -> None:
        """
        删除用户（软删除）
        
        Args:
            db: 数据库会话
            user_id: 用户ID
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        user.status = UserStatus.DELETED
        db.commit()