import pytest

def test_user_registration_success(client):
    """测试用户注册成功"""
    response = client.post("/api/users/register", json={
        "username": "new_user",
        "phone": "13800138000",
        "password": "pass123"  # 使用更短的密码，避免bcrypt 72字节限制
    })
    
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["username"] == "new_user"
    assert data["phone"] == "13800138000"
    assert "password" not in data  # 确保密码不会返回给客户端
    assert "role" in data
    assert "status" in data

def test_user_registration_missing_required_fields(client):
    """测试用户注册时缺少必填字段"""
    response = client.post("/api/users/register", json={
        "username": "incomplete_user"
        # 缺少phone和password
    })
    
    assert response.status_code == 422  # Pydantic验证错误

def test_user_registration_invalid_phone(client):
    """测试用户注册时使用无效的手机号格式"""
    response = client.post("/api/users/register", json={
        "username": "invalid_phone_user",
        "phone": "invalid-phone",
        "password": "password123"
    })
    
    assert response.status_code == 422  # Pydantic验证错误

def test_user_registration_duplicate_username(client, auth_token):
    """测试用户注册时使用已存在的用户名"""
    # 使用fixture中已经创建的用户
    response = client.post("/api/users/register", json={
        "username": "test_user",
        "phone": "13800138001",
        "password": "password123"
    })
    
    assert response.status_code == 400  # 用户名已存在错误
    data = response.json()
    assert "detail" in data

def test_user_login_success(client):
    """测试用户登录成功"""
    # 先注册用户
    client.post("/api/users/register", json={
        "username": "login_test_user",
        "phone": "13800138002",
        "password": "login_password123"
    })
    
    # 登录
    response = client.post("/api/users/login", json={
        "username": "login_test_user",
        "password": "login_password123"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"

def test_user_login_invalid_credentials(client):
    """测试用户使用无效凭证登录"""
    response = client.post("/api/users/login", json={
        "username": "non_existent_user",
        "password": "wrong_password"
    })
    
    assert response.status_code == 401  # 认证失败
    data = response.json()
    assert "detail" in data

def test_user_login_wrong_password(client):
    """测试用户使用错误密码登录"""
    # 先注册用户
    client.post("/api/users/register", json={
        "username": "wrong_pass_user",
        "phone": "13800138003",
        "password": "correct_password123"
    })
    
    # 使用错误密码登录
    response = client.post("/api/users/login", json={
        "username": "wrong_pass_user",
        "password": "wrong_password123"
    })
    
    assert response.status_code == 401  # 认证失败
    data = response.json()
    assert "detail" in data

def test_get_current_user_info(client, auth_token):
    """测试获取当前用户信息"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/api/users/me", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "test_user"
    assert "id" in data
    assert "phone" in data
    assert "role" in data
    assert "status" in data
    assert "password" not in data  # 确保密码不会返回给客户端

def test_get_current_user_unauthorized(client):
    """测试未授权访问获取用户信息"""
    # 不提供token
    response = client.get("/api/users/me")
    
    assert response.status_code == 401  # 未授权
    data = response.json()
    assert "detail" in data

def test_get_current_user_invalid_token(client):
    """测试使用无效token访问获取用户信息"""
    headers = {"Authorization": "Bearer invalid_token_here"}
    response = client.get("/api/users/me", headers=headers)
    
    assert response.status_code == 401  # 未授权
    data = response.json()
    assert "detail" in data

def test_get_current_user_expired_token(client):
    """测试使用过期token访问获取用户信息"""
    # 生成一个过期的token（如果需要，可以调整为实际的过期token）
    # 这里我们使用一个格式正确但无效的token来模拟
    invalid_jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3RfdXNlciIsImV4cCI6MTUxNjIzOTAyMn0.invalid_signature_here"
    headers = {"Authorization": f"Bearer {invalid_jwt_token}"}
    response = client.get("/api/users/me", headers=headers)
    
    assert response.status_code == 401  # 未授权
    data = response.json()
    assert "detail" in data