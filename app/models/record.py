from .db import get_db

class Record:
    @staticmethod
    def create(amount, category_id, record_date, note=""):
        """新增一筆收支"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO records (amount, category_id, note, record_date) 
            VALUES (?, ?, ?, ?)
            ''',
            (amount, category_id, note, record_date)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_all(order_by="record_date DESC, created_at DESC"):
        """獲取所有收支紀錄（包含分類名稱）"""
        conn = get_db()
        cursor = conn.cursor()
        query = f'''
            SELECT r.*, c.name as category_name, c.type as category_type
            FROM records r
            LEFT JOIN categories c ON r.category_id = c.id
            ORDER BY {order_by}
        '''
        cursor.execute(query)
        records = cursor.fetchall()
        conn.close()
        return records

    @staticmethod
    def get_by_id(record_id):
        """根據 ID 獲取特定紀錄"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT r.*, c.name as category_name, c.type as category_type
            FROM records r
            LEFT JOIN categories c ON r.category_id = c.id
            WHERE r.id = ?
        ''', (record_id,))
        record = cursor.fetchone()
        conn.close()
        return record

    @staticmethod
    def update(record_id, amount, category_id, record_date, note=""):
        """更新收支紀錄"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            '''
            UPDATE records 
            SET amount = ?, category_id = ?, note = ?, record_date = ?
            WHERE id = ?
            ''',
            (amount, category_id, note, record_date, record_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(record_id):
        """刪除收支紀錄"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM records WHERE id = ?', (record_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_summary():
        """獲取收支加總資訊：總收入、總支出、總餘額"""
        conn = get_db()
        cursor = conn.cursor()
        
        # 總收入
        cursor.execute('''
            SELECT COALESCE(SUM(r.amount), 0) as total_income 
            FROM records r
            JOIN categories c ON r.category_id = c.id
            WHERE c.type = 'income'
        ''')
        total_income = cursor.fetchone()['total_income']
        
        # 總支出
        cursor.execute('''
            SELECT COALESCE(SUM(r.amount), 0) as total_expense 
            FROM records r
            JOIN categories c ON r.category_id = c.id
            WHERE c.type = 'expense'
        ''')
        total_expense = cursor.fetchone()['total_expense']
        
        conn.close()
        
        return {
            'total_income': total_income,
            'total_expense': total_expense,
            'balance': total_income - total_expense
        }
