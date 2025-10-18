#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
初始化测试数据脚本
用于创建测试用户账号
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from database import engine, Base
from models import User, UserRole, UserStatus
from utils.password_util import hash_password

# 创建数据库会话
db = Session(bind=engine)

try:
    # 创建数据库表（如果不存在）
    Base.metadata.create_all(bind=engine)
    
    print("正在初始化测试数据...")
    
    # 检查是否已有测试用户
    existing_admin = db.query(User).filter(User.username == "admin").first()
    existing_test_user = db.query(User).filter(User.username == "test_user").first()
    
    if not existing_admin:
        # 创建管理员用户
        admin_user = User(
            username="admin",
            password=hash_password("admin_password123"),
            phone="13800138000",
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE
        )
        db.add(admin_user)
        print("✓ 创建管理员用户: admin/admin_password123")
    else:
        print("ℹ 管理员用户 'admin' 已存在")
    
    if not existing_test_user:
        # 创建普通测试用户
        test_user = User(
            username="test_user",
            password=hash_password("password123"),
            phone="13900139000",
            role=UserRole.CUSTOMER,
            status=UserStatus.ACTIVE
        )
        db.add(test_user)
        print("✓ 创建测试用户: test_user/password123")
    else:
        print("ℹ 测试用户 'test_user' 已存在")
    
    # 保存到数据库
    db.commit()
    print("\n✅ 测试数据初始化完成！")
    print("\n可用测试账号:")
    print("  1. 管理员账号: admin / admin_password123")
    print("  2. 普通用户: test_user / password123")
    
except Exception as e:
    print(f"❌ 初始化数据时出错: {e}")
    db.rollback()
    sys.exit(1)
finally:
    # 关闭数据库会话
    db.close()
