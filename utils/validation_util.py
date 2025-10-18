import re
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Optional
from exceptions import ValidationException

def validate_username(username: str) -> bool:
    """
    验证用户名格式
    
    Args:
        username: 用户名
        
    Returns:
        验证是否通过
        
    Raises:
        ValidationException: 用户名格式不正确
    """
    # 用户名：3-20位字母数字下划线
    if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
        raise ValidationException(
            "Username must be 3-20 characters long and contain only letters, numbers, and underscores"
        )
    return True

def validate_password(password: str) -> bool:
    """
    验证密码强度
    
    Args:
        password: 密码
        
    Returns:
        验证是否通过
        
    Raises:
        ValidationException: 密码强度不足
    """
    if len(password) < 6:
        raise ValidationException("Password must be at least 6 characters long")
    return True

def validate_phone(phone: str) -> bool:
    """
    验证手机号格式（中国手机号）
    
    Args:
        phone: 手机号
        
    Returns:
        验证是否通过
        
    Raises:
        ValidationException: 手机号格式不正确
    """
    if not re.match(r'^1[3-9]\d{9}$', phone):
        raise ValidationException("Invalid phone number format")
    return True

def validate_positive_number(value: float, field_name: str = "value") -> bool:
    """
    验证是否为正数
    
    Args:
        value: 要验证的数值
        field_name: 字段名称
        
    Returns:
        验证是否通过
        
    Raises:
        ValidationException: 不是正数
    """
    if value <= 0:
        raise ValidationException(f"{field_name} must be positive")
    return True

def validate_required(value: Optional[str], field_name: str) -> bool:
    """
    验证必填字段
    
    Args:
        value: 要验证的值
        field_name: 字段名称
        
    Returns:
        验证是否通过
        
    Raises:
        ValidationException: 字段为空
    """
    if value is None or value.strip() == "":
        raise ValidationException(f"{field_name} is required")
    return True