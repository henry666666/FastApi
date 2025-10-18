from typing import Optional, List
from sqlalchemy.orm import Session
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import User, UserStatus
from exceptions import ResourceNotFoundException

class UserRepository:
    """
    用户数据访问层
    """
    
    @staticmethod
    def save(db: Session, user: User) -> User:
        """
        保存用户
        
        Args:
            db: 数据库会话
            user: 用户对象
            
        Returns:
            保存后的用户对象
        """
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def find_by_id(db: Session, user_id: int) -> User:
        """
        根据ID查找用户
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            
        Returns:
            用户对象
            
        Raises:
            ResourceNotFoundException: 用户不存在
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ResourceNotFoundException("User", user_id)
        return user
    
    @staticmethod
    def find_by_username(db: Session, username: str) -> Optional[User]:
        """
        根据用户名查找用户
        
        Args:
            db: 数据库会话
            username: 用户名
            
        Returns:
            用户对象，如果不存在则返回None
        """
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def find_all(db: Session) -> List[User]:
        """
        查找所有用户
        
        Args:
            db: 数据库会话
            
        Returns:
            用户列表
        """
        return db.query(User).all()
    
    @staticmethod
    def update_status(db: Session, user_id: int, status: UserStatus) -> User:
        """
        更新用户状态
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            status: 新状态
            
        Returns:
            更新后的用户对象
        """
        user = UserRepository.find_by_id(db, user_id)
        user.status = status
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def delete(db: Session, user_id: int) -> None:
        """
        删除用户
        
        Args:
            db: 数据库会话
            user_id: 用户ID
        """
        user = UserRepository.find_by_id(db, user_id)
        db.delete(user)
        db.commit()
    
    @staticmethod
    def exists_by_username(db: Session, username: str) -> bool:
        """
        检查用户名是否已存在
        
        Args:
            db: 数据库会话
            username: 用户名
            
        Returns:
            是否存在
        """
        return db.query(User).filter(User.username == username).first() is not None