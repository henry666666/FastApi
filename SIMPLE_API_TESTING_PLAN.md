# 订单管理系统（FastAPI）简易API测试计划

## 1. 测试概述

本文档提供了一个简单实用的API测试计划，适用于开发过程中的快速验证和功能测试。我们将重点利用FastAPI自带的Swagger UI进行手动测试，同时提供简单的自动化测试方案。

## 2. 使用FastAPI自带Swagger UI进行测试

### 2.1 Swagger UI访问方式

FastAPI自动生成交互式API文档，使用方法如下：

1. 启动FastAPI应用服务器：
   ```bash
   python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

2. 在浏览器中访问以下URL：
   - Swagger UI: http://localhost:8000/docs
   - ReDoc文档: http://localhost:8000/redoc

3. Swagger UI界面将显示所有API端点、参数和请求/响应格式

### 2.2 Swagger UI测试步骤

1. **用户注册测试**：
   - 展开`/api/users/register`端点
   - 点击"Try it out"按钮
   - 填写请求体（username、email、password）
   - 点击"Execute"按钮执行请求
   - 观察响应状态码和响应内容

2. **用户登录测试**：
   - 展开`/api/users/login`端点
   - 点击"Try it out"按钮
   - 填写请求体（username、password）
   - 点击"Execute"按钮执行请求
   - 保存返回的`access_token`用于后续测试

3. **带认证的API测试**：
   - 展开需要认证的端点（如`/api/users/me`）
   - 点击"Try it out"按钮
   - 在"Authorization"字段中输入`Bearer {access_token}`
   - 点击"Execute"按钮执行请求
   - 观察响应结果

4. **其他端点测试**：
   - 按照上述步骤测试所有CRUD操作端点
   - 验证各种状态码和错误处理情况

### 2.3 Swagger UI测试优点

- **零配置**：FastAPI自动生成，无需额外设置
- **交互式界面**：直观易用，可直接在浏览器中测试
- **实时文档**：API变更时自动更新文档
- **参数验证**：自动检查请求参数格式
- **响应示例**：提供响应格式示例

## 3. 简易自动化测试方案

### 3.1 使用Python requests库进行简单测试

创建一个测试脚本，使用Python的requests库测试API：

```python
# simple_api_test.py
import requests
import json

BASE_URL = "http://localhost:8000"

def test_user_registration():
    print("测试用户注册...")
    url = f"{BASE_URL}/api/users/register"
    payload = {
        "username": "test_api_user",
        "email": "test_api@example.com",
        "password": "test_password123"
    }
    response = requests.post(url, json=payload)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    return response.status_code == 201

def test_user_login():
    print("测试用户登录...")
    url = f"{BASE_URL}/api/users/login"
    payload = {
        "username": "test_api_user",
        "password": "test_password123"
    }
    response = requests.post(url, json=payload)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        print(f"获取到token: {token}")
        return token
    return None

def test_protected_endpoint(token):
    print("测试受保护的端点...")
    url = f"{BASE_URL}/api/users/me"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    return response.status_code == 200

# 运行测试流程
if __name__ == "__main__":
    print("===== 开始API测试 =====")
    
    if test_user_registration():
        token = test_user_login()
        if token:
            test_protected_endpoint(token)
    
    print("===== API测试结束 =====")
```

### 3.2 使用FastAPI TestClient进行测试

FastAPI提供了TestClient工具，可以在不启动服务器的情况下测试API：

```python
# test_client.py
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_register():
    response = client.post(
        "/api/users/register",
        json={"username": "test_client", "email": "test_client@example.com", "password": "test_password"}
    )
    assert response.status_code == 201
    return response.json()

def test_login():
    response = client.post(
        "/api/users/login",
        json={"username": "test_client", "password": "test_password"}
    )
    assert response.status_code == 200
    return response.json()

def test_get_user_info(token):
    response = client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    return response.json()

# 运行测试
if __name__ == "__main__":
    print("测试用户注册...")
    user = test_register()
    print(f"注册成功: {user}")
    
    print("测试用户登录...")
    login_response = test_login()
    token = login_response["access_token"]
    print(f"登录成功，获取到token")
    
    print("测试获取用户信息...")
    user_info = test_get_user_info(token)
    print(f"获取用户信息成功: {user_info}")
