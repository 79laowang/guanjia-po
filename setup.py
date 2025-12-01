#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
官家婆应用程序打包配置
"""

from setuptools import setup, find_packages
import sys
from pathlib import Path

# 项目信息
PROJECT_NAME = "GuanjiaPo"
APP_NAME = "官家婆"
VERSION = "1.0.0"
DESCRIPTION = "个人家庭账目库存管理软件"
AUTHOR = "GuanjiaPo Software"
AUTHOR_EMAIL = "support@guanjiapo.com"

# 项目根目录
HERE = Path(__file__).parent.absolute()

# 读取README文件
def read_file(filename):
    filepath = HERE / filename
    if filepath.exists():
        with open(filepath, encoding='utf-8') as f:
            return f.read()
    return ""

# 读取依赖
def get_requirements():
    requirements_file = HERE / 'requirements.txt'
    if requirements_file.exists():
        with open(requirements_file, encoding='utf-8') as f:
            requirements = []
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    requirements.append(line)
            return requirements
    return []

# 基本配置
setup(
    name=PROJECT_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url="https://github.com/guanjiapo/guanjiapo",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    package_data={
        '': ['resources/**/*', '*.qss', '*.png', '*.jpg', '*.ico'],
    },
    python_requires='>=3.8',
    install_requires=get_requirements(),
    entry_points={
        'console_scripts': [
            'guanjia-po=main:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Office/Business :: Financial',
        'Topic :: Home/Automation',
    ],
    keywords='家庭 账目 库存 管理 财务',
)