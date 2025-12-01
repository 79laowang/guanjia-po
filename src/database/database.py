import sqlite3
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
from ..utils.config import DB_CONFIG, DEFAULT_CATEGORIES, DEFAULT_INVENTORY_CATEGORIES

class DatabaseManager:
    def __init__(self):
        self.db_path = DB_CONFIG['database_path']
        self.connection = None
        self.connect()
        self.initialize_database()

    def connect(self):
        """连接数据库"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # 使结果可以通过列名访问
            return True
        except Exception as e:
            print(f"数据库连接失败: {e}")
            return False

    def initialize_database(self):
        """初始化数据库表结构"""
        try:
            cursor = self.connection.cursor()

            # 创建分类表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    type TEXT NOT NULL CHECK (type IN ('income', 'expense')),
                    color TEXT DEFAULT '#1890ff',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # 创建账目表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL CHECK (type IN ('income', 'expense')),
                    amount REAL NOT NULL CHECK (amount > 0),
                    category_id INTEGER NOT NULL,
                    description TEXT,
                    date DATE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories (id)
                )
            ''')

            # 创建物品类别表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS item_categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # 创建物品表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category_id INTEGER,
                    quantity REAL DEFAULT 0,
                    unit TEXT DEFAULT '个',
                    unit_price REAL DEFAULT 0,
                    min_quantity REAL DEFAULT 0,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES item_categories (id)
                )
            ''')

            # 创建库存变动记录表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS inventory_transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id INTEGER NOT NULL,
                    type TEXT NOT NULL CHECK (type IN ('in', 'out')),
                    quantity REAL NOT NULL,
                    unit_price REAL DEFAULT 0,
                    reason TEXT,
                    date DATE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (item_id) REFERENCES items (id)
                )
            ''')

            # 创建设置表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            self.connection.commit()

            # 插入默认数据
            self.insert_default_data()

        except Exception as e:
            print(f"数据库初始化失败: {e}")
            self.connection.rollback()

    def insert_default_data(self):
        """插入默认数据"""
        try:
            cursor = self.connection.cursor()

            # 插入默认分类
            for category_type, categories in DEFAULT_CATEGORIES.items():
                for category in categories:
                    cursor.execute('''
                        INSERT OR IGNORE INTO categories (name, type, color)
                        VALUES (?, ?, ?)
                    ''', (category['name'], category_type, category['color']))

            # 插入默认物品分类
            for category in DEFAULT_INVENTORY_CATEGORIES:
                cursor.execute('''
                    INSERT OR IGNORE INTO item_categories (name, description)
                    VALUES (?, ?)
                ''', (category['name'], category['description']))

            self.connection.commit()

        except Exception as e:
            print(f"插入默认数据失败: {e}")
            self.connection.rollback()

    def execute_query(self, query: str, params: tuple = ()) -> List[sqlite3.Row]:
        """执行查询并返回结果"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except Exception as e:
            print(f"查询执行失败: {e}")
            return []

    def execute_update(self, query: str, params: tuple = ()) -> int:
        """执行更新操作并返回影响的行数"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"更新执行失败: {e}")
            self.connection.rollback()
            return 0

    def execute_insert(self, query: str, params: tuple = ()) -> int:
        """执行插入操作并返回插入的ID"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"插入执行失败: {e}")
            self.connection.rollback()
            return 0

    # ========== 分类相关操作 ==========
    def get_categories(self, category_type: Optional[str] = None) -> List[Dict]:
        """获取分类列表"""
        query = "SELECT * FROM categories"
        params = []

        if category_type:
            query += " WHERE type = ?"
            params.append(category_type)

        query += " ORDER BY name"

        rows = self.execute_query(query, tuple(params))
        return [dict(row) for row in rows]

    def add_category(self, name: str, category_type: str, color: str = '#1890ff') -> int:
        """添加分类"""
        query = "INSERT INTO categories (name, type, color) VALUES (?, ?, ?)"
        return self.execute_insert(query, (name, category_type, color))

    def update_category(self, category_id: int, name: str, color: str) -> int:
        """更新分类"""
        query = "UPDATE categories SET name = ?, color = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        return self.execute_update(query, (name, color, category_id))

    def delete_category(self, category_id: int) -> int:
        """删除分类"""
        query = "DELETE FROM categories WHERE id = ?"
        return self.execute_update(query, (category_id,))

    # ========== 账目相关操作 ==========
    def get_accounts(self, filters: Dict = None) -> List[Dict]:
        """获取账目列表"""
        if filters is None:
            filters = {}

        query = '''
            SELECT a.*, c.name as category_name, c.color as category_color
            FROM accounts a
            LEFT JOIN categories c ON a.category_id = c.id
            WHERE 1=1
        '''
        params = []

        if 'type' in filters:
            query += " AND a.type = ?"
            params.append(filters['type'])

        if 'category_id' in filters and filters['category_id']:
            query += " AND a.category_id = ?"
            params.append(filters['category_id'])

        if 'start_date' in filters and filters['start_date']:
            query += " AND a.date >= ?"
            params.append(filters['start_date'])

        if 'end_date' in filters and filters['end_date']:
            query += " AND a.date <= ?"
            params.append(filters['end_date'])

        if 'keyword' in filters and filters['keyword']:
            query += " AND (a.description LIKE ? OR c.name LIKE ?)"
            keyword = f"%{filters['keyword']}%"
            params.extend([keyword, keyword])

        query += " ORDER BY a.date DESC, a.created_at DESC"

        if 'limit' in filters:
            query += " LIMIT ?"
            params.append(filters['limit'])

        rows = self.execute_query(query, tuple(params))
        return [dict(row) for row in rows]

    def add_account(self, account_type: str, amount: float, category_id: int,
                   description: str, date: str) -> int:
        """添加账目"""
        query = '''
            INSERT INTO accounts (type, amount, category_id, description, date)
            VALUES (?, ?, ?, ?, ?)
        '''
        return self.execute_insert(query, (account_type, amount, category_id, description, date))

    def update_account(self, account_id: int, updates: Dict) -> int:
        """更新账目"""
        if not updates:
            return 0

        set_clause = ', '.join([f"{key} = ?" for key in updates.keys()])
        query = f"UPDATE accounts SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        params = list(updates.values()) + [account_id]
        return self.execute_update(query, tuple(params))

    def delete_account(self, account_id: int) -> int:
        """删除账目"""
        query = "DELETE FROM accounts WHERE id = ?"
        return self.execute_update(query, (account_id,))

    # ========== 统计相关操作 ==========
    def get_account_summary(self, start_date: str, end_date: str) -> List[Dict]:
        """获取账目汇总"""
        query = '''
            SELECT type, SUM(amount) as total, COUNT(*) as count
            FROM accounts
            WHERE date BETWEEN ? AND ?
            GROUP BY type
        '''
        rows = self.execute_query(query, (start_date, end_date))
        return [dict(row) for row in rows]

    def get_category_summary(self, start_date: str, end_date: str,
                           category_type: Optional[str] = None) -> List[Dict]:
        """获取分类汇总"""
        query = '''
            SELECT c.name, c.color, COALESCE(SUM(a.amount), 0) as total,
                   COALESCE(COUNT(a.id), 0) as count
            FROM categories c
            LEFT JOIN accounts a ON c.id = a.category_id
                AND a.date BETWEEN ? AND ?
        '''
        params = [start_date, end_date]

        if category_type:
            query += " WHERE c.type = ?"
            params.append(category_type)

        query += " GROUP BY c.id, c.name, c.color ORDER BY total DESC"

        rows = self.execute_query(query, tuple(params))
        return [dict(row) for row in rows]

    # ========== 物品相关操作 ==========
    def get_items(self, filters: Dict = None) -> List[Dict]:
        """获取物品列表"""
        if filters is None:
            filters = {}

        query = '''
            SELECT i.*, ic.name as category_name
            FROM items i
            LEFT JOIN item_categories ic ON i.category_id = ic.id
            WHERE 1=1
        '''
        params = []

        if 'category_id' in filters and filters['category_id']:
            query += " AND i.category_id = ?"
            params.append(filters['category_id'])

        if 'keyword' in filters and filters['keyword']:
            query += " AND (i.name LIKE ? OR i.description LIKE ?)"
            keyword = f"%{filters['keyword']}%"
            params.extend([keyword, keyword])

        if 'low_stock' in filters and filters['low_stock']:
            query += " AND i.quantity <= i.min_quantity AND i.min_quantity > 0"

        query += " ORDER BY i.name"

        rows = self.execute_query(query, tuple(params))
        return [dict(row) for row in rows]

    def add_item(self, name: str, category_id: Optional[int], quantity: float,
                unit: str, unit_price: float, min_quantity: float, description: str) -> int:
        """添加物品"""
        query = '''
            INSERT INTO items (name, category_id, quantity, unit, unit_price, min_quantity, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        return self.execute_insert(query, (name, category_id, quantity, unit, unit_price, min_quantity, description))

    def update_item(self, item_id: int, updates: Dict) -> int:
        """更新物品"""
        if not updates:
            return 0

        set_clause = ', '.join([f"{key} = ?" for key in updates.keys()])
        query = f"UPDATE items SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        params = list(updates.values()) + [item_id]
        return self.execute_update(query, tuple(params))

    def delete_item(self, item_id: int) -> int:
        """删除物品"""
        query = "DELETE FROM items WHERE id = ?"
        return self.execute_update(query, (item_id,))

    # ========== 库存变动相关操作 ==========
    def add_inventory_transaction(self, item_id: int, transaction_type: str,
                                 quantity: float, unit_price: float, reason: str, date: str) -> int:
        """添加库存变动记录"""
        # 先添加变动记录
        query = '''
            INSERT INTO inventory_transactions (item_id, type, quantity, unit_price, reason, date)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        result = self.execute_insert(query, (item_id, transaction_type, quantity, unit_price, reason, date))

        # 更新物品库存
        if transaction_type == 'in':
            update_query = "UPDATE items SET quantity = quantity + ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        else:
            update_query = "UPDATE items SET quantity = quantity - ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?"

        self.execute_update(update_query, (quantity, item_id))

        return result

    def get_inventory_transactions(self, filters: Dict = None) -> List[Dict]:
        """获取库存变动记录"""
        if filters is None:
            filters = {}

        query = '''
            SELECT it.*, i.name as item_name, ic.name as category_name
            FROM inventory_transactions it
            LEFT JOIN items i ON it.item_id = i.id
            LEFT JOIN item_categories ic ON i.category_id = ic.id
            WHERE 1=1
        '''
        params = []

        if 'item_id' in filters and filters['item_id']:
            query += " AND it.item_id = ?"
            params.append(filters['item_id'])

        if 'type' in filters and filters['type']:
            query += " AND it.type = ?"
            params.append(filters['type'])

        if 'start_date' in filters and filters['start_date']:
            query += " AND it.date >= ?"
            params.append(filters['start_date'])

        if 'end_date' in filters and filters['end_date']:
            query += " AND it.date <= ?"
            params.append(filters['end_date'])

        query += " ORDER BY it.date DESC, it.created_at DESC"

        if 'limit' in filters:
            query += " LIMIT ?"
            params.append(filters['limit'])

        rows = self.execute_query(query, tuple(params))
        return [dict(row) for row in rows]

    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()

    def __del__(self):
        """析构函数，确保数据库连接被关闭"""
        self.close()