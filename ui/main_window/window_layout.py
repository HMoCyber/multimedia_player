"""主窗口布局（负责所有UI组件的组装，单一职责）"""
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QSizePolicy, QSplitter
)
from PyQt6.QtCore import Qt
from multimedia_player.ui.components.video_playback_panel import VideoPlaybackPanel
from multimedia_player.ui.components.file_tree_panel import FileTreePanel
from multimedia_player.ui.components.log_panel import LogPanel
from multimedia_player.ui.components.subtitle_panel import SubtitlePanel
from multimedia_player.config.config_manager import ConfigManager

class WindowLayout:
    """主窗口布局管理器（组装所有UI面板）"""
    def __init__(self, main_window: QWidget, config_manager: ConfigManager):
        self.main_window = main_window
        self.config_manager = config_manager

        # 声明所有子面板
        self.file_tree_panel = None
        self.video_playback_panel = None
        self.log_panel = None
        self.subtitle_panel = None

        # 构建主布局
        self._build_main_layout()

    def _build_main_layout(self):
        """构建整体布局（修复screen()调用 + 修复FileTreePanel参数）"""
        # 核心修复：screen() 必须加括号调用
        screen = self.main_window.screen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # 主容器Widget
        central_widget = QWidget()
        self.main_window.setCentralWidget(central_widget)

        # 主垂直布局
        main_v_layout = QVBoxLayout(central_widget)
        main_v_layout.setContentsMargins(10, 10, 10, 10)
        main_v_layout.setSpacing(8)

        # 上部分：文件树 + 视频面板
        top_splitter = QSplitter(Qt.Orientation.Horizontal)
        top_splitter.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        # ===================== 核心修复：传入 config_manager 参数 =====================
        self.file_tree_panel = FileTreePanel(self.config_manager)
        self.file_tree_panel.setMinimumWidth(int(screen_width * 0.2))
        top_splitter.addWidget(self.file_tree_panel)

        # 右侧视频面板
        self.video_playback_panel = VideoPlaybackPanel()
        self.video_playback_panel.setMinimumWidth(int(screen_width * 0.5))
        top_splitter.addWidget(self.video_playback_panel)

        # 下部分：日志 + 字幕
        bottom_splitter = QSplitter(Qt.Orientation.Horizontal)
        bottom_splitter.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )
        bottom_splitter.setFixedHeight(180)

        # 左侧日志面板
        self.log_panel = LogPanel()
        self.log_panel.setMinimumWidth(int(screen_width * 0.3))
        bottom_splitter.addWidget(self.log_panel)

        # 右侧字幕面板
        self.subtitle_panel = SubtitlePanel()
        self.subtitle_panel.setMinimumWidth(int(screen_width * 0.4))
        bottom_splitter.addWidget(self.subtitle_panel)

        # 组装到主布局
        main_v_layout.addWidget(top_splitter)
        main_v_layout.addWidget(bottom_splitter)