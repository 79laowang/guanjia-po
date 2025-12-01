#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
官家婆应用程序打包脚本
使用PyInstaller打包成可执行文件
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def clean_build():
    """清理之前的构建文件"""
    dirs_to_clean = ['build', 'dist', '__pycache__']

    for dir_name in dirs_to_clean:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"清理目录: {dir_path}")
            shutil.rmtree(dir_path)

    # 清理Python缓存文件
    for py_file in Path('.').rglob('*.py'):
        cache_file = py_file.with_suffix('.pyc')
        if cache_file.exists():
            cache_file.unlink()

        cache_dir = py_file.parent / '__pycache__'
        if cache_dir.exists():
            shutil.rmtree(cache_dir)

def install_requirements():
    """安装依赖包"""
    print("安装依赖包...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("依赖包安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"安装依赖包失败: {e}")
        return False

def build_executable():
    """构建可执行文件"""
    print("开始构建可执行文件...")

    # PyInstaller命令
    cmd = [
        'pyinstaller',
        '--name=官家婆',
        '--windowed',  # 无控制台窗口
        '--onefile',   # 打包成单个文件
        '--icon=resources/icons/app.ico',  # 应用图标
        '--add-data=resources;resources',  # 添加资源文件
        '--hidden-import=PyQt6.QtCore',
        '--hidden-import=PyQt6.QtGui',
        '--hidden-import=PyQt6.QtWidgets',
        '--hidden-import=matplotlib.backends.backend_qt5agg',
        '--hidden-import=PIL._tkinter_finder',
        '--exclude-module=matplotlib.backends.backend_tkagg',
        '--exclude-module=tkinter',
        '--distpath=dist',
        '--workpath=build',
        '--specpath=.',
        'src/main.py'
    ]

    try:
        subprocess.check_call(cmd)
        print("构建完成!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        return False
    except FileNotFoundError:
        print("PyInstaller未安装，正在安装...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
            print("PyInstaller安装完成，重新构建...")
            return build_executable()
        except subprocess.CalledProcessError:
            print("PyInstaller安装失败")
            return False

def create_installer():
    """创建安装包（可选）"""
    print("创建安装包...")

    # 这里可以使用NSIS或其他工具创建Windows安装包
    # 由于复杂度较高，这里只提供思路

    installer_dir = Path('installer')
    installer_dir.mkdir(exist_ok=True)

    # 复制可执行文件到安装包目录
    exe_file = Path('dist/官家婆.exe')
    if exe_file.exists():
        shutil.copy2(exe_file, installer_dir / '官家婆.exe')
        print(f"安装包文件已复制到: {installer_dir}")
        return True
    else:
        print("找不到可执行文件")
        return False

def main():
    """主函数"""
    print("=== 官家婆应用程序打包工具 ===")

    # 检查当前目录
    if not Path('src/main.py').exists():
        print("错误: 请在项目根目录运行此脚本")
        return 1

    # 清理构建文件
    if input("是否清理之前的构建文件? (y/n): ").lower() == 'y':
        clean_build()

    # 安装依赖
    if not install_requirements():
        return 1

    # 构建可执行文件
    if not build_executable():
        return 1

    # 创建安装包
    if input("是否创建安装包? (y/n): ").lower() == 'y':
        create_installer()

    print("\n=== 打包完成 ===")
    print("可执行文件位置: dist/官家婆.exe")

    # 显示文件大小
    exe_file = Path('dist/官家婆.exe')
    if exe_file.exists():
        size_mb = exe_file.stat().st_size / (1024 * 1024)
        print(f"文件大小: {size_mb:.1f} MB")

    return 0

if __name__ == '__main__':
    sys.exit(main())