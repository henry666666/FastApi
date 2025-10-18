from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import settings
from database import engine, Base
from exception_handler import global_exception_handler
from routers import merchant, order, product, user

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建FastAPI应用
app = FastAPI(
    title="订单管理系统 API",
    description="基于FastAPI的订单管理系统，包含用户、商家、商品和订单管理功能",
    version="1.0.0",
    docs_url="/swagger-ui.html",  # 保持与Spring Boot一致的文档URL
    redoc_url="/redoc",
    openapi_url="/v3/api-docs"
)

# 配置全局异常处理器
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RequestValidationError, global_exception_handler)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user.router)
app.include_router(merchant.router)
app.include_router(product.router)
app.include_router(order.router)

@app.get("/")
async def root():
    """
    根路径
    """
    return {"message": "订单管理系统 API 正在运行"}

@app.get("/health")
async def health_check():
    """
    健康检查接口
    """
    return {"status": "healthy"}
