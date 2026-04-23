from .db import get_db

class Category:
    @staticmethod
    def create(name, category_type):
        """
        新增分類
        :param name: 分類名稱
        :param category_type: 'income' 或 'expense'
        """
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO categories (name, type) VALUES (?, ?)',
            (name, category_type)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        """獲取所有分類"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM categories ORDER BY type, name')
        categories = cursor.fetchall()
        conn.close()
        return categories

    @staticmethod
    def get_by_id(category_id):
        """根據 ID 獲取特定分類"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM categories WHERE id = ?', (category_id,))
        category = cursor.fetchone()
        conn.close()
        return category

    @staticmethod
    def delete(category_id):
        """刪除分類"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM categories WHERE id = ?', (category_id,))
        conn.commit()
        conn.close()
