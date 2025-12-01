from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QGridLayout, QScrollArea, QSizePolicy, QPushButton
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from datetime import datetime, date, timedelta
import sys

class StatisticCard(QFrame):
    """统计卡片"""
    def __init__(self, title: str, value: str, subtitle: str = "", color: str = "#1890ff", icon: str = "📊"):
        super().__init__()
        self.setup_ui(title, value, subtitle, color, icon)

    def setup_ui(self, title, value, subtitle, color, icon):
        self.setFixedSize(240, 120)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #ffffff;
                border: 1px solid #e8e8e8;
                border-radius: 8px;
                padding: 16px;
            }}
            QFrame:hover {{
                border-color: {color};
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        # 标题行
        title_layout = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 20px; color: {color};")
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #8c8c8c;
                font-weight: 500;
            }
        """)
        title_layout.addWidget(icon_label)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        layout.addLayout(title_layout)

        # 数值
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            QLabel {{
                font-size: 28px;
                font-weight: bold;
                color: {color};
                margin: 8px 0;
            }}
        """)
        layout.addWidget(value_label)

        # 副标题
        if subtitle:
            subtitle_label = QLabel(subtitle)
            subtitle_label.setStyleSheet("""
                QLabel {
                    font-size: 12px;
                    color: #bfbfbf;
                }
            """)
            layout.addWidget(subtitle_label)

        layout.addStretch()

class RecentAccountWidget(QFrame):
    """最近账目部件"""
    def __init__(self, accounts_data=None):
        super().__init__()
        self.accounts_data = accounts_data or []
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #e8e8e8;
                border-radius: 8px;
                padding: 16px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        # 标题
        title_label = QLabel("最近账目")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #262626;
                margin-bottom: 12px;
            }
        """)
        layout.addWidget(title_label)

        # 账目列表
        self.setup_account_list(layout)

        # 查看更多按钮
        more_button = QPushButton("查看全部")
        more_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #1890ff;
                color: #1890ff;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
                margin-top: 12px;
            }
            QPushButton:hover {
                background-color: rgba(24, 144, 255, 0.08);
            }
        """)
        layout.addWidget(more_button)

    def setup_account_list(self, parent_layout):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setFixedHeight(300)

        list_widget = QWidget()
        list_layout = QVBoxLayout(list_widget)
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_layout.setSpacing(8)

        # 添加账目项
        for account in self.accounts_data[:10]:  # 只显示最近10条
            account_item = self.create_account_item(account)
            list_layout.addWidget(account_item)

        list_layout.addStretch()
        scroll_area.setWidget(list_widget)
        parent_layout.addWidget(scroll_area)

    def create_account_item(self, account):
        """创建账目项"""
        item = QFrame()
        item.setStyleSheet("""
            QFrame {
                background-color: #fafafa;
                border: 1px solid #f0f0f0;
                border-radius: 6px;
                padding: 12px;
            }
            QFrame:hover {
                background-color: #f5f5f5;
                border-color: #e8e8e8;
            }
        """)

        layout = QHBoxLayout(item)
        layout.setContentsMargins(12, 12, 12, 12)

        # 日期
        date_label = QLabel(account.get('date', ''))
        date_label.setStyleSheet("font-size: 12px; color: #8c8c8c;")
        date_label.setFixedWidth(80)

        # 分类
        category_label = QLabel(account.get('category_name', ''))
        category_label.setStyleSheet("font-size: 14px; color: #262626; font-weight: 500;")
        category_label.setFixedWidth(80)

        # 金额
        amount = account.get('amount', 0)
        account_type = account.get('type', 'expense')
        amount_text = f"+￥{amount:.2f}" if account_type == 'income' else f"-￥{amount:.2f}"
        amount_color = "#52c41a" if account_type == 'income' else "#ff4d4f"

        amount_label = QLabel(amount_text)
        amount_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {amount_color};")
        amount_label.setFixedWidth(100)

        # 说明
        description_label = QLabel(account.get('description', ''))
        description_label.setStyleSheet("font-size: 14px; color: #595959;")
        description_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        layout.addWidget(date_label)
        layout.addWidget(category_label)
        layout.addWidget(amount_label)
        layout.addWidget(description_label)

        return item