```

## 4. API测试用例设计

### 4.1 用户管理API测试用例

| 测试用例ID | 端点 | 方法 | 描述 | 预期结果 |
|------------|------|------|------|----------|
| UC001 | /api/users/register | POST | 正常用户注册 | 状态码201，返回用户信息 |
| UC002 | /api/users/register | POST | 注册已存在用户 | 状态码400，返回错误信息 |
| UC003 | /api/users/register | POST | 注册信息不完整 | 状态码422，返回验证错误 |
| UC004 | /api/users/login | POST | 正确凭证登录 | 状态码200，返回access_token |
| UC005 | /api/users/login | POST | 错误密码登录 | 状态码401，返回认证错误 |
| UC006 | /api/users/me | GET | 获取当前用户信息 | 状态码200，返回用户信息 |
| UC007 | /api/users/me | GET | 无效token访问 | 状态码401，返回认证错误 |

### 4.2 商品管理API测试用例

| 测试用例ID | 端点 | 方法 | 描述 | 预期结果 |
|------------|------|------|------|----------|
| PC001 | /api/products | GET | 获取商品列表 | 状态码200，返回商品列表 |
| PC002 | /api/products/{id} | GET | 获取单个商品 | 状态码200，返回商品详情 |
| PC003 | /api/products/{id} | GET | 获取不存在商品 | 状态码404，返回错误信息 |
| PC004 | /api/products | POST | 创建新商品 | 状态码201，返回创建的商品 |
| PC005 | /api/products/{id} | PUT | 更新商品信息 | 状态码200，返回更新后的商品 |
| PC006 | /api/products/{id} | DELETE | 删除商品 | 状态码204，无内容返回 |

### 4.3 订单管理API测试用例

| 测试用例ID | 端点 | 方法 | 描述 | 预期结果 |
|------------|------|------|------|----------|
| OC001 | /api/orders | GET | 获取订单列表 | 状态码200，返回订单列表 |
| OC002 | /api/orders | POST | 创建新订单 | 状态码201，返回创建的订单 |
| OC003 | /api/orders/{id} | GET | 获取单个订单 | 状态码200，返回订单详情 |
| OC004 | /api/orders/{id}/status | PUT | 更新订单状态 | 状态码200，返回更新后的订单 |
| OC005 | /api/orders | POST | 创建订单（库存不足） | 状态码400，返回错误信息 |

## 5. 测试流程与最佳实践

### 5.1 基本测试流程

1. **准备测试数据**：确保数据库处于干净状态
2. **启动应用服务器**：运行`uvicorn app:app --reload`
3. **访问Swagger UI**：打开http://localhost:8000/docs
4. **执行测试用例**：按照测试用例表逐个测试API
5. **记录测试结果**：记录成功/失败情况和错误信息
6. **问题分析与修复**：针对测试失败的API进行调试和修复
7. **回归测试**：修复后重新测试相关API

### 5.2 测试最佳实践

1. **测试环境隔离**：使用专用的测试数据库
2. **测试数据管理**：测试前清理数据，测试后恢复环境
3. **边界值测试**：测试各种边界条件和异常情况
4. **错误处理验证**：确保所有错误情况都能返回适当的错误响应
5. **权限验证**：测试不同用户角色的访问权限
6. **日志记录**：在测试过程中启用详细日志，便于问题排查

## 6. 常见问题与排查

### 6.1 API响应状态码说明

- **200 OK**：请求成功
- **201 Created**：资源创建成功
- **204 No Content**：请求成功，无内容返回
- **400 Bad Request**：请求参数错误
- **401 Unauthorized**：认证失败
- **403 Forbidden**：权限不足
- **404 Not Found**：资源不存在
- **422 Unprocessable Entity**：请求验证错误
- **500 Internal Server Error**：服务器内部错误

### 6.2 常见问题排查步骤

1. **检查请求参数**：确保参数格式正确、必填项已填写
2. **验证认证信息**：检查token是否有效、是否已过期
3. **查看服务器日志**：分析服务器日志中的错误信息
4. **检查数据库状态**：确认数据库连接正常，表结构正确
5. **使用Postman等工具**：交叉验证API行为

## 7. 自动化测试集成

对于更全面的测试，可以考虑集成以下工具：

1. **pytest**：Python的测试框架，可用于编写更结构化的测试用例
2. **Postman/Newman**：API测试工具，可导出测试集合并集成到CI/CD流程
3. **GitHub Actions/Jenkins**：将API测试集成到持续集成流程中

### 7.1 使用pytest的简单示例

```python
# test_api.py
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

@pytest.fixture
def auth_token():
    # 注册测试用户
    client.post("/api/users/register", json={
        "username": "test_pytest",
        "email": "test_pytest@example.com",
        "password": "test_password"
    })
    # 登录获取token
    response = client.post("/api/users/login", json={
        "username": "test_pytest",
        "password": "test_password"
    })
    return response.json()["access_token"]

def test_get_products():
    response = client.get("/api/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_product(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/api/products", json={
        "name": "测试商品",
        "description": "测试描述",
        "price": 99.99,
        "stock": 100,
        "merchant_id": 1
    }, headers=headers)
    assert response.status_code == 201
```

## 8. 总结

本测试计划提供了使用FastAPI自带Swagger UI进行快速API测试的方法，以及简单的自动化测试方案。通过这些方法，可以在开发过程中快速验证API功能，确保系统正常运行。对于更复杂的测试需求，可以参考之前创建的《稳定性测试计划》文档，结合更全面的测试策略。

FastAPI的Swagger UI是一个非常强大的工具，特别适合开发阶段的API测试和文档查阅。通过它，开发人员可以轻松地进行手动测试，而无需编写额外的测试代码或使用第三方工具。