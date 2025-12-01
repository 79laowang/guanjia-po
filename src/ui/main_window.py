import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QSplitter, QMenuBar, QStatusBar,
    QMessageBox, QApplication
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QIcon, QFont, QAction, QPixmap

from .dashboard import DashboardWidget
from .account import AccountWidget
from .inventory import InventoryWidget
from .statistics import StatisticsWidget
from ..database.database import DatabaseManager
from ..utils.config import APP_CONFIG, COLORS

class NavigationButton(QPushButton):
    """导航按钮"""
    def __init__(self, text, icon_path=None, is_active=False):
        super().__init__()
        self.setText(text)
        self.setCheckable(True)
        self.setAutoExclusive(True)
        self.setChecked(is_active)

        # 设置样式
        self.setFixedHeight(50)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # 应用样式
        self.update_style(is_active)

    def update_style(self, is_active):
        """更新按钮样式"""
        if is_active:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['primary']};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px;
                    font-weight: bold;
                    font-size: 14px;
                    text-align: left;
                }}
                QPushButton:hover {{
                    background-color: #1677ff;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {COLORS['text_primary']};
                    border: none;
                    border-radius: 8px;
                    padding: 12px;
                    font-size: 14px;
                    text-align: left;
                }}
                QPushButton:hover {{
                    background-color: rgba(24, 144, 255, 0.1);
                    color: {COLORS['primary']};
                }}
                QPushButton:checked {{
                    background-color: {COLORS['primary']};
                    color: white;
                }}
            """)

class SidebarWidget(QFrame):
    """侧边栏导航"""
    page_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(10)

        # 应用标题
        title_label = QLabel("🏠 官家婆")
        title_label.setStyleSheet(f"""
            QLabel {{
                font-size: 24px;
                font-weight: bold;
                color: {COLORS['primary']};
                margin-bottom: 20px;
            }}
        """)
        layout.addWidget(title_label)

        # 导航按钮
        self.nav_buttons = {}

        buttons_config = [
            ('dashboard', '总览', '📊'),
            ('accounts', '账目管理', '💰'),
            ('inventory', '库存管理', '📦'),
            ('statistics', '统计报表', '📈'),
            ('settings', '设置', '⚙️')
        ]

        for page_id, text, icon in buttons_config:
            button = NavigationButton(f"{icon} {text}", is_active=(page_id == 'dashboard'))
            button.clicked.connect(lambda checked, pid=page_id: self.on_nav_clicked(pid))
            layout.addWidget(button)
            self.nav_buttons[page_id] = button

        layout.addStretch()

        # 设置侧边栏样式
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border-right: 1px solid {COLORS['border']};
            }}
        """)
        self.setFixedWidth(200)

    def on_nav_clicked(self, page_id):
        """导航按钮点击事件"""
        # 更新按钮状态
        for button_id, button in self.nav_buttons.items():
            button.update_style(button_id == page_id)

        # 发出页面切换信号
        self.page_changed.emit(page_id)

