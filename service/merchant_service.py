from typing import List, Optional
from sqlalchemy.orm import Session
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Merchant, MerchantRequest, MerchantResponse
from repository.merchant_repository import MerchantRepository
from utils.validation_util import validate_required, validate_phone, validate_positive_number

class MerchantService:
    """
    商家业务逻辑层
    """
    
    @staticmethod
    def create_merchant(db: Session, request: MerchantRequest) -> MerchantResponse:
        """
        创建商家
        
        Args:
            db: 数据库会话
            request: 商家创建请求
            
        Returns:
            商家响应对象
        """
        # 验证输入
        validate_required(request.name, "name")
        validate_phone(request.contact)
        
        # 创建商家
        merchant = Merchant(
            name=request.name,
            contact=request.contact,
            rating=5.0  # 默认评分
        )
        
        # 保存商家
        saved_merchant = MerchantRepository.save(db, merchant)
        
        # 返回响应对象
        return MerchantResponse.model_validate(saved_merchant)
    
    @staticmethod
    def get_merchant_by_id(db: Session, merchant_id: int) -> MerchantResponse:
        """
        根据ID获取商家
        
        Args:
            db: 数据库会话
            merchant_id: 商家ID
            
        Returns:
            商家响应对象
        """
        merchant = MerchantRepository.find_by_id(db, merchant_id)
        return MerchantResponse.model_validate(merchant)
    
    @staticmethod
    def get_all_merchants(
        db: Session,
        name: Optional[str] = None,
        min_rating: Optional[float] = None
    ) -> List[MerchantResponse]:
        """
        获取所有商家，支持筛选
        
        Args:
            db: 数据库会话
            name: 商家名称搜索关键词
            min_rating: 最低评分
            
        Returns:
            商家响应对象列表
        """
        merchants = MerchantRepository.find_all(db, name=name, min_rating=min_rating)
        return [MerchantResponse.model_validate(merchant) for merchant in merchants]
    
    @staticmethod
    def update_merchant(
        db: Session,
        merchant_id: int,
        request: MerchantRequest
    ) -> MerchantResponse:
        """
        更新商家信息
        
        Args:
            db: 数据库会话
            merchant_id: 商家ID
            request: 商家更新请求
            
        Returns:
            更新后的商家响应对象
        """
        # 验证输入
        validate_required(request.name, "name")
        validate_phone(request.contact)
        
        # 更新商家
        updated_merchant = MerchantRepository.update(
            db, 
            merchant_id, 
            name=request.name, 
            contact=request.contact
        )
        
        # 返回响应对象
        return MerchantResponse.model_validate(updated_merchant)
    
    @staticmethod
    def update_merchant_rating(db: Session, merchant_id: int, rating: float) -> MerchantResponse:
        """
        更新商家评分
        
        Args:
            db: 数据库会话
            merchant_id: 商家ID
            rating: 新评分
            
        Returns:
            更新后的商家响应对象
        """
        # 验证评分范围
        if rating < 0 or rating > 5:
            raise ValueError("Rating must be between 0 and 5")
        
        # 更新评分
        updated_merchant = MerchantRepository.update_rating(db, merchant_id, rating)
        
        # 返回响应对象
        return MerchantResponse.model_validate(updated_merchant)
    
    @staticmethod
    def delete_merchant(db: Session, merchant_id: int) -> None:
        """
        删除商家
        
        Args:
            db: 数据库会话
            merchant_id: 商家ID
        """
        MerchantRepository.delete(db, merchant_id)