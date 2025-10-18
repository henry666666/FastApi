# Spring Boot 到 FastAPI 迁移过程文档

本文档详细记录了将 Spring Boot 项目迁移到 FastAPI 框架的完整过程。

## 一、项目结构搭建

### 1. 创建基本目录结构
```
fastApi/
├── app.py                # 应用入口
├── config.py             # 配置文件
├── database.py           # 数据库连接配置
├── models.py             # 数据模型
├── exceptions.py         # 自定义异常
├── exception_handler.py  # 全局异常处理器
├── repository/           # 数据访问层
├── service/              # 业务逻辑层
├── routers/              # API路由层
└── utils/                # 工具类
```

### 2. 配置依赖项
创建 `requirements.txt` 文件，包含以下依赖：
```
fastapi
uvicorn[standard]
sqlalchemy
python-jose[cryptography]
python-multipart
passlib[bcrypt]
pydantic
pydantic-settings
```

## 二、核心模块实现

### 1. 数据库连接配置 (database.py)
- 使用 SQLAlchemy 配置 SQLite 数据库连接
- 创建数据库会话工厂和依赖项

### 2. 数据模型定义 (models.py)
- 将 Java 实体类转换为 SQLAlchemy 模型
- 实现了以下模型：
  - User
  - Merchant
  - Product
  - Order
  - OrderItem
  - OrderStatus (枚举)

### 3. 异常处理层 (exceptions.py, exception_handler.py)
- 创建自定义异常类
- 实现全局异常处理器

### 4. 工具层 (utils/)
- password_util.py: 密码加密和验证工具
- validation_util.py: 数据验证工具

## 三、业务逻辑实现

### 1. 数据访问层 (repository/)
- user_repository.py: 用户数据操作
- merchant_repository.py: 商家数据操作
- product_repository.py: 产品数据操作
- order_repository.py: 订单数据操作
- order_item_repository.py: 订单项数据操作

### 2. 业务逻辑层 (service/)
- user_service.py: 用户相关业务逻辑
- merchant_service.py: 商家相关业务逻辑
- product_service.py: 产品相关业务逻辑
- order_service.py: 订单相关业务逻辑

### 3. API路由层 (routers/)
- user.py: 用户相关接口
- merchant.py: 商家相关接口
- product.py: 产品相关接口
- order.py: 订单相关接口

## 四、安全机制实现

### 1. JWT认证
- 实现了基于 JWT 的用户认证
- 创建了获取当前用户的依赖项

### 2. 密码安全
- 使用 bcrypt 进行密码加密
- 实现密码验证功能

## 五、解决导入问题

在项目开发过程中，遇到了相对导入的问题，通过以下方式解决：

1. 在每个需要导入的文件顶部添加路径配置代码：
```python
import sys
import os

# 获取当前文件的绝对路径
current_path = os.path.dirname(os.path.abspath(__file__))
# 添加项目根目录到 sys.path
sys.path.append(os.path.dirname(current_path))
```

2. 将相对导入改为绝对导入，例如：
   - 从 `from ..models import Merchant` 改为 `from models import Merchant`
   - 从 `from ..database import get_db` 改为 `from database import get_db`

## 六、项目启动

使用以下命令启动 FastAPI 应用：
```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

## 七、API文档访问

应用启动后，可以通过以下地址访问 Swagger UI 文档：
```
http://localhost:8000/swagger-ui.html
```

## 八、迁移过程中的主要挑战

1. **导入路径问题**：FastAPI 项目中相对导入的处理方式与 Spring Boot 不同，需要配置合适的路径
2. **ORM 差异**：从 Hibernate/JPA 迁移到 SQLAlchemy 的语法差异
3. **异步编程模型**：FastAPI 支持异步编程，需要调整代码结构
4. **验证机制**：从 Java Bean Validation 迁移到 Pydantic 验证

## 九、后续优化方向

1. 实现更完善的错误处理机制
2. 添加单元测试和集成测试
3. 优化数据库查询性能
4. 实现缓存机制
5. 添加日志记录功能

---

本文档由迁移工具自动生成，记录了从 Spring Boot 到 FastAPI 的完整迁移过程。