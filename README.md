# 官家婆 - 个人家庭账目库存管理软件

## 简介

官家婆是一款专为家庭设计的个人财务管理软件，帮助用户轻松管理家庭收支和物品库存。

## 主要功能

### 💰 账目管理
- 收入支出记录
- 分类管理（餐饮、购物、交通等）
- 月度/年度统计
- 自定义分类和标签

### 📦 库存管理
- 物品入库出库记录
- 库存预警功能
- 批量操作支持
- 库存统计分析

### 📊 统计报表
- 可视化图表展示
- 收支趋势分析
- 分类占比统计
- 月度/年度对比

### 🎨 界面特色
- 现代化GUI设计
- 简洁易用的操作界面
- 支持多种主题
- 响应式布局

## 技术特点

- **框架**: PyQt6
- **数据库**: SQLite3
- **图表**: Matplotlib
- **平台**: Windows/macOS/Linux
- **打包**: PyInstaller

## 安装说明

### 环境要求
- Python 3.8+
- PyQt6
- SQLite3

### 开发环境安装

1. 克隆项目
```bash
git clone https://github.com/guanjiapo/guanjiapo.git
cd guanjiapo
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行程序
```bash
python run.py
```

### 打包发布

使用PyInstaller打包成可执行文件：

```bash
python build_exe.py
```

打包完成后，可执行文件位于 `dist/官家婆.exe`

## 使用指南

### 首次使用
1. 启动应用程序
2. 在"总览"页面查看系统状态
3. 开始记录您的收支和库存信息

### 账目管理
1. 点击"账目管理"进入账目页面
2. 点击"添加账目"记录新的收入或支出
3. 选择相应的分类和填写详细信息
4. 可以查看和编辑历史记录

### 库存管理
1. 点击"库存管理"进入库存页面
2. 添加物品信息（名称、分类、数量等）
3. 记录入库出库操作
4. 设置最低库存以启用预警功能

### 统计分析
1. 点击"统计报表"查看各类图表
2. 选择时间段进行分析
3. 导出统计报告

## 项目结构

```
guanjia-po/
├── src/                    # 源代码
│   ├── ui/                # UI组件
│   │   ├── main_window.py # 主窗口
│   │   ├── dashboard.py   # 总览页面
│   │   ├── account.py     # 账目管理
│   │   ├── inventory.py   # 库存管理
│   │   └── statistics.py  # 统计报表
│   ├── database/          # 数据库操作
│   │   ├── database.py    # 数据库管理
│   │   └── models.py      # 数据模型
│   ├── widgets/           # 自定义组件
│   ├── utils/             # 工具函数
│   └── main.py           # 程序入口
├── resources/             # 资源文件
│   ├── icons/            # 图标文件
│   └── styles.qss        # 样式表
├── requirements.txt       # 依赖包
├── setup.py              # 安装配置
├── build_exe.py          # 打包脚本
├── run.py                # 运行脚本
└── README.md             # 说明文档
```

## 数据安全

- 所有数据本地存储，不上传云端
- 数据库文件位于用户目录下的 `.guanjia-po` 文件夹
- 建议定期备份数据库文件
- 支持数据导出和导入功能

## 常见问题

### Q: 程序无法启动？
A: 请检查Python版本是否为3.8+，并确保已安装所有依赖包。

### Q: 数据丢失了怎么办？
A: 检查用户目录下的 `.guanjia-po` 文件夹，数据库文件可能还在那里。建议定期备份。

### Q: 如何添加新的分类？
A: 在账目管理页面中，可以添加自定义分类，设置名称和颜色。

### Q: 库存预警如何工作？
A: 当物品库存低于设定的最低值时，系统会在总览页面显示预警提示。

## 更新日志

### v1.0.0 (2024-01-01)
- 🎉 首次发布
- ✨ 基础账目管理功能
- ✨ 库存管理功能
- ✨ 统计报表功能
- ✨ 现代化UI设计

## 贡献指南

欢迎提交Issue和Pull Request来改进项目！

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 联系我们

- 项目主页: https://github.com/guanjiapo/guanjiapo
- 问题反馈: https://github.com/guanjiapo/guanjiapo/issues
- 邮箱: support@guanjiapo.com

---

**官家婆** - 让家庭财务管理更简单！ 🏠💰