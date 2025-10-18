from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from exceptions import BusinessException, ResourceNotFoundException, ValidationException

async def global_exception_handler(request: Request, exc: Exception):
    """
    全局异常处理器
    """
    # 处理请求验证错误
    if isinstance(exc, RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "status": "error",
                "message": "Validation error",
                "details": exc.errors()
            }
        )
    
    # 处理业务异常
    if isinstance(exc, BusinessException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": "error",
                "message": exc.detail
            }
        )
    
    # 处理资源未找到异常
    if isinstance(exc, ResourceNotFoundException):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "status": "error",
                "message": exc.detail
            }
        )
    
    # 处理验证异常
    if isinstance(exc, ValidationException):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "status": "error",
                "message": exc.detail
            }
        )
    
    # 处理Pydantic验证错误
    if isinstance(exc, ValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "status": "error",
                "message": "Validation error",
                "details": exc.errors()
            }
        )
    
    # 处理其他所有异常
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "message": "Internal server error",
            "details": str(exc)
        }
    )