"""主窗口入口（仅组装布局/事件/逻辑，无具体实现）"""
import logging
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt
from multimedia_player.config.config_manager import ConfigManager
from multimedia_player.ui.main_window.window_layout import WindowLayout
from multimedia_player.ui.main_window.window_logic import WindowLogic
from multimedia_player.ui.main_window.window_events import WindowEvents
from multimedia_player.core.media.media_core import MediaCore
from multimedia_player.logger.standard_logger import StandardLogger
from multimedia_player.constants.app_constants import DEFAULT_RESOLUTION, MIN_WINDOW_SIZE

class MainWindow(QMainWindow):
    """主窗口（单一职责：组装各组件，提供统一入口）"""
    def __init__(self):
        super().__init__()
        # 1. 初始化基础组件（配置管理器）
        self.config_manager = ConfigManager()

        # ========== 关键调整：先初始化ui_layout，再调用_init_base_properties ==========
        # 2. 构建UI布局（先创建ui_layout，避免后续方法访问时不存在）
        self.ui_layout = WindowLayout(self, self.config_manager)

        # 3. 初始化基础属性（内部会调用set_window_topmost，此时ui_layout已存在）
        self._init_base_properties()

        # 4. 初始化媒体核心
        self.media_core = MediaCore(self.ui_layout.video_playback_panel.get_video_widget(), self)

        # 5. 初始化业务逻辑
        self.logic = WindowLogic(self, self.ui_layout, self.config_manager, self.media_core)

        # 6. 绑定事件
        self.events = WindowEvents(self, self.ui_layout, self.logic, self.media_core)

        # 7. 注册日志处理器
        logging.getLogger().addHandler(self.ui_layout.log_panel.get_log_handler())

        # 8. 初始化日志
        self._init_startup_log()

    def _init_base_properties(self) -> None:
        """初始化基础属性（仅窗口基础配置）"""
        # 屏幕信息
        self.screen = self.parent().screen() if self.parent() else self.screen()
        self.screen_width = self.screen.geometry().width()
        self.screen_height = self.screen.geometry().height()

        # 分辨率配置
        self.player_width, self.player_height = self.config_manager.get_resolution()
        self.player_width = max(self.player_width, MIN_WINDOW_SIZE[0])
        self.player_height = max(self.player_height, MIN_WINDOW_SIZE[1])

        # 窗口基础设置
        self.setMinimumSize(*MIN_WINDOW_SIZE)
        self.resize(self.player_width, self.player_height)
        self.setWindowTitle(f"多媒体播放器 v1.0 - {self.player_width}x{self.player_height}")

        # 置顶设置（此时ui_layout已初始化，可安全调用）
        self.topmost_state = self.config_manager.get_topmost()
        self.set_window_topmost(self.topmost_state)

    def _init_startup_log(self) -> None:
        """初始化启动日志（仅日志输出）"""
        logging.info(f"""【系统启动】播放器初始化完成 | 
  分辨率: {self.player_width}x{self.player_height} | 
  置顶状态: {self.topmost_state} | 
  进度步长: {self.config_manager.get_step_seconds()}秒 | 
  上次目录: {self.config_manager.get_last_directory() or '无'}""")

    # ========== 窗口控制方法 ==========
    def set_window_topmost(self, topmost: bool) -> None:
        """设置窗口置顶（仅窗口状态变更）"""
        if topmost:
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)
        self.show()  # 重新显示以应用标志
        # 此时ui_layout已存在，可安全访问
        self.ui_layout.video_playback_panel.cb_topmost.setChecked(topmost)

    # ========== 事件重写 ==========
    def keyPressEvent(self, event) -> None:
        """键盘事件（仅转发到事件层）"""
        if not self.events.handle_key_press_event(event):
            super().keyPressEvent(event)