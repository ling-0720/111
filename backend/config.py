# 扫描器配置
SCAN_CONFIG = {
    'timeout': 3600,
    'concurrent_scans': 5,
    'default_ports': '1-1000'
}

# Metasploit配置
METASPLOIT_CONFIG = {
    'host': '127.0.0.1',
    'port': 55553,
    'user': 'msf',
    'password': 'your_password',
    'ssl': True
}

# 数据库配置
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'database': 'vuln_scanner',
    'user': 'root',
    'password': 'your_password'
}

# 日志配置
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'log_dir': 'logs'
} 