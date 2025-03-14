import nmap
import time
from typing import Dict
from datetime import datetime
from ..core.base_scanner import BaseScanner, ScanInitFailedException, InvalidTargetException
from ..utils.network import resolve_host

class NmapScanner(BaseScanner):
    """使用Nmap进行漏洞扫描"""
    
    def _initialize_scanner(self):
        """初始化Nmap扫描器"""
        try:
            self.scanner = nmap.PortScanner()
            self.logger.info("Nmap scanner initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Nmap scanner: {str(e)}")
            raise ScanInitFailedException(f"Failed to initialize Nmap: {str(e)}")

    def scan(self, target: str, scan_type: str = 'quick') -> Dict:
        """执行漏洞扫描"""
        try:
            # 解析目标地址
            target_host = resolve_host(target)
            if not target_host:
                raise InvalidTargetException("Failed to resolve target host")
            
            # 根据扫描类型选择参数
            if scan_type == 'quick':
                arguments = '-sV -F --version-intensity 5'
            else:
                arguments = '-sV -sC -A -T4'
            
            # 执行扫描
            scan_id = f"SCAN_{int(time.time())}"
            self.logger.info(f"Starting {scan_type} scan {scan_id} on {target}")
            
            result = self.scanner.scan(target_host, arguments=arguments)
            
            return {
                'scan_id': scan_id,
                'target': target,
                'scan_type': scan_type,
                'start_time': datetime.now().isoformat(),
                'status': 'completed',
                'results': result
            }
            
        except Exception as e:
            self.logger.error(f"Scan failed: {str(e)}")
            raise

    def get_scan_status(self, scan_id: str) -> Dict:
        """获取扫描任务状态"""
        return {
            'scan_id': scan_id,
            'status': 'completed',
            'progress': 100,
            'last_update': datetime.now().isoformat()
        } 