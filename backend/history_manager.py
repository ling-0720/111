import sqlite3
from datetime import datetime


class HistoryManager:
    def __init__(self, db_path='scan_history.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """初始化数据库表"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
               CREATE TABLE IF NOT EXISTS scan_history (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   scan_id TEXT UNIQUE,
                   timestamp TEXT,
                   target TEXT,
                   scan_type TEXT,
                   vulnerabilities_found INTEGER,
                   status TEXT
               )
           ''')
        conn.commit()
        conn.close()

    def add_record(self, scan_data):
        """添加扫描记录（与前端scanData字段匹配）"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
               INSERT INTO scan_history 
               (scan_id, timestamp, target, scan_type, vulnerabilities_found, status)
               VALUES (?, ?, ?, ?, ?, ?)
           ''', (
            scan_data['scan_id'],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            scan_data['target'],
            scan_data['scan_type'],
            len(scan_data['found_vulnerabilities']),
            scan_data['status']
        ))
        conn.commit()
        conn.close()

    def get_history(self, limit=20):
        """获取最近的扫描记录"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
               SELECT scan_id, timestamp, target, scan_type, vulnerabilities_found, status 
               FROM scan_history 
               ORDER BY timestamp DESC 
               LIMIT ?
           ''', (limit,))
        records = c.fetchall()
        conn.close()
        return [{
            'scan_id': row[0],
            'timestamp': row[1],
            'target': row[2],
            'scan_type': row[3],
            'vulnerabilities_found': row[4],
            'status': row[5]
        } for row in records]


def get_history(self, limit=20, offset=0):  # 添加 offset 参数
    try:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # 使用 OFFSET 关键字实现分页
        c.execute('''
            SELECT scan_id, timestamp, target, scan_type, vulnerabilities_found, status
            FROM scan_history
            ORDER BY timestamp DESC
            LIMIT ? OFFSET ?
        ''', (limit, offset))  # 传递两个参数

        rows = c.fetchall()
        conn.close()

        return [{
            'scan_id': row[0],
            'timestamp': row[1],
            'target': row[2],
            'scan_type': row[3],
            'vulnerabilities_found': row[4],
            'status': row[5]
        } for row in rows]
    except Exception as e:
        print(f"查询历史记录失败: {e}")
        raise
