# Spring Boot 与 FastAPI 项目文件映射对照表

本文档详细列出了从 Spring Boot 项目迁移到 FastAPI 项目过程中的文件对应关系，帮助开发者了解代码在两个框架间的映射关系。

## 一、项目结构映射

| Spring Boot 项目结构 | FastAPI 项目结构 | 说明 |
|-------------------|----------------|------|
| `src/main/java/com/...` | `fastApi/` | 主源码目录 |
| `src/main/resources/` | `fastApi/config.py` | 配置文件目录 |
| `src/main/resources/application.yml` | `fastApi/config.py` | 应用配置文件 |
| `target/` | 无直接对应 | Python项目无编译输出目录 |
| `pom.xml` | `fastApi/requirements.txt` | 依赖管理文件 |

## 二、核心模块映射

### 1. 入口类与配置

| Spring Boot 文件 | FastAPI 文件 | 说明 |
|----------------|------------|------|
| `Application.java` | `fastApi/app.py` | 应用入口类 |
| `@SpringBootApplication` | `FastAPI` 实例 | 应用主配置 |
| `application.yml` | `fastApi/config.py` | 应用配置 |

### 2. 数据模型

| Spring Boot 文件 | FastAPI 文件 | 说明 |
|----------------|------------|------|
| `entity/User.java` | `fastApi/models.py` (User类) | 用户实体 |
| `entity/Merchant.java` | `fastApi/models.py` (Merchant类) | 商家实体 |
| `entity/Product.java` | `fastApi/models.py` (Product类) | 产品实体 |
| `entity/Order.java` | `fastApi/models.py` (Order类) | 订单实体 |
| `entity/OrderItem.java` | `fastApi/models.py` (OrderItem类) | 订单项实体 |
| `entity/OrderStatus.java` | `fastApi/models.py` (OrderStatus枚举) | 订单状态枚举 |

### 3. 数据访问层

| Spring Boot 文件 | FastAPI 文件 | 说明 |
|----------------|------------|------|
| `repository/UserRepository.java` | `fastApi/repository/user_repository.py` | 用户数据访问 |
| `repository/MerchantRepository.java` | `fastApi/repository/merchant_repository.py` | 商家数据访问 |
| `repository/ProductRepository.java` | `fastApi/repository/product_repository.py` | 产品数据访问 |
| `repository/OrderRepository.java` | `fastApi/repository/order_repository.py` | 订单数据访问 |
| `repository/OrderItemRepository.java` | `fastApi/repository/order_item_repository.py` | 订单项数据访问 |
| `@Repository` 注解 | 无直接对应 | Python类实现 |
| `JpaRepository` 接口 | 自定义Repository类 | 数据访问接口 |

### 4. 业务逻辑层

| Spring Boot 文件 | FastAPI 文件 | 说明 |
|----------------|------------|------|
| `service/UserService.java` | `fastApi/service/user_service.py` | 用户业务逻辑 |
| `service/MerchantService.java` | `fastApi/service/merchant_service.py` | 商家业务逻辑 |
| `service/ProductService.java` | `fastApi/service/product_service.py` | 产品业务逻辑 |
| `service/OrderService.java` | `fastApi/service/order_service.py` | 订单业务逻辑 |
| `@Service` 注解 | 无直接对应 | Python类实现 |

### 5. API控制器

| Spring Boot 文件 | FastAPI 文件 | 说明 |
|----------------|------------|------|
| `controller/UserController.java` | `fastApi/routers/user.py` | 用户接口 |
| `controller/MerchantController.java` | `fastApi/routers/merchant.py` | 商家接口 |
| `controller/ProductController.java` | `fastApi/routers/product.py` | 产品接口 |
| `controller/OrderController.java` | `fastApi/routers/order.py` | 订单接口 |
| `@RestController` 注解 | `APIRouter` 实例 | 控制器定义 |
| `@RequestMapping` 注解 | `@router.route()` 装饰器 | 路由映射 |

### 6. 数据传输对象

