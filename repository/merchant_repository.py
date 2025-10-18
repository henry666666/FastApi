from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Merchant
from exceptions import ResourceNotFoundException

class MerchantRepository:
    """
    商家数据访问层
    """
    
    @staticmethod
    def save(db: Session, merchant: Merchant) -> Merchant:
        """
        保存商家
        
        Args:
            db: 数据库会话
            merchant: 商家对象
            
        Returns:
            保存后的商家对象
        """
        db.add(merchant)
        db.commit()
        db.refresh(merchant)
        return merchant
    
    @staticmethod
    def find_by_id(db: Session, merchant_id: int) -> Merchant:
        """
        根据ID查找商家
        
        Args:
            db: 数据库会话
            merchant_id: 商家ID
            
        Returns:
            商家对象
            
        Raises:
            ResourceNotFoundException: 商家不存在
        """
        merchant = db.query(Merchant).filter(Merchant.id == merchant_id).first()
        if not merchant:
            raise ResourceNotFoundException("Merchant", merchant_id)
        return merchant
    
    @staticmethod
    def find_all(db: Session, name: Optional[str] = None, min_rating: Optional[float] = None) -> List[Merchant]:
        """
        查找所有商家，支持按名称和评分筛选
        
        Args:
            db: 数据库会话
            name: 商家名称搜索关键词
            min_rating: 最低评分
            
        Returns:
            商家列表
        """
        query = db.query(Merchant)
        
        if name:
            query = query.filter(Merchant.name.like(f"%{name}%"))
        
        if min_rating is not None:
            query = query.filter(Merchant.rating >= min_rating)
        
        return query.all()
    
    @staticmethod
    def update(db: Session, merchant_id: int, name: Optional[str] = None, contact: Optional[str] = None) -> Merchant:
        """
        更新商家信息
        
        Args:
            db: 数据库会话
            merchant_id: 商家ID
            name: 商家名称
            contact: 联系方式
            
        Returns:
            更新后的商家对象
        """
        merchant = MerchantRepository.find_by_id(db, merchant_id)
        
        if name is not None:
            merchant.name = name
        if contact is not None:
            merchant.contact = contact
        
        db.commit()
        db.refresh(merchant)
        return merchant
    
    @staticmethod
    def update_rating(db: Session, merchant_id: int, rating: float) -> Merchant:
        """
        更新商家评分
        
        Args:
            db: 数据库会话
            merchant_id: 商家ID
            rating: 新评分
            
        Returns:
            更新后的商家对象
        """
        merchant = MerchantRepository.find_by_id(db, merchant_id)
        merchant.rating = rating
        db.commit()
        db.refresh(merchant)
        return merchant
    
    @staticmethod
    def delete(db: Session, merchant_id: int) -> None:
        """
        删除商家
        
        Args:
            db: 数据库会话
            merchant_id: 商家ID
        """
        merchant = MerchantRepository.find_by_id(db, merchant_id)
        db.delete(merchant)
        db.commit()