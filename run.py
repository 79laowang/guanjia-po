#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
官家婆应用程序启动脚本
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

def main():
    """主函数"""
    try:
        from src.ui.main_window import main
        exit_code = main()
        return exit_code
    except ImportError as e:
        print(f"导入错误: {e}")
        print("请确保已安装所有依赖包:")
        print("pip install -r requirements.txt")
        return 1
    except Exception as e:
        print(f"运行时错误: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())