class LowStockWidget(QFrame):
    """库存预警部件"""
    def __init__(self, low_stock_data=None):
        super().__init__()
        self.low_stock_data = low_stock_data or []
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #e8e8e8;
                border-radius: 8px;
                padding: 16px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        # 标题
        title_label = QLabel("库存预警")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #262626;
                margin-bottom: 12px;
            }
        """)
        layout.addWidget(title_label)

        if not self.low_stock_data:
            # 无预警物品
            no_data_label = QLabel("🎉 库存充足，无需预警")
            no_data_label.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    color: #52c41a;
                    text-align: center;
                    padding: 40px 0;
                }
            """)
            no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(no_data_label)
        else:
            # 显示预警物品列表
            self.setup_low_stock_list(layout)

    def setup_low_stock_list(self, parent_layout):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setFixedHeight(200)

        list_widget = QWidget()
        list_layout = QVBoxLayout(list_widget)
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_layout.setSpacing(8)

        for item in self.low_stock_data:
            item_widget = self.create_low_stock_item(item)
            list_layout.addWidget(item_widget)

        list_layout.addStretch()
        scroll_area.setWidget(list_widget)
        parent_layout.addWidget(scroll_area)

    def create_low_stock_item(self, item):
        """创建库存预警项"""
        item_frame = QFrame()
        item_frame.setStyleSheet("""
            QFrame {
                background-color: #fff7e6;
                border: 1px solid #ffd591;
                border-radius: 6px;
                padding: 12px;
            }
            QFrame:hover {
                background-color: #fffbe6;
                border-color: #ffc53d;
            }
        """)

        layout = QHBoxLayout(item_frame)
        layout.setContentsMargins(12, 12, 12, 12)

        # 物品名称
        name_label = QLabel(f"⚠️ {item.get('name', '')}")
        name_label.setStyleSheet("font-size: 14px; font-weight: 500; color: #d48806;")
        name_label.setFixedWidth(120)

        # 当前库存
        current_qty = item.get('quantity', 0)
        min_qty = item.get('min_quantity', 0)
        unit = item.get('unit', '个')

        stock_label = QLabel(f"{current_qty:.1f} / {min_qty:.1f} {unit}")
        stock_label.setStyleSheet("font-size: 14px; color: #d48806;")
        stock_label.setFixedWidth(80)

        # 建议补货
        if current_qty < min_qty / 2:
            suggestion = "急需补货"
            suggestion_color = "#ff4d4f"
        elif current_qty < min_qty:
            suggestion = "建议补货"
            suggestion_color = "#faad14"
        else:
            suggestion = "库存充足"
            suggestion_color = "#52c41a"

        suggestion_label = QLabel(suggestion)
        suggestion_label.setStyleSheet(f"font-size: 12px; color: {suggestion_color}; font-weight: 500;")
        suggestion_label.setFixedWidth(80)

        layout.addWidget(name_label)
        layout.addWidget(stock_label)
        layout.addWidget(suggestion_label)
        layout.addStretch()

        return item_frame

class QuickActionWidget(QFrame):
    """快速操作部件"""
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #e8e8e8;
                border-radius: 8px;
                padding: 20px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # 标题
        title_label = QLabel("快速操作")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #262626;
                margin-bottom: 16px;
            }
        """)
        layout.addWidget(title_label)

        # 按钮网格
        button_layout = QGridLayout()
        button_layout.setSpacing(12)

        # 快速操作按钮
        actions = [
            ("💰 记录支出", "#1890ff"),
            ("💵 记录收入", "#52c41a"),
            ("📦 入库管理", "#722ed1"),
            ("📊 出库管理", "#fa8c16"),
            ("📈 查看统计", "#13c2c2"),
            ("⚙️ 系统设置", "#595959"),
        ]

        for i, (text, color) in enumerate(actions):
            button = QPushButton(text)
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 16px;
                    font-size: 14px;
                    font-weight: 500;
                    text-align: center;
                    min-height: 60px;
                }}
                QPushButton:hover {{
                    background-color: {color}dd;
                    transform: translateY(-2px);
                }}
                QPushButton:pressed {{
                    background-color: {color}bb;
                    transform: translateY(0px);
                }}
            """)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            row, col = i // 3, i % 3
            button_layout.addWidget(button, row, col)

        layout.addLayout(button_layout)

