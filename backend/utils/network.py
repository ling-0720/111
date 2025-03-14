import re
import socket
from typing import Union, Optional
from ipaddress import ip_address, ip_network

def is_valid_target(target: str) -> bool:
    """验证目标是否为有效的IP地址、域名或网段
    
    Args:
        target: 目标地址字符串
        
    Returns:
        bool: 目标是否有效
    """
    
    # 检查是否为IP地址
    try:
        ip_address(target)
        return True
    except ValueError:
        pass
    
    # 检查是否为CIDR网段
    try:
        ip_network(target, strict=False)
        return True
    except ValueError:
        pass
    
    # 检查是否为域名
    if is_valid_domain(target):
        return True
    
    return False

def is_valid_domain(domain: str) -> bool:
    """验证是否为有效的域名
    
    Args:
        domain: 域名字符串
        
    Returns:
        bool: 是否为有效域名
    """
    
    domain_pattern = re.compile(
        r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}'
        r'[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    )
    return bool(domain_pattern.match(domain))

def resolve_host(host: str) -> Optional[str]:
    """
    解析主机名为IP地址
    
    Args:
        host: 主机名或IP地址
        
    Returns:
        Optional[str]: 解析后的IP地址，解析失败返回None
    """
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        return None 