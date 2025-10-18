from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Enum as SQLEnum, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from pydantic import BaseModel, ConfigDict, Field
from enum import Enum
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import Base

# 枚举定义
class UserRole(str, Enum):
    CUSTOMER = "CUSTOMER"
    MERCHANT = "MERCHANT"
    ADMIN = "ADMIN"

class UserStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"
    DELETED = "DELETED"

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    CREATED = "CREATED"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"
    SHIPPED = "SHIPPED"

# 数据库模型
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.CUSTOMER)
    phone = Column(String(20))
    status = Column(SQLEnum(UserStatus), nullable=False, default=UserStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    orders = relationship("Order", back_populates="user")

class Merchant(Base):
    __tablename__ = "merchants"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    contact = Column(String(20))
    rating = Column(Float, default=5.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    products = relationship("Product", back_populates="merchant")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    category = Column(String(100))
    stock = Column(Integer, default=0)
    price = Column(Float, nullable=False)
    merchant_id = Column(Integer, ForeignKey("merchants.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    merchant = relationship("Merchant", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    customer_name = Column(String(200), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(SQLEnum(OrderStatus), nullable=False, default=OrderStatus.CREATED)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    
    # 关系
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")

# Pydantic 模式 (DTOs)
# 用户相关
class UserRegistrationRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, pattern="^[a-zA-Z0-9_]+$")
    password: str = Field(..., min_length=6)
    phone: str = Field(..., pattern="^1[3-9]\d{9}$")

class UserResponse(BaseModel):
    id: int
    username: str
    role: UserRole
    phone: str
    status: UserStatus
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# 商家相关
class MerchantRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    contact: str = Field(..., pattern="^1[3-9]\d{9}$")

class MerchantResponse(BaseModel):
    id: int
    name: str
    contact: str
    rating: float
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# 商品相关
class ProductRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    category: str = Field(..., min_length=1, max_length=100)
    stock: int = Field(..., ge=0)
    price: float = Field(..., gt=0)
    merchant_id: int

class ProductResponse(BaseModel):
    id: int
    name: str
    category: str
    stock: int
    price: float
    merchant_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# 认证相关
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# 订单相关
class OrderItemRequest(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)

class CreateOrderRequest(BaseModel):
    userId: int
    customerName: str = Field(..., min_length=1, max_length=200)
    items: List[OrderItemRequest]

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float
    
    model_config = ConfigDict(from_attributes=True)

class OrderResponse(BaseModel):
    id: int
    user_id: int
    customer_name: str
    amount: float
    status: OrderStatus
    items: List[OrderItemResponse]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
