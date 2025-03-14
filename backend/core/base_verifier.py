from abc import ABC, abstractmethod
from typing import Dict, Optional
from datetime import datetime
from ..models.vulnerability import Vulnerability
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class BaseVerifier(ABC):
    """漏洞验证器基类"""
    
    def __init__(self, config: Dict = None):
        """
        初始化验证器
        
        Args:
            config: 验证器配置
        """
        self.config = config or {}
        self.logger = logger
        self._initialize_verifier()
    
    @abstractmethod
    def _initialize_verifier(self):
        """初始化验证器，子类必须实现"""
        pass
    
    @abstractmethod
    def verify(self, vulnerability: Vulnerability, target_info: Dict) -> Dict:
        """
        验证漏洞是否存在
        
        Args:
            vulnerability: 待验证的漏洞对象
            target_info: 目标信息
            
        Returns:
            Dict: 验证结果
        """
        pass
    
    @abstractmethod
    def get_verification_status(self, verify_id: str) -> Dict:
        """
        获取验证任务状态
        
        Args:
            verify_id: 验证任务ID
            
        Returns:
            Dict: 验证状态信息
        """
        pass

class VerificationException(Exception):
    """验证异常基类"""
    pass

class VerificationFailedException(VerificationException):
    """验证失败异常"""
    pass 