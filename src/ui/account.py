from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class AccountWidget(QWidget):
    """账目管理页面"""
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setup_ui()

    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # 标题
        title_label = QLabel("账目管理")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #262626;
                margin-bottom: 20px;
            }
        """)
        layout.addWidget(title_label)

        # 功能说明
        desc_label = QLabel("这里将显示账目管理功能，包括：")
        desc_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #595959;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(desc_label)

        features = [
            "• 收入支出记录",
            "• 分类管理",
            "• 账目搜索和筛选",
            "• 统计汇总",
            "• 数据导出"
        ]

        for feature in features:
            feature_label = QLabel(feature)
            feature_label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #8c8c8c;
                    margin: 5px 0;
                }
            """)
            layout.addWidget(feature_label)

        # 添加按钮
        button = QPushButton("功能开发中...")
        button.setStyleSheet("""
            QPushButton {
                background-color: #1890ff;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: 500;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #40a9ff;
            }
        """)
        layout.addWidget(button)

        layout.addStretch()