| Spring Boot 文件 | FastAPI 文件 | 说明 |
|----------------|------------|------|
| `dto/*` | 通常直接在 routers 中定义 | 请求/响应对象 |
| `@RequestBody` 注解 | Pydantic 模型参数 | 请求体绑定 |
| `@ResponseBody` 注解 | 函数返回值 | 响应体处理 |

### 7. 异常处理

| Spring Boot 文件 | FastAPI 文件 | 说明 |
|----------------|------------|------|
| `exception/*` | `fastApi/exceptions.py` | 自定义异常 |
| `@ControllerAdvice` | `fastApi/exception_handler.py` | 全局异常处理器 |

### 8. 工具类

| Spring Boot 文件 | FastAPI 文件 | 说明 |
|----------------|------------|------|
| `util/PasswordUtil.java` | `fastApi/utils/password_util.py` | 密码工具 |
| `util/ValidationUtil.java` | `fastApi/utils/validation_util.py` | 验证工具 |

### 9. 安全认证

| Spring Boot 文件 | FastAPI 文件 | 说明 |
|----------------|------------|------|
| `security/JwtTokenProvider.java` | 通常在 `service` 层实现 | JWT 工具 |
| `security/WebSecurityConfig.java` | 在 `app.py` 中配置 | 安全配置 |
| `@PreAuthorize` 注解 | 依赖注入函数 | 权限控制 |

## 三、技术栈映射

| Spring Boot 技术 | FastAPI 技术 | 说明 |
|----------------|------------|------|
| Java | Python | 编程语言 |
| Spring Boot | FastAPI | Web 框架 |
| Spring Data JPA | SQLAlchemy | ORM 框架 |
| Hibernate | SQLAlchemy | ORM 实现 |
| Spring Security | python-jose | 安全框架 |
| Bean Validation | Pydantic | 数据验证 |
| Maven/Gradle | pip | 依赖管理 |
| Tomcat | Uvicorn | Web 服务器 |

## 四、关键注解映射

| Spring Boot 注解 | FastAPI 对应 | 说明 |
|----------------|------------|------|
| `@SpringBootApplication` | `FastAPI()` 实例 | 应用主注解 |
| `@RestController` | `APIRouter()` 实例 | REST控制器 |
| `@RequestMapping` | `@app.get()/@router.get()` | 路由映射 |
| `@GetMapping` | `@app.get()/@router.get()` | GET请求 |
| `@PostMapping` | `@app.post()/@router.post()` | POST请求 |
| `@PutMapping` | `@app.put()/@router.put()` | PUT请求 |
| `@DeleteMapping` | `@app.delete()/@router.delete()` | DELETE请求 |
| `@RequestBody` | 函数参数 | 请求体绑定 |
| `@PathVariable` | `{param}` 和函数参数 | 路径参数 |
| `@RequestParam` | 查询参数 | 查询参数 |
| `@Autowired` | 依赖注入或手动实例化 | 依赖注入 |
| `@Service` | 无直接对应 | 服务层 |
| `@Repository` | 无直接对应 | 数据访问层 |
| `@Entity` | `declarative_base()` 类 | 实体类 |
| `@Table` | `__tablename__` 属性 | 表名 |
| `@Id` | `primary_key=True` | 主键 |
| `@GeneratedValue` | `autoincrement=True` | 自增 |
| `@Column` | `Column` 实例 | 列定义 |

## 五、代码模式差异

| Spring Boot 模式 | FastAPI 模式 | 说明 |
|----------------|------------|------|
| 构造函数注入 | 函数参数注入/手动实例化 | 依赖注入方式 |
| 同步方法 | 支持同步和异步方法 | 执行模式 |
| 返回 ResponseEntity | 返回数据对象 | 响应处理 |
| 异常抛出+ControllerAdvice | 异常抛出+异常处理器 | 异常处理 |
| 配置文件+@Value | Pydantic Settings | 配置读取 |
| Java Bean Validation | Pydantic 模型验证 | 数据验证 |

---

本文档提供了 Spring Boot 与 FastAPI 项目之间的文件和代码映射关系，帮助开发者理解两个框架间的转换逻辑。实际项目中可能存在细节差异，需根据具体实现进行调整。