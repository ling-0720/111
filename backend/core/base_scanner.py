from abc import ABC, abstractmethod
import logging
from typing import Dict, List, Optional
from datetime import datetime
from ..models.vulnerability import Vulnerability
from ..models.scan_result import ScanResult
from ..utils.logger import setup_logger
from ..config import SCAN_CONFIG

logger = setup_logger(__name__)

class ScannerException(Exception):
    """扫描器异常基类"""
    pass

class ScanInitFailedException(ScannerException):
    """扫描器初始化失败异常"""
    pass

class InvalidTargetException(ScannerException):
    """无效目标异常"""
    pass

class BaseScanner(ABC):
    """漏洞扫描器基类"""
    
    def __init__(self, config: Dict = None):
        """
        初始化扫描器
        
        Args:
            config: 扫描器配置
        """
        self.config = config or {}
        self.logger = logger
        self._initialize_scanner()
    
    @abstractmethod
    def _initialize_scanner(self):
        """初始化扫描器，子类必须实现"""
        pass
    
    @abstractmethod
    def scan(self, target: str, scan_type: str = 'quick') -> Dict:
        """
        执行漏洞扫描
        
        Args:
            target: 扫描目标
            scan_type: 扫描类型
            
        Returns:
            Dict: 扫描结果
        """
        pass
    
    @abstractmethod
    def get_scan_status(self, scan_id: str) -> Dict:
        """
        获取扫描任务状态
        
        Args:
            scan_id: 扫描任务ID
            
        Returns:
            Dict: 扫描状态信息
        """
        pass 