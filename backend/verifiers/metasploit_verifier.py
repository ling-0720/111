import time
from typing import Dict, Optional
from pymetasploit3.msfrpc import MsfRpcClient
from ..core.base_verifier import BaseVerifier, VerificationException
from ..models.vulnerability import Vulnerability, VulnerabilityStatus
from ..utils.network import resolve_host

class MetasploitVerifier(BaseVerifier):
    """使用Metasploit框架进行漏洞验证"""
    
    def _initialize_verifier(self):
        """初始化Metasploit RPC客户端"""
        try:
            self.client = MsfRpcClient(
                self.config.get('password', 'yourpassword'),
                server=self.config.get('host', '127.0.0.1'),
                port=self.config.get('port', 55553),
                ssl=self.config.get('ssl', True)
            )
            self.logger.info("Metasploit RPC client initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Metasploit RPC client: {e}")
            raise VerificationException(str(e))
    
    def verify(self, vulnerability: Vulnerability, target_info: Dict) -> Dict:
        """
        使用Metasploit验证漏洞
        
        Args:
            vulnerability: 待验证的漏洞
            target_info: 目标信息
            
        Returns:
            Dict: 验证结果
        """
        verify_id = f"VER_{int(time.time())}"
        self.logger.info(f"Starting verification {verify_id} for {vulnerability.vuln_id}")
        
        try:
            # 解析目标地址
            target_host = resolve_host(target_info['host'])
            if not target_host:
                raise VerificationException("Failed to resolve target host")
            
            # 选择合适的验证模块
            module = self._select_verification_module(vulnerability)
            if not module:
                raise VerificationException("No suitable verification module found")
            
            # 配置验证模块
            module_client = self.client.modules.use('auxiliary', module)
            module_client.target = target_host
            module_client.rport = target_info.get('port', 0)
            
            # 运行验证
            self.logger.info(f"Running verification module {module}")
            result = module_client.execute()
            
            # 处理验证结果
            verification_result = self._process_verification_result(result)
            
            # 更新漏洞状态
            if verification_result['verified']:
                vulnerability.status = VulnerabilityStatus.CONFIRMED
            else:
                vulnerability.status = VulnerabilityStatus.FALSE_POSITIVE
            
            return {
                'verify_id': verify_id,
                'status': 'completed',
                'result': verification_result,
                'vulnerability': vulnerability.to_dict()
            }
            
        except Exception as e:
            self.logger.error(f"Verification failed: {str(e)}")
            return {
                'verify_id': verify_id,
                'status': 'failed',
                'error': str(e)
            }
    
    def _select_verification_module(self, vulnerability: Vulnerability) -> Optional[str]:
        """
        选择合适的Metasploit验证模块
        
        Args:
            vulnerability: 漏洞对象
            
        Returns:
            Optional[str]: 模块路径
        """
        # 根据CVE ID查找对应模块
        if vulnerability.cve_id:
            modules = self.client.modules.search(vulnerability.cve_id)
            if modules:
                return modules[0]['fullname']
        
        # 根据漏洞类型选择通用模块
        vuln_type_modules = {
            'sql_injection': 'auxiliary/scanner/sql/sql_injection',
            'rce': 'auxiliary/scanner/http/apache_rce',
            'xss': 'auxiliary/scanner/http/xss'
        }
        
        for vuln_type, module in vuln_type_modules.items():
            if vuln_type in vulnerability.name.lower():
                return module
        
        return None
    
    def _process_verification_result(self, result: Dict) -> Dict:
        """
        处理Metasploit验证结果
        
        Args:
            result: Metasploit返回的结果
            
        Returns:
            Dict: 标准化的验证结果
        """
        return {
            'verified': result.get('status') == 'success',
            'confidence': self._calculate_confidence(result),
            'details': {
                'module_output': result.get('output', ''),
                'session_info': result.get('session_info', {}),
                'verification_time': datetime.now().isoformat()
            }
        }
    
    def _calculate_confidence(self, result: Dict) -> float:
        """
        计算验证结果的可信度
        
        Args:
            result: 验证结果
            
        Returns:
            float: 可信度分数(0-1)
        """
        confidence = 0.0
        
        # 根据不同因素计算可信度
        if result.get('status') == 'success':
            confidence += 0.6
        
        if result.get('session_info'):
            confidence += 0.2
            
        if result.get('output') and len(result['output']) > 100:
            confidence += 0.2
            
        return min(confidence, 1.0)
    
    def get_verification_status(self, verify_id: str) -> Dict:
        """获取验证任务状态"""
        # 在实际实现中，这里应该查询任务状态
        # 当前实现仅返回模拟数据
        return {
            'verify_id': verify_id,
            'status': 'completed',
            'progress': 100,
            'last_update': datetime.now().isoformat()
        } 