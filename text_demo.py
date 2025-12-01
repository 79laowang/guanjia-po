#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
官家婆应用程序文本演示版本
"""

import sys
import os
import sqlite3
from datetime import datetime, date

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

class DatabaseDemo:
    """演示数据库功能"""
    def __init__(self, db_path=":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # 使结果可以通过列名访问
        self.cursor = self.conn.cursor()
        self.init_database()

    def init_database(self):
        """初始化演示数据库"""
        # 创建分类表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                type TEXT NOT NULL CHECK (type IN ('income', 'expense')),
                color TEXT DEFAULT '#1890ff',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 创建账目表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL CHECK (type IN ('income', 'expense')),
                amount REAL NOT NULL CHECK (amount > 0),
                category_id INTEGER NOT NULL,
                description TEXT,
                date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 创建物品表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity REAL DEFAULT 0,
                unit TEXT DEFAULT '个',
                min_quantity REAL DEFAULT 0,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.conn.commit()

    def insert_sample_data(self):
        """插入示例数据"""
        # 清空数据
        self.cursor.execute('DELETE FROM categories')
        self.cursor.execute('DELETE FROM accounts')
        self.cursor.execute('DELETE FROM items')

        # 插入分类
        categories = [
            ('工资', 'income', '#52c41a'),
            ('奖金', 'income', '#52c41a'),
            ('餐饮', 'expense', '#ff4d4f'),
            ('购物', 'expense', '#ff4d4f'),
            ('交通', 'expense', '#ff4d4f'),
            ('居住', 'expense', '#ff4d4f'),
            ('娱乐', 'expense', '#ff4d4f')
        ]

        self.cursor.executemany('''
            INSERT INTO categories (name, type, color) VALUES (?, ?, ?)
        ''', categories)

        # 插入账目
        accounts = [
            ('income', 8500.00, 1, '2024年1月工资', '2024-01-15'),
            ('expense', 85.50, 3, '午餐', '2024-01-15'),
            ('expense', 234.00, 4, '日用品采购', '2024-01-14'),
            ('expense', 50.00, 5, '地铁月卡充值', '2024-01-13'),
            ('expense', 120.00, 6, '房租', '2024-01-01'),
            ('expense', 80.00, 7, '电影票', '2024-01-20'),
            ('income', 2000.00, 2, '项目奖金', '2024-01-25')
        ]

        self.cursor.executemany('''
            INSERT INTO accounts (type, amount, category_id, description, date) VALUES (?, ?, ?, ?, ?)
        ''', accounts)

        # 插入物品
        items = [
            ('牛奶', 8, '盒', 10, '每日早餐'),
            ('洗衣液', 1, '瓶', 2, '清洁用品'),
            ('大米', 25, 'kg', 15, '主食'),
            ('纸巾', 3, '包', 5, '日常用品'),
            ('充电器', 2, '个', 1, '电子配件')
        ]

        self.cursor.executemany('''
            INSERT INTO items (name, quantity, unit, min_quantity, description) VALUES (?, ?, ?, ?, ?)
        ''', items)

        self.conn.commit()

    def get_summary(self):
        """获取汇总信息"""
        # 收支汇总
        self.cursor.execute('''
            SELECT type, SUM(amount) as total, COUNT(*) as count
            FROM accounts
            GROUP BY type
        ''')

        summary = {}
        for row in self.cursor.fetchall():
            summary[row['type']] = row

        # 物品汇总
        self.cursor.execute('SELECT COUNT(*) as count FROM items')
        item_count = self.cursor.fetchone()['count']

        # 库存预警
        self.cursor.execute('''
            SELECT name, quantity, min_quantity, unit
            FROM items
            WHERE quantity <= min_quantity AND min_quantity > 0
        ''')
        low_stock = self.cursor.fetchall()

        return summary, item_count, low_stock

    def get_recent_accounts(self, limit=5):
        """获取最近账目"""
        self.cursor.execute('''
            SELECT a.type, a.amount, c.name as category, a.description, a.date
            FROM accounts a
            LEFT JOIN categories c ON a.category_id = c.id
            ORDER BY a.date DESC, a.created_at DESC
            LIMIT ?
        ''', (limit,))

        return self.cursor.fetchall()

    def close(self):
        """关闭数据库连接"""
        self.conn.close()

def display_ui():
    """显示UI界面"""
    print("\n" + "="*80)
    print("🏠 官家婆 - 个人家庭账目库存管理软件")
    print("="*80)

    # 初始化数据库
    db = DatabaseDemo()
    db.insert_sample_data()

    # 获取数据
    summary, item_count, low_stock = db.get_summary()
    recent_accounts = db.get_recent_accounts()

    # 显示统计信息
    print("\n📊 总览")
    print("-"*60)

    income_summary = summary.get('income')
    expense_summary = summary.get('expense')
    income_total = income_summary['total'] if income_summary else 0
    expense_total = expense_summary['total'] if expense_summary else 0
    balance = income_total - expense_total

    print(f"  本月收入:    ￥{income_total:,.2f}")
    print(f"  本月支出:    ￥{expense_total:,.2f}")
    print(f"  本月结余:    ￥{balance:,.2f}")
    print(f"  库存物品:    {item_count} 种")

    # 显示最近账目
    print(f"\n💰 最近账目")
    print("-"*60)

    for i, account in enumerate(recent_accounts, 1):
        type_emoji = "💵" if account['type'] == 'income' else "💸"
        print(f"  {i:2d}. {type_emoji} {account['date']} {account['category']:<6} ￥{account['amount']:>8.2f} {account['description']}")

    # 显示库存预警
    print(f"\n📦 库存预警")
    print("-"*60)

    if low_stock:
        for item in low_stock:
            warning = "⚠️" if item['quantity'] <= item['min_quantity']/2 else "🔶"
            print(f"  {warning} {item['name']:<8} {item['quantity']:.1f}/{item['min_quantity']:.1f} {item['unit']}")
    else:
        print("  🎉 库存充足，无需预警")

    # 显示菜单
    print(f"\n📋 功能菜单")
    print("-"*60)

    menu_items = [
        "1. 💰 记录收入",
        "2. 💸 记录支出",
        "3. 📦 物品入库",
        "4. 📤 物品出库",
        "5. 📊 查看统计",
        "6. ⚙️ 系统设置",
        "0. ❌ 退出程序"
    ]

    for item in menu_items:
        print(f"  {item}")

    print("\n" + "="*80)
    print("💡 这是官家婆项目的演示版本")
    print("🔧 完整版本需要图形界面环境运行")
    print("📝 包含完整的数据库设计和功能模块")
    print("🎊 PyQt6 + SQLite3 技术栈")
    print("="*80)

    db.close()

def show_features():
    """显示功能特性"""
    print("\n✨ 核心功能特性:")
    features = [
        "💰 账目管理 - 完整的收支记录和分类管理",
        "📦 库存管理 - 物品入库出库和库存预警系统",
        "📊 统计报表 - 可视化图表和数据分析",
        "🎨 现代化UI - 基于PyQt6的桌面应用程序界面",
        "💾 本地存储 - SQLite3数据库，数据安全可靠",
        "🔧 模块化设计 - 清晰的项目结构和组件化开发"
    ]

    for feature in features:
        print(f"  {feature}")

def show_tech_stack():
    """显示技术栈"""
    print("\n🔧 技术栈:")
    tech_stack = [
        ("GUI框架", "PyQt6"),
        ("数据库", "SQLite3"),
        ("开发语言", "Python 3.8+"),
        ("数据可视化", "Matplotlib"),
        ("打包工具", "PyInstaller"),
        ("项目架构", "MVC模式")
    ]

    for tech, tool in tech_stack:
        print(f"  {tech:<12}: {tool}")

def main():
    """主函数"""
    print("🚀 启动官家婆应用程序...")

    try:
        display_ui()
        show_features()
        show_tech_stack()

        print(f"\n🎉 官家婆项目运行成功！")
        print(f"📅 运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        return 0

    except KeyboardInterrupt:
        print(f"\n\n👋 程序被用户中断")
        return 0
    except Exception as e:
        print(f"\n❌ 程序运行时出现错误: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        print(f"\n📊 演示完成，感谢使用官家婆！")

if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n程序被用户中断")
        sys.exit(0)