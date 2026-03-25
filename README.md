# 多媒体播放器项目文档
## 文档信息
| 项类   | 内容             |
|------|----------------|
| 项目版本 | v1.0.1         |
| 开发语言 | Python 3.8+    |
| 核心框架 | PyQt6 6.7.0    |
| 适用系统 | Windows        |
| 维护原则 | 单一职责、层间解耦、组件复用 |

## 1. 项目概述
轻量级跨平台多媒体播放器，支持主流媒体格式播放、SRT/TXT格式字幕加载、灵活的播放控制（进度调整/音量调节/窗口置顶）等核心功能。项目采用**极致细分的代码结构**，每个文件仅负责单一功能点，大幅降低维护成本，便于功能拓展。

## 2. 环境准备
### 2.1 基础要求
- Python版本：3.8 及以上（推荐3.10+）
- 系统权限：可读写本地文件、创建临时目录

### 2.2 依赖安装
```bash
# 方式1：通过requirements.txt安装（推荐）
pip install -r requirements.txt

# 方式2：手动安装
pip install PyQt6==6.7.0
```

## 3. 项目结构
```
multimedia_player/                  # 项目根目录
├── __init__.py                     # 项目包导出（简化上层导入）
├── main.py                         # 程序入口（仅负责启动/退出/资源清理）
├── constants/                      # 常量层（纯数据，无业务逻辑）
│   ├── __init__.py                 # 导出所有常量
│   ├── app_constants.py            # 基础配置（步长、分辨率、临时目录等）
│   ├── style_constants.py          # UI样式常量（颜色、字体、尺寸、边距）
│   └── format_constants.py         # 格式常量（支持的文件格式、日志/时间格式）
├── config/                         # 配置层（仅处理配置读写）
│   ├── __init__.py                 # 导出配置类
│   ├── config_manager.py           # 配置读写核心逻辑（通用/快捷方法）
│   └── default_config.py           # 默认配置字典（纯数据，无逻辑）
├── logger/                         # 日志层（仅处理日志相关）
│   ├── __init__.py                 # 导出日志组件
│   ├── standard_logger.py          # UI日志处理器（输出日志到界面）
│   ├── log_formatter.py            # 日志格式化（统一日志字符串格式）
│   └── log_init.py                 # 日志系统初始化（文件/控制台日志）
├── utils/                          # 工具层（通用工具函数，无业务耦合）
│   ├── __init__.py                 # 导出工具类
│   ├── time_utils.py               # 时间转换/格式化（毫秒转时分秒等）
│   ├── path_utils.py               # 路径处理（相对路径、扩展名、文件大小等）
│   ├── file_utils.py               # 文件基础操作（读取、类型判断、过滤）
│   ├── file_scanner.py             # 目录扫描（仅扫描媒体/字幕文件）
│   └── subtitle/                   # 字幕解析子包（可独立复用）
│       ├── __init__.py             # 导出解析器+提供统一获取方法
│       ├── subtitle_base.py        # 字幕解析基类（定义统一接口）
│       ├── srt_parser.py           # SRT格式解析（仅处理SRT）
│       └── txt_parser.py           # TXT格式解析（仅处理TXT）
├── ui/                             # UI层（仅处理界面相关，无核心业务）
│   ├── __init__.py                 # 导出UI组件
│   ├── styles/                     # 样式管理（纯样式表字符串）
│   │   ├── __init__.py
│   │   └── dark_style.py           # 深色主题样式表（可新增浅色主题）
│   ├── dialogs/                    # 对话框组件（独立弹窗）
│   │   ├── __init__.py
│   │   ├── dialog_base.py          # 对话框基类（通用配置：模态、标题等）
│   │   ├── step_setting_dialog.py  # 进度步长设置（仅步长相关）
│   │   └── resolution_setting_dialog.py # 分辨率设置（仅分辨率相关）
│   ├── components/                 # 可复用UI组件（独立封装）
│   │   ├── __init__.py
│   │   ├── file_tree_panel.py      # 文件树面板（仅显示文件/目录）
│   │   ├── media_control_bar.py    # 播放控制栏（仅播放/进度/音量按钮）
│   │   ├── log_panel.py            # 日志面板（仅显示日志）
│   │   ├── subtitle_panel.py       # 字幕面板（仅显示字幕内容）
│   │   └── video_playback_panel.py # 视频播放面板（仅视频+置顶复选框）
│   └── main_window/                # 主窗口（拆分布局/事件/逻辑）
│       ├── __init__.py
│       ├── main_window.py          # 主窗口入口（组装所有组件）
│       ├── window_layout.py        # 仅负责UI布局（无事件/逻辑）
│       ├── window_events.py        # 仅负责事件绑定/转发（无业务逻辑）
│       └── window_logic.py         # 仅负责业务逻辑（无UI/事件）
├── core/                           # 核心层（业务核心，无UI耦合）
│   ├── __init__.py                 # 导出核心组件
│   ├── media/                      # 媒体核心子包（播放相关）
│   │   ├── __init__.py
│   │   ├── media_core.py           # 媒体核心入口（组装子组件）
│   │   ├── playback_control.py     # 仅处理播放/暂停/重播/加载媒体
│   │   ├── progress_manager.py     # 仅处理播放进度（设置/更新）
│   │   ├── volume_manager.py       # 仅处理音量（设置/静音/恢复）
│   │   └── subtitle_manager.py     # 字幕管理（预留拓展接口）
│   └── events/                     # 事件总线（预留：解耦组件通信）
│       ├── __init__.py
│       └── event_bus.py            # 事件订阅/发布（统一通信）
└── resources/                      # 资源层（预留：图标/翻译等）
    ├── __init__.py
    └── icons/                      # 图标资源目录
```

## 5. 项目贡献
项目作者：Morland
