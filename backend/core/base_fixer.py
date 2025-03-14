from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from datetime import datetime
from ..models.vulnerability import Vulnerability
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class BaseFixer(ABC):
    """漏洞修复模块基类"""
    
    def __init__(self, config: Dict = None):
        """
        初始化修复模块
        
        Args:
            config: 配置信息
        """
        self.config = config or {}
        self.logger = logger
        self._initialize_fixer()
    
    @abstractmethod
    def _initialize_fixer(self):
        """初始化修复环境"""
        pass
    
    @abstractmethod
    def fix(self, vulnerability: Vulnerability, target_info: Dict) -> Dict:
        """
        执行漏洞修复
        
        Args:
            vulnerability: 待修复的漏洞
            target_info: 目标信息
            
        Returns:
            Dict: 修复结果
        """
        pass
    
    @abstractmethod
    def verify_fix(self, vulnerability: Vulnerability, fix_id: str) -> Dict:
        """
        验证修复结果
        
        Args:
            vulnerability: 已修复的漏洞
            fix_id: 修复任务ID
            
        Returns:
            Dict: 验证结果
        """
        pass
    
    @abstractmethod
    def rollback(self, fix_id: str) -> bool:
        """
        回滚修复操作
        
        Args:
            fix_id: 修复任务ID
            
        Returns:
            bool: 是否成功回滚
        """
        pass
    
    @abstractmethod
    def get_fix_status(self, fix_id: str) -> Dict:
        """
        获取修复任务状态
        
        Args:
            fix_id: 修复任务ID
            
        Returns:
            Dict: 任务状态信息
        """
        pass

class FixException(Exception):
    """修复异常基类"""
    pass

class FixFailedException(FixException):
    """修复失败异常"""
    pass

class RollbackFailedException(FixException):
    """回滚失败异常"""
    pass 