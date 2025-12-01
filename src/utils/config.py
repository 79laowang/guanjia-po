import os
import sys
from pathlib import Path

# 获取应用数据目录
if getattr(sys, 'frozen', False):
    # 打包后的应用
    APPLICATION_DIR = sys._MEIPASS
    USER_DATA_DIR = Path.home() / '.guanjia-po'
else:
    # 开发环境
    APPLICATION_DIR = Path(__file__).parent.parent.parent
    USER_DATA_DIR = APPLICATION_DIR / 'data'

# 确保数据目录存在
USER_DATA_DIR.mkdir(exist_ok=True)

# 数据库文件路径
DATABASE_PATH = USER_DATA_DIR / 'guanjia_po.db'

# 应用配置
APP_CONFIG = {
    'app_name': '官家婆',
    'app_version': '1.0.0',
    'app_description': '个人家庭账目库存管理软件',
    'company': 'GuanjiaPo Software',
    'window_title': '官家婆 - 家庭账目库存管理',
    'default_window_size': (1200, 800),
    'minimum_window_size': (800, 600),
}

# 数据库配置
DB_CONFIG = {
    'database_path': str(DATABASE_PATH),
    'backup_count': 10,
}

# UI配置
UI_CONFIG = {
    'theme': 'default',
    'font_family': 'Microsoft YaHei',
    'font_size': 9,
    'date_format': 'yyyy-MM-dd',
    'time_format': 'hh:mm:ss',
    'datetime_format': 'yyyy-MM-dd hh:mm:ss',
    'currency_symbol': '￥',
}

# 颜色配置
COLORS = {
    'primary': '#1890ff',
    'success': '#52c41a',
    'warning': '#faad14',
    'error': '#ff4d4f',
    'info': '#1890ff',
    'text_primary': '#262626',
    'text_secondary': '#8c8c8c',
    'text_disabled': '#bfbfbf',
    'background': '#f5f5f5',
    'surface': '#ffffff',
    'border': '#d9d9d9',
    'income': '#52c41a',
    'expense': '#ff4d4f',
}

# 图标配置
ICONS = {
    'app_icon': 'resources/icons/app.png',
    'dashboard': 'resources/icons/dashboard.png',
    'account': 'resources/icons/account.png',
    'inventory': 'resources/icons/inventory.png',
    'statistics': 'resources/icons/statistics.png',
    'settings': 'resources/icons/settings.png',
}

# 分类配置
DEFAULT_CATEGORIES = {
    'income': [
        {'name': '工资', 'color': '#52c41a'},
        {'name': '奖金', 'color': '#52c41a'},
        {'name': '投资收益', 'color': '#52c41a'},
        {'name': '其他收入', 'color': '#52c41a'},
    ],
    'expense': [
        {'name': '餐饮', 'color': '#ff4d4f'},
        {'name': '购物', 'color': '#ff4d4f'},
        {'name': '交通', 'color': '#ff4d4f'},
        {'name': '居住', 'color': '#ff4d4f'},
        {'name': '医疗', 'color': '#ff4d4f'},
        {'name': '教育', 'color': '#ff4d4f'},
        {'name': '娱乐', 'color': '#ff4d4f'},
        {'name': '其他支出', 'color': '#ff4d4f'},
    ],
}

# 库存物品分类配置
DEFAULT_INVENTORY_CATEGORIES = [
    {'name': '食品饮料', 'description': '各类食品和饮料'},
    {'name': '日用品', 'description': '日常生活用品'},
    {'name': '服装鞋帽', 'description': '服装、鞋子、帽子等'},
    {'name': '电子产品', 'description': '电子设备和配件'},
    {'name': '家居用品', 'description': '家具和家居装饰'},
    {'name': '学习用品', 'description': '书籍、文具等'},
    {'name': '其他', 'description': '其他物品'},
]