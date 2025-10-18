import pytest

def test_create_merchant_success(client, auth_token):
    """测试成功创建商家"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/api/merchants", json={
        "name": "测试商家名称",
        "description": "这是一个测试商家的详细描述",
        "address": "测试地址123号",
        "contact": "13800138000"
    }, headers=headers)
    
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["name"] == "测试商家名称"
    assert data["description"] == "这是一个测试商家的详细描述"
    assert data["address"] == "测试地址123号"
    assert data["contact"] == "13800138000"

def test_create_merchant_missing_required_fields(client, auth_token):
    """测试创建商家时缺少必填字段"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/api/merchants", json={
        # 缺少必填字段如name
        "description": "只有描述"
    }, headers=headers)
    
    assert response.status_code == 422  # Pydantic验证错误

def test_create_merchant_empty_name(client, auth_token):
    """测试创建商家时使用空名称"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/api/merchants", json={
        "name": "",  # 空名称
        "description": "测试描述",
        "address": "测试地址",
        "contact": "1234567890"
    }, headers=headers)
    
    assert response.status_code == 422  # Pydantic验证错误

def test_get_merchant_by_id(client, auth_token, test_merchant):
    """测试通过ID获取商家详情"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get(f"/api/merchants/{test_merchant['id']}", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_merchant["id"]
    assert data["name"] == test_merchant["name"]
    assert data["description"] == test_merchant["description"]
    assert data["address"] == test_merchant["address"]
    assert data["contact"] == test_merchant["contact"]

def test_get_nonexistent_merchant(client, auth_token):
    """测试获取不存在的商家"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/api/merchants/999999", headers=headers)
    
    assert response.status_code == 404  # 商家不存在
    data = response.json()
    assert "detail" in data

def test_get_merchant_list(client, auth_token, test_merchant):
    """测试获取商家列表"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # 创建另一个商家，确保至少有两个商家
    client.post("/api/merchants", json={
        "name": "第二个测试商家",
        "description": "第二个商家描述",
        "address": "测试地址2",
        "contact": "13900139000"
    }, headers=headers)
    
    response = client.get("/api/merchants", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    
    # 验证test_merchant在返回列表中
    found = any(merchant["id"] == test_merchant["id"] for merchant in data)
    assert found, "测试商家应该在返回的列表中"

def test_update_merchant_success(client, auth_token, test_merchant):
    """测试成功更新商家信息"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.put(f"/api/merchants/{test_merchant['id']}", json={
        "name": "更新后的商家名称",
        "description": "更新后的商家描述",
        "address": "更新后的地址",
        "contact": "13700137000"
    }, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_merchant["id"]
    assert data["name"] == "更新后的商家名称"
    assert data["description"] == "更新后的商家描述"
    assert data["address"] == "更新后的地址"
    assert data["contact"] == "13700137000"

def test_update_merchant_partial(client, auth_token, test_merchant):
    """测试部分更新商家信息"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.patch(f"/api/merchants/{test_merchant['id']}", json={
        "contact": "13600136000"  # 只更新联系方式
    }, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_merchant["id"]
    assert data["contact"] == "13600136000"
    assert data["name"] == test_merchant["name"]  # 其他字段保持不变

def test_update_nonexistent_merchant(client, auth_token):
    """测试更新不存在的商家"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.put("/api/merchants/999999", json={
        "name": "不存在的商家",
        "description": "描述",
        "address": "地址",
        "contact": "1234567890"
    }, headers=headers)
    
    assert response.status_code == 404  # 商家不存在

def test_delete_merchant_success(client, auth_token, test_merchant):
    """测试成功删除商家"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.delete(f"/api/merchants/{test_merchant['id']}", headers=headers)
    
    assert response.status_code == 204  # 成功删除，无内容返回
    
    # 验证商家确实被删除了
    get_response = client.get(f"/api/merchants/{test_merchant['id']}", headers=headers)
    assert get_response.status_code == 404

def test_delete_nonexistent_merchant(client, auth_token):
    """测试删除不存在的商家"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.delete("/api/merchants/999999", headers=headers)
    
    assert response.status_code == 404  # 商家不存在

def test_delete_merchant_with_products(client, auth_token, test_merchant, test_product):
    """测试删除包含商品的商家（应被拒绝）"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.delete(f"/api/merchants/{test_merchant['id']}", headers=headers)
    
    # 这里取决于业务逻辑，如果不允许删除包含商品的商家，则应返回错误
    # 否则，如果允许删除但会级联删除相关商品，则返回204
    # 根据通常的最佳实践，这里假设不允许删除包含商品的商家
    assert response.status_code == 400  # 删除失败
    data = response.json()
    assert "detail" in data

def test_search_merchants_by_name(client, auth_token, test_merchant):
    """测试通过名称搜索商家"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # 创建另一个商家，确保名称可区分
    client.post("/api/merchants", json={
        "name": "苹果商家",
        "description": "销售苹果产品",
        "address": "苹果街",
        "contact": "13811111111"
    }, headers=headers)
    
    # 通过部分名称搜索
    response = client.get("/api/merchants?search=苹果", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    
    # 确保返回的所有商家名称都包含搜索词
    for merchant in data:
        assert "苹果" in merchant["name"]