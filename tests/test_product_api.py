import pytest

def test_create_product_success(client, auth_token):
    """测试成功创建商品"""
    # 先创建一个商家
    headers = {"Authorization": f"Bearer {auth_token}"}
    merchant_response = client.post("/api/merchants", json={
        "name": "创建商品测试商家",
        "description": "测试商家描述",
        "address": "测试地址",
        "contact": "1234567890"
    }, headers=headers)
    
    merchant_data = merchant_response.json()
    
    # 创建商品
    response = client.post("/api/products", json={
        "name": "新测试商品",
        "description": "商品详细描述",
        "price": 129.99,
        "stock": 50,
        "merchant_id": merchant_data["id"]
    }, headers=headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "新测试商品"
    assert data["description"] == "商品详细描述"
    assert data["price"] == 129.99
    assert data["stock"] == 50
    assert data["merchant_id"] == merchant_data["id"]

def test_create_product_missing_required_fields(client, auth_token):
    """测试创建商品时缺少必填字段"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/api/products", json={
        # 缺少必填字段如name、price、stock等
        "description": "只有描述"
    }, headers=headers)
    
    assert response.status_code == 422  # Pydantic验证错误

def test_create_product_invalid_price(client, auth_token):
    """测试创建商品时使用无效的价格"""
    # 先创建一个商家
    headers = {"Authorization": f"Bearer {auth_token}"}
    merchant_response = client.post("/api/merchants", json={
        "name": "无效价格测试商家",
        "description": "测试商家描述",
        "address": "测试地址",
        "contact": "1234567890"
    }, headers=headers)
    
    merchant_data = merchant_response.json()
    
    # 使用负数价格
    response = client.post("/api/products", json={
        "name": "无效价格商品",
        "description": "价格为负数",
        "price": -10.99,
        "stock": 10,
        "merchant_id": merchant_data["id"]
    }, headers=headers)
    
    assert response.status_code == 422  # Pydantic验证错误

def test_create_product_invalid_stock(client, auth_token):
    """测试创建商品时使用无效的库存"""
    # 先创建一个商家
    headers = {"Authorization": f"Bearer {auth_token}"}
    merchant_response = client.post("/api/merchants", json={
        "name": "无效库存测试商家",
        "description": "测试商家描述",
        "address": "测试地址",
        "contact": "1234567890"
    }, headers=headers)
    
    merchant_data = merchant_response.json()
    
    # 使用负数库存
    response = client.post("/api/products", json={
        "name": "无效库存商品",
        "description": "库存为负数",
        "price": 10.99,
        "stock": -5,
        "merchant_id": merchant_data["id"]
    }, headers=headers)
    
    assert response.status_code == 422  # Pydantic验证错误

def test_get_product_by_id(client, auth_token, test_product):
    """测试通过ID获取商品详情"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get(f"/api/products/{test_product['id']}", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_product["id"]
    assert data["name"] == test_product["name"]
    assert data["price"] == test_product["price"]

def test_get_nonexistent_product(client, auth_token):
    """测试获取不存在的商品"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/api/products/999999", headers=headers)
    
    assert response.status_code == 404  # 商品不存在
    data = response.json()
    assert "detail" in data

def test_get_product_list(client, auth_token, test_product):
    """测试获取商品列表"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/api/products", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    
    # 检查是否包含我们的测试商品
    found = any(item["id"] == test_product["id"] for item in data)
    assert found, "测试商品应该在返回的列表中"

def test_update_product_success(client, auth_token, test_product):
    """测试成功更新商品信息"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.put(f"/api/products/{test_product['id']}", json={
        "name": "更新后的商品名称",
        "price": 159.99,
        "stock": 200,
        "description": "更新后的商品描述"
    }, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_product["id"]
    assert data["name"] == "更新后的商品名称"
    assert data["price"] == 159.99
    assert data["stock"] == 200
    assert data["description"] == "更新后的商品描述"

def test_update_product_partial(client, auth_token, test_product):
    """测试部分更新商品信息"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.patch(f"/api/products/{test_product['id']}", json={
        "price": 179.99  # 只更新价格
    }, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_product["id"]
    assert data["price"] == 179.99
    assert data["name"] == test_product["name"]  # 其他字段保持不变

def test_delete_product_success(client, auth_token, test_product):
    """测试成功删除商品"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.delete(f"/api/products/{test_product['id']}", headers=headers)
    
    assert response.status_code == 204  # 成功删除，无内容返回
    
    # 验证商品确实被删除了
    get_response = client.get(f"/api/products/{test_product['id']}", headers=headers)
    assert get_response.status_code == 404

def test_delete_nonexistent_product(client, auth_token):
    """测试删除不存在的商品"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.delete("/api/products/999999", headers=headers)
    
    assert response.status_code == 404  # 商品不存在

def test_product_filtering_by_merchant(client, auth_token, test_product):
    """测试按商家ID筛选商品"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # 创建另一个商家和商品
    merchant2_response = client.post("/api/merchants", json={
        "name": "第二个测试商家",
        "description": "测试商家描述2",
        "address": "测试地址2",
        "contact": "0987654321"
    }, headers=headers)
    
    merchant2_data = merchant2_response.json()
    
    client.post("/api/products", json={
        "name": "第二个商家的商品",
        "description": "商品描述",
        "price": 89.99,
        "stock": 100,
        "merchant_id": merchant2_data["id"]
    }, headers=headers)
    
    # 按第一个商家ID筛选
    response = client.get(f"/api/products?merchant_id={test_product['merchant_id']}", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    
    # 确保返回的所有商品都属于指定商家
    for item in data:
        assert item["merchant_id"] == test_product["merchant_id"]