from typing import Dict, Optional
from ..models.vulnerability import Vulnerability, Severity, VulnerabilityStatus
import re

def nmap_to_vulnerability(
    host: str,
    port: int,
    protocol: str,
    script_name: str,
    output: str
) -> Optional[Vulnerability]:
    """将Nmap扫描结果转换为标准漏洞对象
    
    Args:
        host: 目标主机
        port: 端口号
        protocol: 协议
        script_name: Nmap脚本名称
        output: 脚本输出结果
        
    Returns:
        Optional[Vulnerability]: 转换后的漏洞对象，如果不是漏洞则返回None
    """
    
    # 提取CVE编号
    cve_pattern = re.compile(r'CVE-\d{4}-\d+')
    cve_matches = cve_pattern.findall(output)
    cve_id = cve_matches[0] if cve_matches else None
    
    # 判断严重程度
    severity = determine_severity(output)
    
    # 提取CVSS分数
    cvss_score = extract_cvss_score(output)
    
    # 创建漏洞对象
    if is_vulnerability_output(script_name, output):
        return Vulnerability(
            vuln_id=f"VULN-{host}-{port}",
            name=script_name,
            description=output,
            severity=severity,
            status=VulnerabilityStatus.UNCONFIRMED,
            cve_id=cve_id,
            cvss_score=cvss_score,
            affected_component=f"{protocol}:{port}",
            technical_details={
                "host": host,
                "port": port,
                "protocol": protocol,
                "script_output": output
            }
        )
    return None

def determine_severity(output: str) -> Severity:
    """根据输出内容判断漏洞严重程度
    
    Args:
        output: Nmap脚本输出内容
        
    Returns:
        Severity: 漏洞严重程度枚举值
    """
    
    # 根据关键词判断严重程度
    if any(word in output.lower() for word in ["critical", "严重", "rce"]):
        return Severity.CRITICAL
    elif any(word in output.lower() for word in ["high", "高危"]):
        return Severity.HIGH
    elif any(word in output.lower() for word in ["medium", "中危"]):
        return Severity.MEDIUM
    elif any(word in output.lower() for word in ["low", "低危"]):
        return Severity.LOW
    return Severity.INFO

def extract_cvss_score(output: str) -> Optional[float]:
    """从输出中提取CVSS分数
    
    Args:
        output: Nmap脚本输出内容
        
    Returns:
        Optional[float]: CVSS分数，如果未找到则返回None
    """
    
    cvss_pattern = re.compile(r'CVSS:(\d+\.\d+)')
    match = cvss_pattern.search(output)
    if match:
        return float(match.group(1))
    return None

def is_vulnerability_output(script_name: str, output: str) -> bool:
    """判断是否为漏洞相关输出
    
    Args:
        script_name: Nmap脚本名称
        output: 脚本输出内容
        
    Returns:
        bool: 是否为漏洞相关输出
    """
    
    vuln_keywords = [
        "vulnerability", "漏洞", "exploit", "attack",
        "overflow", "injection", "bypass", "weak"
    ]
    return (
        "vuln" in script_name.lower() or
        any(keyword in output.lower() for keyword in vuln_keywords)
    ) 