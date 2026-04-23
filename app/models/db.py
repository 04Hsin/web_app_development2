import sqlite3
import os

DATABASE = 'instance/database.db'

def get_db():
    """
    獲取資料庫連線，並設定 row_factory 使查詢結果可以像字典一樣存取。
    """
    # Ensure instance directory exists
    os.makedirs('instance', exist_ok=True)
    
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(schema_path='database/schema.sql'):
    """
    從 database/schema.sql 初始化資料庫。
    """
    # Ensure instance directory exists
    os.makedirs('instance', exist_ok=True)
    
    with get_db() as conn:
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()

# 當檔案被直接執行時，進行初始化
if __name__ == '__main__':
    # Adjust path if run directly from app/models/db.py
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    schema_path = os.path.join(project_root, 'database', 'schema.sql')
    DATABASE = os.path.join(project_root, 'instance', 'database.db')
    init_db(schema_path)
    print("Database initialized successfully.")
