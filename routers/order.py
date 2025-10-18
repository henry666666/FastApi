from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db
from models import CreateOrderRequest, OrderResponse
from service.order_service import OrderService

router = APIRouter(prefix="/api/orders", tags=["orders"])

@router.post("/place", response_model=OrderResponse, status_code=201)
def place_order(
    request: CreateOrderRequest,
    db: Session = Depends(get_db)
):
    """
    下单接口
    
    - **userId**: 用户ID
    - **customerName**: 客户名称
    - **items**: 订单商品列表
      - **productId**: 商品ID
      - **quantity**: 数量
    """
    return OrderService.place_order(db, request)

@router.get("/{id}", response_model=OrderResponse)
def get_order_by_id(
    id: int,
    db: Session = Depends(get_db)
):
    """
    根据ID查询订单
    """
    return OrderService.get_order_by_id(db, id)

@router.get("", response_model=List[OrderResponse])
def get_all_orders(
    db: Session = Depends(get_db)
):
    """
    查询所有订单
    """
    return OrderService.get_all_orders(db)

@router.get("/user/{userId}", response_model=List[OrderResponse])
def get_orders_by_user_id(
    userId: int,
    db: Session = Depends(get_db)
):
    """
    查询用户的所有订单
    """
    return OrderService.get_orders_by_user_id(db, userId)

@router.post("/{id}/confirm", response_model=OrderResponse)
def confirm_order(
    id: int,
    db: Session = Depends(get_db)
):
    """
    确认订单
    """
    return OrderService.confirm_order(db, id)

@router.post("/{id}/cancel", response_model=OrderResponse)
def cancel_order(
    id: int,
    db: Session = Depends(get_db)
):
    """
    取消订单
    """
    return OrderService.cancel_order(db, id)