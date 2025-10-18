import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from database import Base, get_db
from config import settings

# 创建测试数据库引擎
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_order_management.db"
test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# 创建测试会话工厂
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# 重写get_db依赖，使用测试数据库
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# 应用依赖覆盖
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def test_db():
    """创建测试数据库表"""
    # 创建所有表
    Base.metadata.create_all(bind=test_engine)
    yield
    # 测试结束后删除所有表
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def client(test_db):
    """测试客户端fixture"""
    with TestClient(app) as c:
        yield c

@pytest.fixture
def auth_token(client):
    """创建测试用户并返回认证token"""
    # 注册测试用户
    client.post("/api/users/register", json={
        "username": "test_user",
        "phone": "13800138004",
        "password": "test_password123"
    })
    
    # 登录获取token
    response = client.post("/api/users/login", json={
        "username": "test_user",
        "password": "test_password123"
    })
    
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest.fixture
def admin_token(client):
    """创建管理员用户并返回认证token"""
    # 这里假设系统有创建管理员的API或者有默认管理员账户
    # 暂时使用普通用户token，实际测试中需要调整
    # 可以通过直接插入数据库创建管理员账户
    from models import User, UserRole, UserStatus
    from sqlalchemy.orm import Session
    from utils.password_util import get_password_hash
    
    db = TestingSessionLocal()
    try:
        # 检查管理员是否已存在
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            # 创建管理员账户
            admin = User(
                username="admin",
                phone="13800138005",
                password=get_password_hash("admin_password123"),
                role=UserRole.ADMIN,
                status=UserStatus.ACTIVE
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
        
        # 登录获取token
        response = client.post("/api/users/login", json={
            "username": "admin",
            "password": "admin_password123"
        })
        
        assert response.status_code == 200
        return response.json()["access_token"]
    finally:
        db.close()

@pytest.fixture
def test_merchant(client, auth_token):
    """创建测试商家"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/api/merchants", json={
        "name": "测试商家",
        "description": "测试商家描述",
        "address": "测试地址",
        "contact": "1234567890"
    }, headers=headers)
    
    assert response.status_code == 201
    return response.json()

@pytest.fixture
def test_product(client, auth_token, test_merchant):
    """创建测试商品"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/api/products", json={
        "name": "测试商品",
        "description": "测试商品描述",
        "price": 99.99,
        "stock": 100,
        "merchant_id": test_merchant["id"]
    }, headers=headers)
    
    assert response.status_code == 201
    return response.json()

@pytest.fixture
def test_order(client, auth_token, test_product):
    """创建测试订单"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/api/orders", json={
        "items": [
            {
                "product_id": test_product["id"],
                "quantity": 2
            }
        ]
    }, headers=headers)
    
    assert response.status_code == 201
    return response.json()