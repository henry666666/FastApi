from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db
from models import MerchantRequest, MerchantResponse
from service.merchant_service import MerchantService

router = APIRouter(prefix="/api/merchants", tags=["merchants"])

@router.post("", response_model=MerchantResponse, status_code=201)
def create_merchant(
    request: MerchantRequest,
    db: Session = Depends(get_db)
):
    """
    创建商家
    
    - **name**: 商家名称
    - **contact**: 联系方式（手机号）
    """
    return MerchantService.create_merchant(db, request)

@router.get("/{id}", response_model=MerchantResponse)
def get_merchant_by_id(
    id: int,
    db: Session = Depends(get_db)
):
    """
    根据ID查询商家
    """
    return MerchantService.get_merchant_by_id(db, id)

@router.get("", response_model=List[MerchantResponse])
def get_all_merchants(
    name: Optional[str] = Query(None, description="商家名称搜索关键词"),
    minRating: Optional[float] = Query(None, description="最低评分", ge=0, le=5),
    db: Session = Depends(get_db)
):
    """
    查询所有商家，支持筛选
    
    - **name**: 按名称搜索
    - **minRating**: 按最低评分筛选
    """
    return MerchantService.get_all_merchants(db, name=name, min_rating=minRating)

@router.put("/{id}", response_model=MerchantResponse)
def update_merchant(
    id: int,
    request: MerchantRequest,
    db: Session = Depends(get_db)
):
    """
    更新商家信息
    
    - **name**: 商家名称
    - **contact**: 联系方式
    """
    return MerchantService.update_merchant(db, id, request)

@router.put("/{id}/rating", response_model=MerchantResponse)
def update_merchant_rating(
    id: int,
    rating: float = Query(..., description="新评分", ge=0, le=5),
    db: Session = Depends(get_db)
):
    """
    更新商家评分
    
    - **rating**: 新评分（0-5之间）
    """
    return MerchantService.update_merchant_rating(db, id, rating)

@router.delete("/{id}", status_code=204)
def delete_merchant(
    id: int,
    db: Session = Depends(get_db)
):
    """
    删除商家
    """
    MerchantService.delete_merchant(db, id)
    return None