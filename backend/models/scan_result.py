from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
from .vulnerability import Vulnerability

@dataclass
class ScanResult:
    """扫描结果数据模型
    
    属性:
        scan_id (str): 扫描任务唯一标识符
        target (str): 扫描目标
        scan_type (str): 扫描类型（quick/full/vuln）
        start_time (datetime): 扫描开始时间
        end_time (Optional[datetime]): 扫描结束时间
        status (str): 扫描状态（running/completed/failed）
        vulnerabilities (List[Vulnerability]): 发现的漏洞列表
        raw_result (Dict): 原始扫描结果
        error_message (Optional[str]): 错误信息（如果有）
    """
    
    scan_id: str
    target: str
    scan_type: str
    start_time: datetime
    vulnerabilities: List[Vulnerability]
    raw_result: Dict
    end_time: Optional[datetime] = None
    status: str = "running"
    error_message: Optional[str] = None

    def to_dict(self) -> Dict:
        """将扫描结果转换为字典格式"""
        return {
            "scan_id": self.scan_id,
            "target": self.target,
            "scan_type": self.scan_type,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "status": self.status,
            "vulnerabilities": [v.to_dict() for v in self.vulnerabilities],
            "error_message": self.error_message
        } 