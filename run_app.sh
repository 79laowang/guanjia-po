#!/bin/bash
# 官家婆应用程序启动脚本

# 激活虚拟环境
if [ -d "guanjia_po_env" ]; then
    echo "激活虚拟环境..."
    source guanjia_po_env/bin/activate
else
    echo "警告: 未找到虚拟环境 guanjia_po_env"
fi

# 检查是否设置了 DISPLAY
if [ -z "$DISPLAY" ]; then
    echo "设置虚拟显示..."
    export DISPLAY=:99
    # 启动 Xvfb 如果尚未运行
    if ! pgrep -f "Xvfb :99" > /dev/null; then
        Xvfb :99 -screen 0 1024x768x24 &> /dev/null &
        sleep 2
    fi
fi

# 运行应用程序
echo "启动官家婆应用程序..."
python run.py
