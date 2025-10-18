import pytest

def test_create_order_success(client, auth_token, test_product):
    """测试成功创建订单"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # 创建订单
    response = client.post("/api/orders", json={
        "items": [
            {
                "product_id": test_product["id"],
                "quantity": 3
            }
        ]
    }, headers=headers)
    
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert "status" in data
    assert "items" in data
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == test_product["id"]
    assert data["items"][0]["quantity"] == 3
    assert "total_price" in data

def test_create_order_invalid_product(client, auth_token):
    """测试创建订单时使用无效的商品ID"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    response = client.post("/api/orders", json={
        "items": [
            {
                "product_id": 999999,  # 不存在的商品ID
                "quantity": 1
            }
        ]
    }, headers=headers)
    
    assert response.status_code == 404  # 商品不存在
    data = response.json()
    assert "detail" in data

def test_create_order_insufficient_stock(client, auth_token, test_product):
    """测试创建订单时库存不足"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # 尝试订购超过库存的数量
    response = client.post("/api/orders", json={
        "items": [
            {
                "product_id": test_product["id"],
                "quantity": 9999  # 远超过test_product中的stock值(100)
            }
        ]
    }, headers=headers)
    
    assert response.status_code == 400  # 库存不足错误
    data = response.json()
    assert "detail" in data

def test_create_order_invalid_quantity(client, auth_token, test_product):
    """测试创建订单时使用无效的数量"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    response = client.post("/api/orders", json={
        "items": [
            {
                "product_id": test_product["id"],
                "quantity": 0  # 数量不能为0
            }
        ]
    }, headers=headers)
    
    assert response.status_code == 422  # Pydantic验证错误

def test_get_order_by_id(client, auth_token, test_order):
    """测试通过ID获取订单详情"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get(f"/api/orders/{test_order['id']}", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_order["id"]
    assert "status" in data
    assert "items" in data
    assert "total_price" in data

def test_get_nonexistent_order(client, auth_token):
    """测试获取不存在的订单"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/api/orders/999999", headers=headers)
    
    assert response.status_code == 404  # 订单不存在
    data = response.json()
    assert "detail" in data

def test_get_user_orders(client, auth_token, test_order):
    """测试获取用户的所有订单"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # 创建另一个订单，确保至少有两个订单
    response = client.post("/api/orders", json={
        "items": [
            {
                "product_id": test_order["items"][0]["product_id"],
                "quantity": 1
            }
        ]
    }, headers=headers)
    
    # 获取用户的所有订单
    response = client.get("/api/orders", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    
    # 验证test_order在返回列表中
    found = any(order["id"] == test_order["id"] for order in data)
    assert found, "测试订单应该在返回的列表中"

def test_update_order_status_admin(client, admin_token, test_order):
    """测试管理员更新订单状态"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # 更新订单状态为已发货
    response = client.patch(f"/api/orders/{test_order['id']}/status", json={
        "status": "SHIPPED"
    }, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_order["id"]
    assert data["status"] == "SHIPPED"

def test_update_order_status_regular_user(client, auth_token, test_order):
    """测试普通用户尝试更新订单状态（应被拒绝）"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # 尝试更新订单状态
    response = client.patch(f"/api/orders/{test_order['id']}/status", json={
        "status": "SHIPPED"
    }, headers=headers)
    
    assert response.status_code == 403  # 权限不足

def test_update_nonexistent_order_status(client, admin_token):
    """测试更新不存在订单的状态"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    response = client.patch("/api/orders/999999/status", json={
        "status": "SHIPPED"
    }, headers=headers)
    
    assert response.status_code == 404  # 订单不存在

def test_update_order_with_invalid_status(client, admin_token, test_order):
    """测试使用无效状态更新订单"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    response = client.patch(f"/api/orders/{test_order['id']}/status", json={
        "status": "INVALID_STATUS"
    }, headers=headers)
    
    assert response.status_code == 422  # Pydantic验证错误

def test_cancel_order_by_user(client, auth_token):
    """测试用户取消自己的订单"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # 先创建一个新订单
    response = client.post("/api/orders", json={
        "items": [
            {
                "product_id": 1,  # 假设ID为1的商品存在
                "quantity": 1
            }
        ]
    }, headers=headers)
    
    order_data = response.json()
    
    # 取消订单
    cancel_response = client.post(f"/api/orders/{order_data['id']}/cancel", headers=headers)
    
    assert cancel_response.status_code == 200
    data = cancel_response.json()
    assert data["id"] == order_data["id"]
    assert data["status"] == "CANCELLED"

def test_cancel_shipped_order(client, auth_token, test_order, admin_token):
    """测试取消已发货的订单（应被拒绝）"""
    # 先将订单状态更新为已发货
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    client.patch(f"/api/orders/{test_order['id']}/status", json={
        "status": "SHIPPED"
    }, headers=admin_headers)
    
    # 尝试取消已发货的订单
    user_headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post(f"/api/orders/{test_order['id']}/cancel", headers=user_headers)
    
    assert response.status_code == 400  # 不能取消已发货的订单

def test_filter_orders_by_status(client, auth_token, test_order, admin_token):
    """测试按状态筛选订单"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # 创建一个已取消的订单
    cancel_order_response = client.post("/api/orders", json={
        "items": [
            {
                "product_id": 1,  # 假设ID为1的商品存在
                "quantity": 1
            }
        ]
    }, headers=headers)
    
    cancel_order = cancel_order_response.json()
    client.post(f"/api/orders/{cancel_order['id']}/cancel", headers=headers)
    
    # 按状态筛选
    response = client.get("/api/orders?status=PENDING", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    
    # 确保返回的所有订单状态都是PENDING
    for order in data:
        assert order["status"] == "PENDING"