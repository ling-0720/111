import sqlite3

class UserManager:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             username TEXT UNIQUE,
             password TEXT,
             role TEXT)
        ''')
        conn.commit()
        conn.close()

    def register_user(self, username, password, role="user"):
        """注册用户"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, password, role))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def authenticate_user(self, username, password):
        """验证用户"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = c.fetchone()
        conn.close()
        return user

    def get_user_role(self, username):
        """获取用户角色"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT role FROM users WHERE username = ?', (username,))
        role = c.fetchone()
        conn.close()
        return role[0] if role else None