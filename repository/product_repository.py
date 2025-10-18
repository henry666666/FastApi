from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Product
from exceptions import ResourceNotFoundException

class ProductRepository:
    """
    商品数据访问层
    """
    
    @staticmethod
    def save(db: Session, product: Product) -> Product:
        """
        保存商品
        
        Args:
            db: 数据库会话
            product: 商品对象
            
        Returns:
            保存后的商品对象
        """
        db.add(product)
        db.commit()
        db.refresh(product)
        return product
    
    @staticmethod
    def find_by_id(db: Session, product_id: int) -> Product:
        """
        根据ID查找商品
        
        Args:
            db: 数据库会话
            product_id: 商品ID
            
        Returns:
            商品对象
            
        Raises:
            ResourceNotFoundException: 商品不存在
        """
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ResourceNotFoundException("Product", product_id)
        return product
    
    @staticmethod
    def find_all(
        db: Session,
        category: Optional[str] = None,
        merchant_id: Optional[int] = None,
        name: Optional[str] = None,
        available: Optional[bool] = None
    ) -> List[Product]:
        """
        查找所有商品，支持多种筛选条件
        
        Args:
            db: 数据库会话
            category: 商品分类
            merchant_id: 商家ID
            name: 商品名称搜索关键词
            available: 是否有库存
            
        Returns:
            商品列表
        """
        query = db.query(Product)
        
        if category:
            query = query.filter(Product.category == category)
        
        if merchant_id:
            query = query.filter(Product.merchant_id == merchant_id)
        
        if name:
            query = query.filter(Product.name.like(f"%{name}%"))
        
        if available is not None:
            if available:
                query = query.filter(Product.stock > 0)
            else:
                query = query.filter(Product.stock <= 0)
        
        return query.all()
    
    @staticmethod
    def update(
        db: Session,
        product_id: int,
        name: Optional[str] = None,
        category: Optional[str] = None,
        stock: Optional[int] = None,
        price: Optional[float] = None
    ) -> Product:
        """
        更新商品信息
        
        Args:
            db: 数据库会话
            product_id: 商品ID
            name: 商品名称
            category: 商品分类
            stock: 库存数量
            price: 商品价格
            
        Returns:
            更新后的商品对象
        """
        product = ProductRepository.find_by_id(db, product_id)
        
        if name is not None:
            product.name = name
        if category is not None:
            product.category = category
        if stock is not None:
            product.stock = stock
        if price is not None:
            product.price = price
        
        db.commit()
        db.refresh(product)
        return product
    
    @staticmethod
    def update_stock(db: Session, product_id: int, stock: int) -> Product:
        """
        更新商品库存
        
        Args:
            db: 数据库会话
            product_id: 商品ID
            stock: 新库存数量
            
        Returns:
            更新后的商品对象
        """
        product = ProductRepository.find_by_id(db, product_id)
        product.stock = stock
        db.commit()
        db.refresh(product)
        return product
    
    @staticmethod
    def delete(db: Session, product_id: int) -> None:
        """
        删除商品
        
        Args:
            db: 数据库会话
            product_id: 商品ID
        """
        product = ProductRepository.find_by_id(db, product_id)
        db.delete(product)
        db.commit()
    
    @staticmethod
    def reduce_stock(db: Session, product_id: int, quantity: int) -> Product:
        """
        减少商品库存
        
        Args:
            db: 数据库会话
            product_id: 商品ID
            quantity: 减少的数量
            
        Returns:
            更新后的商品对象
        """
        product = ProductRepository.find_by_id(db, product_id)
        product.stock -= quantity
        db.commit()
        db.refresh(product)
        return product