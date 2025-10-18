from typing import List
from sqlalchemy.orm import Session, joinedload
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Order, OrderStatus
from exceptions import ResourceNotFoundException

class OrderRepository:
    """
    订单数据访问层
    """
    
    @staticmethod
    def save(db: Session, order: Order) -> Order:
        """
        保存订单
        
        Args:
            db: 数据库会话
            order: 订单对象
            
        Returns:
            保存后的订单对象
        """
        db.add(order)
        db.commit()
        db.refresh(order)
        return order
    
    @staticmethod
    def find_by_id(db: Session, order_id: int) -> Order:
        """
        根据ID查找订单，包含订单商品
        
        Args:
            db: 数据库会话
            order_id: 订单ID
            
        Returns:
            订单对象（包含订单商品）
            
        Raises:
            ResourceNotFoundException: 订单不存在
        """
        order = db.query(Order).options(
            joinedload(Order.order_items)
        ).filter(Order.id == order_id).first()
        
        if not order:
            raise ResourceNotFoundException("Order", order_id)
        
        return order
    
    @staticmethod
    def find_all(db: Session) -> List[Order]:
        """
        查找所有订单
        
        Args:
            db: 数据库会话
            
        Returns:
            订单列表
        """
        return db.query(Order).options(
            joinedload(Order.order_items)
        ).all()
    
    @staticmethod
    def find_by_user_id(db: Session, user_id: int) -> List[Order]:
        """
        根据用户ID查找订单
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            
        Returns:
            订单列表
        """
        return db.query(Order).options(
            joinedload(Order.order_items)
        ).filter(Order.user_id == user_id).all()
    
    @staticmethod
    def update_status(db: Session, order_id: int, status: OrderStatus) -> Order:
        """
        更新订单状态
        
        Args:
            db: 数据库会话
            order_id: 订单ID
            status: 新状态
            
        Returns:
            更新后的订单对象
        """
        order = OrderRepository.find_by_id(db, order_id)
        order.status = status
        db.commit()
        db.refresh(order)
        return order
    
    @staticmethod
    def delete(db: Session, order_id: int) -> None:
        """
        删除订单
        
        Args:
            db: 数据库会话
            order_id: 订单ID
        """
        order = OrderRepository.find_by_id(db, order_id)
        db.delete(order)
        db.commit()