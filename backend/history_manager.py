import sqlite3
from datetime import datetime

class HistoryManager:
    def __init__(self, db_path="vulnerability_history.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # 创建历史记录表
        c.execute('''
            CREATE TABLE IF NOT EXISTS scan_history
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             scan_id TEXT,
             timestamp TEXT,
             target_ip TEXT,
             scan_type TEXT,
             vulnerabilities_found INTEGER,
             status TEXT)
        ''')
        
        conn.commit()
        conn.close()
    
    def add_record(self, scan_data):
        """添加新的扫描记录"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            INSERT INTO scan_history
            (scan_id, timestamp, target_ip, scan_type, vulnerabilities_found, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            scan_data["scan_id"],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            scan_data["target"],
            scan_data["scan_type"],
            len(scan_data["found_vulnerabilities"]),
            "完成"
        ))
        
        conn.commit()
        conn.close()
    
    def get_history(self, limit=20):
        """获取历史记录"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            SELECT * FROM scan_history
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        records = c.fetchall()
        conn.close()
        
        return [{
            "id": r[0],
            "scan_id": r[1],
            "timestamp": r[2],
            "target_ip": r[3],
            "scan_type": r[4],
            "vulnerabilities_found": r[5],
            "status": r[6]
        } for r in records] 