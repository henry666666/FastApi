from fastapi import HTTPException, status

class ResourceNotFoundException(HTTPException):
    """资源未找到异常"""
    def __init__(self, resource_name: str, resource_id: int):
        self.resource_name = resource_name
        self.resource_id = resource_id
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource_name} with id {resource_id} not found"
        )

class BusinessException(HTTPException):
    """业务逻辑异常"""
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(
            status_code=status_code,
            detail=detail
        )

class ValidationException(HTTPException):
    """数据验证异常"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )

class InsufficientStockException(BusinessException):
    """库存不足异常"""
    def __init__(self, product_id: int, required: int, available: int):
        super().__init__(
            detail=f"Insufficient stock for product {product_id}. Required: {required}, Available: {available}"
        )

class DuplicateResourceException(BusinessException):
    """资源重复异常"""
    def __init__(self, resource_name: str, field: str, value: str):
        super().__init__(
            detail=f"{resource_name} with {field} '{value}' already exists"
        )