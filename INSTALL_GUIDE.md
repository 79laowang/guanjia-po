# 官家婆应用程序安装指南

## 问题诊断
当前错误: `No module named 'PyQt6'`

## 安装步骤

### 方法1: 使用系统包管理器（推荐）

```bash
# 安装PyQt6和相关包
sudo dnf install python3-pyqt6 python3-pyqt6-sip python3-pyqt6-qtquick python3-pyqt6-tools
sudo dnf install python3-matplotlib python3-pandas python3-pillow python3-numpy
sudo dnf install python3-requests python3-dateutil python3-six
```

### 方法2: 使用pip（如果方法1失败）

```bash
# 安装开发工具
sudo dnf groupinstall "Development Tools" -y
sudo dnf install python3-devel python3-pip python3-setuptools python3-wheel -y

# 升级pip
python3 -m pip install --upgrade pip

# 安装PyQt6
python3 -m pip install PyQt6 PyQt6-tools

# 安装其他依赖
python3 -m pip install matplotlib pandas pillow numpy better-sqlite3
```

### 方法3: 使用虚拟环境

```bash
# 创建虚拟环境
cd guanjia-po
python3 -m venv guanjia_po_env

# 激活虚拟环境
source guanjia_po_env/bin/activate

# 升级pip
pip install --upgrade pip

# 安装依赖
pip install PyQt6 PyQt6-tools matplotlib pandas pillow numpy better-sqlite3

# 运行程序
python run.py
```

### 方法4: 如果上述都失败，尝试conda（如果有安装）

```bash
# 创建conda环境
conda create -n guanjia_po python=3.8
conda activate guanjia_po

# 安装依赖
conda install pyqt matplotlib pandas pillow numpy

# 运行程序
python run.py
```

## 验证安装

```python
# 测试PyQt6
python3 -c "from PyQt6.QtWidgets import QApplication; print('PyQt6 安装成功!')"

# 检查版本
python3 -c "import PyQt6; print('PyQt6版本:', PyQt6.QtCore.PYQT_VERSION_STR)"
```

## 运行应用

```bash
# 进入项目目录
cd guanjia-po

# 方法1：使用运行脚本
python3 run_system.py

# 方法2：直接运行
python3 src/main.py

# 方法3：如果安装了全部依赖
python3 run.py
```

## 故障排除

### 如果遇到编译错误：
```bash
# 安装必要的编译工具
sudo dnf install gcc gcc-c++ make qt6-qtbase-devel qt6-qttools-devel -y

# 清理pip缓存
python3 -m pip cache purge

# 重新安装
python3 -m pip install --force-reinstall PyQt6
```

### 如果遇到显示问题：
```bash
# 设置显示环境
export DISPLAY=:0
export QT_QPA_PLATFORM=offscreen

# 或者使用虚拟显示
sudo dnf install xorg-x11-server-Xvfb -y
Xvfb :99 &
export DISPLAY=:99
```

### 如果依赖冲突：
```bash
# 检查已安装的包
pip3 list | grep PyQt

# 卸载旧版本
pip3 uninstall PyQt6 PyQt5

# 重新安装
pip3 install PyQt6==6.6.1
```

## 项目文件说明

- `run.py` - 主运行脚本（需要完整依赖）
- `run_system.py` - 系统运行脚本（使用系统Python）
- `simple_demo.py` - 简化演示版本（无GUI依赖）
- `text_demo.py` - 文本演示版本
- `demo.py` - 项目结构演示

## 联系支持

如果安装遇到问题，请检查：
1. Python版本: `python3 --version`
2. PyQt6安装: `python3 -c "import PyQt6; print(PyQt6.__version__)"`
3. 系统包: `dnf list installed | grep python3-qt`