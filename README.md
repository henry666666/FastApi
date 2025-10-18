# 订单管理系统 (FastAPI版本)

## 项目简介

本项目是一个订单管理系统，由Spring Boot迁移至FastAPI框架实现。系统提供用户管理、商家管理、产品管理和订单处理等核心功能，采用现代化的Python异步Web框架构建，具备高性能和良好的开发体验。

## 项目架构

项目采用经典的分层架构设计，包括：

1. **数据模型层 (Model)**：使用SQLAlchemy定义数据模型
2. **数据访问层 (Repository)**：负责数据库操作
3. **业务逻辑层 (Service)**：实现核心业务逻辑
4. **API路由层 (Router)**：提供HTTP接口
5. **工具层 (Utils)**：包含各种工具函数
6. **异常处理层**：统一处理各类异常

## 项目结构

```
fastApi/
├── app.py                  # 应用主入口
├── config.py               # 配置文件
├── database.py             # 数据库配置
├── models.py               # 数据模型定义
├── exceptions.py           # 自定义异常类
├── exception_handler.py    # 全局异常处理器
├── repository/             # 数据访问层
│   ├── __init__.py
│   ├── user_repository.py
│   ├── merchant_repository.py
│   ├── product_repository.py
│   ├── order_repository.py
│   └── order_item_repository.py
├── service/                # 业务逻辑层
│   ├── __init__.py
│   ├── user_service.py
│   ├── merchant_service.py
│   ├── product_service.py
│   └── order_service.py
├── routers/                # API路由层
│   ├── __init__.py
│   ├── user.py
│   ├── merchant.py
│   ├── product.py
│   └── order.py
├── utils/                  # 工具层
│   ├── __init__.py
│   ├── password_util.py
│   └── validation_util.py
├── requirements.txt        # 项目依赖
└── order_management.db     # SQLite数据库文件
```

## 核心功能

1. **用户管理**
   - 用户注册、登录
   - 用户信息查询和更新
   - 基于JWT的身份认证

2. **商家管理**
   - 商家信息的增删改查
   - 商家状态管理

3. **产品管理**
   - 产品信息的增删改查
   - 产品库存管理
   - 产品状态管理

4. **订单管理**
   - 创建订单
   - 查询订单信息
   - 更新订单状态
   - 订单明细管理

## 技术栈

- **Web框架**: FastAPI
- **ORM**: SQLAlchemy
- **数据库**: SQLite
- **认证**: JWT (JSON Web Tokens)
- **密码加密**: bcrypt
- **数据验证**: Pydantic
- **服务器**: Uvicorn

## 项目启动步骤

### 1. 环境准备

确保已安装Python 3.8或更高版本，然后克隆项目并进入项目目录：

```bash
cd c:/Users/Administrator/Desktop/testdemo/java-demo/fastApi
```

### 2. 安装依赖

使用pip安装项目所需的所有依赖：

```bash
pip install -r requirements.txt
```

### 3. 数据库初始化

项目使用SQLite数据库，数据库文件会在首次运行时自动创建，无需额外配置。

### 4. 启动应用

使用以下命令启动FastAPI应用：

```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

- `--host 0.0.0.0`: 允许从任何IP地址访问
- `--port 8000`: 使用8000端口
- `--reload`: 启用热重载，修改代码后自动重启服务

### 5. 访问API文档

应用启动后，可以通过以下地址访问自动生成的API文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 6. 停止服务

按 `Ctrl + C` 停止运行中的服务

## API使用说明

### 认证

大部分API需要JWT认证，认证流程如下：

1. 调用登录接口获取token
2. 在后续请求的Authorization头中添加token：`Bearer {your_token}`

### 主要API端点

- **用户相关**
  - POST `/api/users/register` - 用户注册
  - POST `/api/users/login` - 用户登录
  - GET `/api/users/me` - 获取当前用户信息

- **商家相关**
  - GET `/api/merchants` - 获取商家列表
  - POST `/api/merchants` - 创建新商家
  - GET `/api/merchants/{id}` - 获取商家详情
  - PUT `/api/merchants/{id}` - 更新商家信息
  - DELETE `/api/merchants/{id}` - 删除商家

- **产品相关**
  - GET `/api/products` - 获取产品列表
  - POST `/api/products` - 创建新产品
  - GET `/api/products/{id}` - 获取产品详情
  - PUT `/api/products/{id}` - 更新产品信息
  - DELETE `/api/products/{id}` - 删除产品

- **订单相关**
  - GET `/api/orders` - 获取订单列表
  - POST `/api/orders` - 创建新订单
  - GET `/api/orders/{id}` - 获取订单详情
  - PUT `/api/orders/{id}/status` - 更新订单状态

## 开发说明

### 代码风格

- 遵循Python PEP 8规范
- 使用类型注解增强代码可读性
- 添加适当的注释说明复杂逻辑

### 调试技巧

- 使用`--reload`参数启动开发服务器，修改代码后自动重启
- 利用FastAPI的交互式文档进行API测试
- 使用Python内置的pdb模块进行代码调试

## 相关文档

- **迁移过程文档**: [MIGRATION_PROCESS.md](MIGRATION_PROCESS.md)
- **项目映射文档**: [PROJECT_MAPPING.md](PROJECT_MAPPING.md)
- **FastAPI官方文档**: https://fastapi.tiangolo.com/
- **SQLAlchemy官方文档**: https://docs.sqlalchemy.org/

## 许可证

MIT License

## API Specification Comparison

### User API

#### Spring Boot
```java
@PostMapping("/register")
public ResponseEntity<UserResponse> registerUser(
    @RequestBody UserRegistrationRequest request) {
    // ...
}

@GetMapping("/{id}")  
public ResponseEntity<UserResponse> getUserById(@PathVariable Long id) {
    // ...
}
```

#### FastAPI Equivalent
```python
@app.post("/users/register", response_model=schemas.UserResponse)
async def register_user(user: schemas.UserCreate):
    # ...

@app.get("/users/{user_id}", response_model=schemas.UserResponse)  
async def get_user(user_id: int):
    # ...
```

### Order API

#### Spring Boot  
```java
@PostMapping("/place")
public ResponseEntity<Order> placeOrder(
    @RequestBody CreateOrderRequest request) {
    // ...
}

@PostMapping("/{id}/confirm")
public ResponseEntity<Order> confirmOrder(@PathVariable Long id) {
    // ...
}
```

#### FastAPI Equivalent
```python
@app.post("/orders/", response_model=schemas.Order)
async def place_order(order: schemas.OrderCreate):
    # ...

@app.post("/orders/{order_id}/confirm", response_model=schemas.Order)
async def confirm_order(order_id: int):
    # ...
```

## Migration Checklist

- [ ] Set up FastAPI project structure
- [ ] Implement SQLAlchemy models
- [ ] Create Pydantic schemas
- [ ] Port core business logic
- [ ] Implement API endpoints
- [ ] Add authentication
- [ ] Set up database migrations
- [ ] Write unit tests
- [ ] Configure deployment

## Next Steps

1. Review the current Spring Boot implementation details
2. Begin with database model implementation
3. Progressively migrate modules:
   - Users → Merchants → Products → Orders
4. Test each migrated component
5. Final integration testing

See `TASK.MD` for detailed implementation tasks and progress tracking.
