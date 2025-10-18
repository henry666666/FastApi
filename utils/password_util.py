from passlib.context import CryptContext
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings

# 创建密码加密上下文
pwd_context = CryptContext(schemes=[settings.PASSWORD_SCHEME], deprecated="auto")

def hash_password(password: str) -> str:
    """
    对密码进行加密
    
    Args:
        password: 原始密码
        
    Returns:
        加密后的密码哈希值
    """
    # bcrypt限制密码长度为72字节，需要先截断
    password = password[:72]
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码是否匹配
    
    Args:
        plain_password: 明文密码
        hashed_password: 哈希后的密码
        
    Returns:
        密码是否匹配
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    获取密码哈希值（别名方法）
    
    Args:
        password: 原始密码
        
    Returns:
        加密后的密码哈希值
    """
    return hash_password(password)