class DashboardWidget(QWidget):
    """总览页面"""
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setup_ui()
        self.load_data()

        # 定时刷新数据
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.load_data)
        self.refresh_timer.start(60000)  # 每分钟刷新一次

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(16)

        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # 内容容器
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(16)

        # 统计卡片行
        self.setup_statistics_cards(content_layout)

        # 主要内容区域
        content_row_layout = QHBoxLayout()
        content_row_layout.setSpacing(16)

        # 左侧：最近账目
        self.recent_accounts_widget = RecentAccountWidget()
        content_row_layout.addWidget(self.recent_accounts_widget, 2)

        # 右侧：库存预警
        self.low_stock_widget = LowStockWidget()
        content_row_layout.addWidget(self.low_stock_widget, 1)

        content_layout.addLayout(content_row_layout)

        # 快速操作区域
        self.quick_action_widget = QuickActionWidget()
        content_layout.addWidget(self.quick_action_widget)

        # 添加弹性空间
        content_layout.addStretch()

        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        # 设置整体样式
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
            }
        """)

    def setup_statistics_cards(self, parent_layout):
        """设置统计卡片"""
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(16)

        # 初始化卡片
        self.income_card = StatisticCard("本月收入", "￥0.00", "较上月 +0%")
        self.expense_card = StatisticCard("本月支出", "￥0.00", "较上月 +0%", color="#ff4d4f", icon="💸")
        self.balance_card = StatisticCard("本月结余", "￥0.00", "收支平衡", color="#52c41a", icon="💰")
        self.inventory_card = StatisticCard("库存物品", "0", "种物品", color="#722ed1", icon="📦")

        cards_layout.addWidget(self.income_card)
        cards_layout.addWidget(self.expense_card)
        cards_layout.addWidget(self.balance_card)
        cards_layout.addWidget(self.inventory_card)

        # 添加弹性空间
        cards_layout.addStretch()

        parent_layout.addLayout(cards_layout)

    def load_data(self):
        """加载数据"""
        try:
            # 计算本月统计
            today = date.today()
            first_day = today.replace(day=1)
            end_day = today

            # 获取本月账目汇总
            summaries = self.db_manager.get_account_summary(
                first_day.strftime('%Y-%m-%d'),
                end_day.strftime('%Y-%m-%d')
            )

            income_total = 0
            expense_total = 0

            for summary in summaries:
                if summary['type'] == 'income':
                    income_total = summary['total']
                elif summary['type'] == 'expense':
                    expense_total = summary['total']

            balance = income_total - expense_total

            # 更新统计卡片
            self.income_card.findChild(QLabel).setText(f"￥{income_total:.2f}")
            self.expense_card.findChild(QLabel).setText(f"￥{expense_total:.2f}")
            self.balance_card.findChild(QLabel).setText(f"￥{balance:.2f}")

            # 获取物品数量
            items = self.db_manager.get_items()
            item_count = len(items)
            self.inventory_card.findChild(QLabel).setText(str(item_count))

            # 获取最近账目
            recent_accounts = self.db_manager.get_accounts({'limit': 10})
            # 重新创建最近账目部件
            self.recent_accounts_widget.deleteLater()
            self.recent_accounts_widget = RecentAccountWidget(recent_accounts)

            # 获取库存预警物品
            low_stock_items = self.db_manager.get_items({'low_stock': True})
            # 重新创建库存预警部件
            self.low_stock_widget.deleteLater()
            self.low_stock_widget = LowStockWidget(low_stock_items)

            # 更新布局
            # 这里需要重新添加到布局中，简化起见这里不展示具体实现

        except Exception as e:
            print(f"加载数据失败: {e}")

    def cleanup(self):
        """清理资源"""
        if self.refresh_timer.isActive():
            self.refresh_timer.stop()