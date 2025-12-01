#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单的PyQt6测试应用
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🏠 官家婆 - 测试版本")
        self.setGeometry(100, 100, 800, 600)
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # 标题
        title = QLabel("🏠 官家婆 - 个人家庭账目库存管理软件")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #1890ff;
                margin-bottom: 20px;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # 说明
        desc = QLabel("✨ 欢迎使用官家婆！\n\n这是一个基于PyQt6的桌面应用程序框架。\n\n主要功能：")
        desc.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #262626;
                line-height: 1.6;
            }
        """)
        layout.addWidget(desc)

        # 功能列表
        features = [
            "💰 账目管理 - 收入支出记录、分类管理",
            "📦 库存管理 - 物品入库出库、库存预警",
            "📊 统计报表 - 可视化图表、趋势分析",
            "🎨 现代UI - PyQt6界面、响应式设计",
            "💾 本地存储 - SQLite数据库、数据安全"
        ]

        for feature in features:
            feature_label = QLabel(f"  • {feature}")
            feature_label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #595959;
                    margin: 5px 0;
                }
            """)
            layout.addWidget(feature_label)

        # 按钮区域
        button_layout = QHBoxLayout()

        test_db_btn = QPushButton("🗄️ 测试数据库")
        test_db_btn.setStyleSheet("""
            QPushButton {
                background-color: #1890ff;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #40a9ff;
            }
        """)
        test_db_btn.clicked.connect(self.test_database)
        button_layout.addWidget(test_db_btn)

        exit_btn = QPushButton("❌ 退出")
        exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff4d4f;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #ff7875;
            }
        """)
        exit_btn.clicked.connect(self.close)
        button_layout.addWidget(exit_btn)

        layout.addLayout(button_layout)
        layout.addStretch()

        # 设置整体样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
        """)

    def test_database(self):
        try:
            import sqlite3
            conn = sqlite3.connect(':memory:')
            conn.execute('CREATE TABLE test (id INTEGER PRIMARY KEY)')
            conn.close()
            QMessageBox.information(self, "数据库测试", "✅ SQLite数据库连接成功！")
        except Exception as e:
            QMessageBox.critical(self, "数据库错误", f"❌ 数据库连接失败：{e}")

def main():
    app = QApplication(sys.argv)

    # 设置应用属性
    app.setApplicationName("官家婆")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("GuanjiaPo Software")

    # 设置字体
    font = QFont("Microsoft YaHei", 9)
    app.setFont(font)

    window = TestWindow()
    window.show()

    return app.exec()

if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"程序运行时出现错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)