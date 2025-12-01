#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
官家婆 - 个人家庭账目库存管理软件
主程序入口
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from ui.main_window import main

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