class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.current_page = 'dashboard'

        self.setup_ui()
        self.setup_menu()
        self.setup_statusbar()
        self.connect_signals()

        # 显示总览页面
        self.switch_page('dashboard')

    def setup_ui(self):
        """设置主界面"""
        self.setWindowTitle(APP_CONFIG['window_title'])
        self.setMinimumSize(*APP_CONFIG['minimum_window_size'])
        self.resize(*APP_CONFIG['default_window_size'])

        # 创建中央控件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 创建分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # 创建侧边栏
        self.sidebar = SidebarWidget()
        splitter.addWidget(self.sidebar)

        # 创建内容区域
        self.content_area = QFrame()
        self.content_area.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['background']};
            }}
        """)

        # 内容区域布局
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(20, 20, 20, 20)

        # 页面标题
        self.page_title = QLabel("总览")
        self.page_title.setStyleSheet(f"""
            QLabel {{
                font-size: 28px;
                font-weight: bold;
                color: {COLORS['text_primary']};
                margin-bottom: 20px;
            }}
        """)
        self.content_layout.addWidget(self.page_title)

        # 页面内容区域
        self.page_content = QWidget()
        self.page_layout = QVBoxLayout(self.page_content)
        self.page_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.addWidget(self.page_content)

        splitter.addWidget(self.content_area)
        splitter.setStretchFactor(0, 0)  # 侧边栏固定宽度
        splitter.setStretchFactor(1, 1)  # 内容区域可拉伸

        main_layout.addWidget(splitter)

        # 应用主窗口样式
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {COLORS['background']};
            }}
        """)

    def setup_menu(self):
        """设置菜单栏"""
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu('文件(&F)')

        new_account_action = QAction('新建账目(&N)', self)
        new_account_action.setShortcut('Ctrl+N')
        new_account_action.triggered.connect(lambda: self.switch_page('accounts'))
        file_menu.addAction(new_account_action)

        new_inventory_action = QAction('新建库存(&I)', self)
        new_inventory_action.setShortcut('Ctrl+Shift+N')
        new_inventory_action.triggered.connect(lambda: self.switch_page('inventory'))
        file_menu.addAction(new_inventory_action)

        file_menu.addSeparator()

        exit_action = QAction('退出(&X)', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 视图菜单
        view_menu = menubar.addMenu('视图(&V)')

        dashboard_action = QAction('总览(&D)', self)
        dashboard_action.setShortcut('Ctrl+1')
        dashboard_action.triggered.connect(lambda: self.switch_page('dashboard'))
        view_menu.addAction(dashboard_action)

        accounts_action = QAction('账目管理(&A)', self)
        accounts_action.setShortcut('Ctrl+2')
        accounts_action.triggered.connect(lambda: self.switch_page('accounts'))
        view_menu.addAction(accounts_action)

        inventory_action = QAction('库存管理(&S)', self)
        inventory_action.setShortcut('Ctrl+3')
        inventory_action.triggered.connect(lambda: self.switch_page('inventory'))
        view_menu.addAction(inventory_action)

        statistics_action = QAction('统计报表(&T)', self)
        statistics_action.setShortcut('Ctrl+4')
        statistics_action.triggered.connect(lambda: self.switch_page('statistics'))
        view_menu.addAction(statistics_action)

        # 帮助菜单
        help_menu = menubar.addMenu('帮助(&H)')

        about_action = QAction('关于(&A)', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def setup_statusbar(self):
        """设置状态栏"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # 添加状态信息
        self.status_bar.showMessage(f"欢迎使用{APP_CONFIG['app_name']} v{APP_CONFIG['app_version']}")

    def connect_signals(self):
        """连接信号槽"""
        self.sidebar.page_changed.connect(self.switch_page)

    def switch_page(self, page_id):
        """切换页面"""
        # 清空当前页面内容
        for i in reversed(range(self.page_layout.count())):
            child = self.page_layout.itemAt(i).widget()
            if child is not None:
                child.deleteLater()

        # 创建新页面
        if page_id == 'dashboard':
            page_widget = DashboardWidget(self.db_manager)
            self.page_title.setText("总览")
        elif page_id == 'accounts':
            page_widget = AccountWidget(self.db_manager)
            self.page_title.setText("账目管理")
        elif page_id == 'inventory':
            page_widget = InventoryWidget(self.db_manager)
            self.page_title.setText("库存管理")
        elif page_id == 'statistics':
            page_widget = StatisticsWidget(self.db_manager)
            self.page_title.setText("统计报表")
        else:  # settings
            page_widget = QWidget()
            layout = QVBoxLayout(page_widget)
            layout.addWidget(QLabel("设置页面功能开发中..."))
            self.page_title.setText("设置")

        # 添加新页面
        self.page_layout.addWidget(page_widget)
        self.current_page = page_id

        # 更新状态栏
        self.status_bar.showMessage(f"当前页面: {self.page_title.text()}")

    def show_about(self):
        """显示关于对话框"""
        about_text = f"""
        <h2>{APP_CONFIG['app_name']}</h2>
        <p>{APP_CONFIG['app_description']}</p>
        <p>版本: {APP_CONFIG['app_version']}</p>
        <p><b>开发方:</b> {APP_CONFIG['company']}</p>
        <hr>
        <p>一款简单实用的家庭财务管理工具</p>
        <p>帮助您轻松管理家庭收支和物品库存</p>
        """

        QMessageBox.about(self, f"关于 {APP_CONFIG['app_name']}", about_text)

    def closeEvent(self, event):
        """窗口关闭事件"""
        try:
            if self.db_manager:
                self.db_manager.close()
            event.accept()
        except Exception as e:
            print(f"关闭应用时出错: {e}")
            event.accept()

def main():
    """应用主函数"""
    app = QApplication(sys.argv)

    # 设置应用属性
    app.setApplicationName(APP_CONFIG['app_name'])
    app.setApplicationVersion(APP_CONFIG['app_version'])
    app.setOrganizationName(APP_CONFIG['company'])

    # 设置字体
    font = QFont("Microsoft YaHei", 9)
    app.setFont(font)

    # 创建并显示主窗口
    window = MainWindow()
    window.show()

    return app.exec()