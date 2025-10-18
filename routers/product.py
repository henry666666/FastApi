from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db
from models import ProductRequest, ProductResponse
from service.product_service import ProductService

router = APIRouter(prefix="/api/products", tags=["products"])

@router.post("", response_model=ProductResponse, status_code=201)
def create_product(
    request: ProductRequest,
    db: Session = Depends(get_db)
):
    """
    创建商品
    
    - **name**: 商品名称
    - **category**: 商品分类
    - **stock**: 库存数量
    - **price**: 商品价格
    - **merchantId**: 所属商家ID
    """
    return ProductService.create_product(db, request)

@router.get("/{id}", response_model=ProductResponse)
def get_product_by_id(
    id: int,
    db: Session = Depends(get_db)
):
    """
    根据ID查询商品
    """
    return ProductService.get_product_by_id(db, id)

@router.get("", response_model=List[ProductResponse])
def get_all_products(
    category: Optional[str] = Query(None, description="商品分类"),
    merchantId: Optional[int] = Query(None, description="商家ID"),
    name: Optional[str] = Query(None, description="商品名称搜索关键词"),
    available: Optional[bool] = Query(None, description="是否有库存"),
    db: Session = Depends(get_db)
):
    """
    查询所有商品，支持多种筛选条件
    
    - **category**: 按分类查询
    - **merchantId**: 按商家查询
    - **name**: 按名称搜索
    - **available**: 查询有库存的商品
    """
    return ProductService.get_all_products(
        db,
        category=category,
        merchant_id=merchantId,
        name=name,
        available=available
    )

@router.put("/{id}", response_model=ProductResponse)
def update_product(
    id: int,
    request: ProductRequest,
    db: Session = Depends(get_db)
):
    """
    更新商品信息
    
    - **name**: 商品名称
    - **category**: 商品分类
    - **stock**: 库存数量
    - **price**: 商品价格
    - **merchantId**: 所属商家ID
    """
    return ProductService.update_product(db, id, request)

@router.put("/{id}/stock", response_model=ProductResponse)
def update_product_stock(
    id: int,
    stock: int = Query(..., description="新库存数量", ge=0),
    db: Session = Depends(get_db)
):
    """
    更新商品库存
    
    - **stock**: 新库存数量
    """
    return ProductService.update_product_stock(db, id, stock)

@router.delete("/{id}", status_code=204)
def delete_product(
    id: int,
    db: Session = Depends(get_db)
):
    """
    删除商品
    """
    ProductService.delete_product(db, id)
    return None