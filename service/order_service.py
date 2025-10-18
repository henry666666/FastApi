from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Order, OrderItem, OrderStatus, CreateOrderRequest, OrderResponse
from repository.order_repository import OrderRepository
from repository.order_item_repository import OrderItemRepository
from repository.product_repository import ProductRepository
from repository.user_repository import UserRepository
from exceptions import InsufficientStockException, BusinessException

class OrderService:
    """
    订单业务逻辑层
    """
    
    @staticmethod
    def place_order(db: Session, request: CreateOrderRequest) -> OrderResponse:
        """
        下单
        
        Args:
            db: 数据库会话
            request: 创建订单请求
            
        Returns:
            订单响应对象
            
        Raises:
            InsufficientStockException: 库存不足
        """
        # 验证用户是否存在
        UserRepository.find_by_id(db, request.userId)
        
        # 验证所有商品是否存在并检查库存
        total_amount = 0.0
        order_items = []
        
        for item_request in request.items:
            # 获取商品
            product = ProductRepository.find_by_id(db, item_request.productId)
            
            # 检查库存
            if product.stock < item_request.quantity:
                raise InsufficientStockException(
                    product.id, 
                    item_request.quantity, 
                    product.stock
                )
            
            # 计算金额
            item_total = product.price * item_request.quantity
            total_amount += item_total
            
            # 创建订单详情对象
            order_item = OrderItem(
                product_id=product.id,
                quantity=item_request.quantity,
                price=product.price
            )
            order_items.append(order_item)
        
        # 创建订单
        order = Order(
            user_id=request.userId,
            customer_name=request.customerName,
            amount=total_amount,
            status=OrderStatus.CREATED
        )
        
        # 保存订单
        saved_order = OrderRepository.save(db, order)
        
        # 为订单详情设置订单ID
        for item in order_items:
            item.order_id = saved_order.id
        
        # 保存订单详情
        OrderItemRepository.save_all(db, order_items)
        
        # 减少商品库存
        for item_request in request.items:
            product = ProductRepository.find_by_id(db, item_request.productId)
            ProductRepository.reduce_stock(db, product.id, item_request.quantity)
        
        # 获取完整的订单信息
        complete_order = OrderRepository.find_by_id(db, saved_order.id)
        
        # 返回响应对象
        return OrderResponse.model_validate(complete_order)
    
    @staticmethod
    def get_order_by_id(db: Session, order_id: int) -> OrderResponse:
        """
        根据ID获取订单
        
        Args:
            db: 数据库会话
            order_id: 订单ID
            
        Returns:
            订单响应对象
        """
        order = OrderRepository.find_by_id(db, order_id)
        return OrderResponse.model_validate(order)
    
    @staticmethod
    def get_all_orders(db: Session) -> List[OrderResponse]:
        """
        获取所有订单
        
        Args:
            db: 数据库会话
            
        Returns:
            订单响应对象列表
        """
        orders = OrderRepository.find_all(db)
        return [OrderResponse.model_validate(order) for order in orders]
    
    @staticmethod
    def get_orders_by_user_id(db: Session, user_id: int) -> List[OrderResponse]:
        """
        根据用户ID获取订单
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            
        Returns:
            订单响应对象列表
        """
        # 验证用户是否存在
        UserRepository.find_by_id(db, user_id)
        
        orders = OrderRepository.find_by_user_id(db, user_id)
        return [OrderResponse.model_validate(order) for order in orders]
    
    @staticmethod
    def confirm_order(db: Session, order_id: int) -> OrderResponse:
        """
        确认订单
        
        Args:
            db: 数据库会话
            order_id: 订单ID
            
        Returns:
            更新后的订单响应对象
        """
        order = OrderRepository.find_by_id(db, order_id)
        
        # 检查订单状态
        if order.status != OrderStatus.CREATED:
            raise BusinessException(f"Cannot confirm order with status: {order.status}")
        
        # 更新状态
        updated_order = OrderRepository.update_status(db, order_id, OrderStatus.CONFIRMED)
        
        # 返回响应对象
        return OrderResponse.model_validate(updated_order)
    
    @staticmethod
    def cancel_order(db: Session, order_id: int) -> OrderResponse:
        """
        取消订单
        
        Args:
            db: 数据库会话
            order_id: 订单ID
            
        Returns:
            更新后的订单响应对象
        """
        order = OrderRepository.find_by_id(db, order_id)
        
        # 检查订单状态
        if order.status in [OrderStatus.CANCELLED, OrderStatus.COMPLETED]:
            raise BusinessException(f"Cannot cancel order with status: {order.status}")
        
        # 更新状态
        updated_order = OrderRepository.update_status(db, order_id, OrderStatus.CANCELLED)
        
        # 恢复库存
        for item in updated_order.order_items:
            product = ProductRepository.find_by_id(db, item.product_id)
            ProductRepository.update_stock(db, product.id, product.stock + item.quantity)
        
        # 返回响应对象
        return OrderResponse.model_validate(updated_order)