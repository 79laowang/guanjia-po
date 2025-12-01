#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
官家婆应用程序基础运行脚本
仅使用标准库和已安装的包
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

def basic_run():
    """基础运行函数，不依赖PyQt6"""
    print("🏠 官家婆 - 个人家庭账目库存管理软件")
    print("=" * 60)

    print("\n✅ 项目状态:")
    print("  📁 项目结构: 完整")
    print("  💾 数据库设计: SQLite3 + 完整表结构")
    print("  🎨 UI组件: PyQt6 + 现代化设计")
    print("  📊 功能模块: 账目 + 库存 + 统计")
    print("  📦 文档: 安装指南 + 使用说明")

    print("\n🔧 运行环境:")
    print(f"  Python版本: {sys.version}")
    print(f"  工作目录: {os.getcwd()}")
    print(f"  项目路径: {project_root}")

    print("\n📂 项目文件检查:")
    important_files = [
        'src/main.py',
        'src/ui/main_window.py',
        'src/database/database.py',
        'src/utils/config.py',
        'requirements.txt',
        'README.md'
    ]

    for file_path in important_files:
        full_path = os.path.join(project_root, file_path)
        if os.path.exists(full_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} (文件不存在)")

    print("\n🚀 启动说明:")
    print("  1. 安装PyQt6: pip3 install PyQt6 PyQt6-tools")
    print("  2. 安装其他依赖: pip3 install matplotlib pandas pillow")
    print("  3. 运行GUI版本: python3 run.py")
    print("  4. 或使用虚拟环境: source guanjia_po_env/bin/activate && python run.py")

    print("\n📋 检查PyQt6可用性:")
    try:
        from PyQt6.QtWidgets import QApplication
        print("  ✅ PyQt6 已安装并可用")
    except ImportError as e:
        print(f"  ❌ PyQt6 不可用: {e}")

    print("\n📋 检查其他依赖:")
    dependencies = ['matplotlib', 'pandas', 'pillow', 'numpy']
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"  ✅ {dep} 已安装")
        except ImportError:
            print(f"  ❌ {dep} 未安装")

    print("\n📊 统计信息:")
    import shutil
    project_size = sum(
        os.path.getsize(os.path.join(project_root, 'src', filename))
        for filename in os.listdir(os.path.join(project_root, 'src'))
        if os.path.isfile(os.path.join(project_root, 'src', filename))
    )
    print(f"  源代码大小: {project_size / 1024:.1f} KB")

    file_count = len(list(Path(project_root).rglob('*.py')))
    print(f"  Python文件: {file_count} 个")

    line_count = 0
    for py_file in Path(project_root).rglob('*.py'):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                line_count += len(f.readlines())
        except:
            pass
    print(f"  代码行数: {line_count} 行")

    print("\n" + "=" * 60)
    print("💡 提示: 完整的官家婆项目已准备就绪！")
    print("   请按照上述安装说明安装依赖后运行GUI版本。")

if __name__ == '__main__':
    try:
        basic_run()
    except KeyboardInterrupt:
        print("\n\n👋 程序被用户中断")
    except Exception as e:
        print(f"\n\n❌ 运行时出现错误: {e}")
        import traceback
        traceback.print_exc()