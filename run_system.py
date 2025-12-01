#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
官家婆应用程序启动脚本 (系统Python版本)
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from src.ui.main_window import main
    exit_code = main()
    sys.exit(exit_code)
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保已安装所有依赖包:")
    print("pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"运行时错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)