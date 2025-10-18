from typing import List, Optional
from sqlalchemy.orm import Session
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Product, ProductRequest, ProductResponse
from repository.product_repository import ProductRepository
from repository.merchant_repository import MerchantRepository
from utils.validation_util import validate_required, validate_positive_number
from exceptions import BusinessException

class ProductService:
    """
    商品业务逻辑层
    """
    
    @staticmethod
    def create_product(db: Session, request: ProductRequest) -> ProductResponse:
        """
        创建商品
        
        Args:
            db: 数据库会话
            request: 商品创建请求
            
        Returns:
            商品响应对象
        """
        # 验证输入
        validate_required(request.name, "name")
        validate_required(request.category, "category")
        validate_positive_number(request.price, "price")
        
        if request.stock < 0:
            raise BusinessException("Stock cannot be negative")
        
        # 验证商家是否存在
        MerchantRepository.find_by_id(db, request.merchant_id)
        
        # 创建商品
        product = Product(
            name=request.name,
            category=request.category,
            stock=request.stock,
            price=request.price,
            merchant_id=request.merchant_id
        )
        
        # 保存商品
        saved_product = ProductRepository.save(db, product)
        
        # 返回响应对象
        return ProductResponse.model_validate(saved_product)
    
    @staticmethod
    def get_product_by_id(db: Session, product_id: int) -> ProductResponse:
        """
        根据ID获取商品
        
        Args:
            db: 数据库会话
            product_id: 商品ID
            
        Returns:
            商品响应对象
        """
        product = ProductRepository.find_by_id(db, product_id)
        return ProductResponse.model_validate(product)
    
    @staticmethod
    def get_all_products(
        db: Session,
        category: Optional[str] = None,
        merchant_id: Optional[int] = None,
        name: Optional[str] = None,
        available: Optional[bool] = None
    ) -> List[ProductResponse]:
        """
        获取所有商品，支持多种筛选条件
        
        Args:
            db: 数据库会话
            category: 商品分类
            merchant_id: 商家ID
            name: 商品名称搜索关键词
            available: 是否有库存
            
        Returns:
            商品响应对象列表
        """
        products = ProductRepository.find_all(
            db,
            category=category,
            merchant_id=merchant_id,
            name=name,
            available=available
        )
        return [ProductResponse.model_validate(product) for product in products]
    
    @staticmethod
    def update_product(
        db: Session,
        product_id: int,
        request: ProductRequest
    ) -> ProductResponse:
        """
        更新商品信息
        
        Args:
            db: 数据库会话
            product_id: 商品ID
            request: 商品更新请求
            
        Returns:
            更新后的商品响应对象
        """
        # 验证输入
        validate_required(request.name, "name")
        validate_required(request.category, "category")
        validate_positive_number(request.price, "price")
        
        if request.stock < 0:
            raise BusinessException("Stock cannot be negative")
        
        # 验证商家是否存在
        MerchantRepository.find_by_id(db, request.merchant_id)
        
        # 更新商品
        updated_product = ProductRepository.update(
            db,
            product_id,
            name=request.name,
            category=request.category,
            stock=request.stock,
            price=request.price
        )
        
        # 返回响应对象
        return ProductResponse.model_validate(updated_product)
    
    @staticmethod
    def update_product_stock(db: Session, product_id: int, stock: int) -> ProductResponse:
        """
        更新商品库存
        
        Args:
            db: 数据库会话
            product_id: 商品ID
            stock: 新库存数量
            
        Returns:
            更新后的商品响应对象
        """
        if stock < 0:
            raise BusinessException("Stock cannot be negative")
        
        updated_product = ProductRepository.update_stock(db, product_id, stock)
        return ProductResponse.model_validate(updated_product)
    
    @staticmethod
    def delete_product(db: Session, product_id: int) -> None:
        """
        删除商品
        
        Args:
            db: 数据库会话
            product_id: 商品ID
        """
        ProductRepository.delete(db, product_id)