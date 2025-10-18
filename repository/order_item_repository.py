from sqlalchemy.orm import Session
from typing import List
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import OrderItem
from exceptions import ResourceNotFoundException

class OrderItemRepository:
    """
    订单详情数据访问层
    """
    
    @staticmethod
    def save(db: Session, order_item: OrderItem) -> OrderItem:
        """
        保存订单详情
        
        Args:
            db: 数据库会话
            order_item: 订单详情对象
            
        Returns:
            保存后的订单详情对象
        """
        db.add(order_item)
        db.commit()
        db.refresh(order_item)
        return order_item
    
    @staticmethod
    def save_all(db: Session, order_items: List[OrderItem]) -> List[OrderItem]:
        """
        批量保存订单详情
        
        Args:
            db: 数据库会话
            order_items: 订单详情列表
            
        Returns:
            保存后的订单详情列表
        """
        for item in order_items:
            db.add(item)
        db.commit()
        return order_items
    
    @staticmethod
    def find_by_id(db: Session, order_item_id: int) -> OrderItem:
        """
        根据ID查找订单详情
        
        Args:
            db: 数据库会话
            order_item_id: 订单详情ID
            
        Returns:
            订单详情对象
            
        Raises:
            ResourceNotFoundException: 订单详情不存在
        """
        order_item = db.query(OrderItem).filter(OrderItem.id == order_item_id).first()
        if not order_item:
            raise ResourceNotFoundException("OrderItem", order_item_id)
        return order_item
    
    @staticmethod
    def find_by_order_id(db: Session, order_id: int) -> List[OrderItem]:
        """
        根据订单ID查找所有订单详情
        
        Args:
            db: 数据库会话
            order_id: 订单ID
            
        Returns:
            订单详情列表
        """
        return db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    
    @staticmethod
    def delete(db: Session, order_item_id: int) -> None:
        """
        删除订单详情
        
        Args:
            db: 数据库会话
            order_item_id: 订单详情ID
        """
        order_item = OrderItemRepository.find_by_id(db, order_item_id)
        db.delete(order_item)
        db.commit()
    
    @staticmethod
    def delete_by_order_id(db: Session, order_id: int) -> None:
        """
        删除订单的所有详情
        
        Args:
            db: 数据库会话
            order_id: 订单ID
        """
        db.query(OrderItem).filter(OrderItem.order_id == order_id).delete()
        db.commit()