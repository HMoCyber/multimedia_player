"""视频播放面板（仅视频显示+置顶复选框，单一职责）"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout,
    QCheckBox, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt
# 核心修复：QVideoWidget 从 QtMultimediaWidgets 导入（PyQt6 新标准）
from PyQt6.QtMultimediaWidgets import QVideoWidget

class VideoPlaybackPanel(QWidget):
    """视频播放面板（负责视频画面展示 + 窗口置顶控件）"""
    def __init__(self, parent=None):
        super().__init__(parent)
        # 核心控件
        self.video_widget = QVideoWidget()
        self.cb_topmost = QCheckBox("窗口置顶")
        # 初始化UI
        self._init_ui()

    def _init_ui(self):
        """初始化界面布局（适配PyQt6 + Python3.13）"""
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)

        # 视频控件：自适应拉伸（填满父容器）
        video_size_policy = QSizePolicy(
            QSizePolicy.Policy.Expanding,   # 水平策略：Expanding
            QSizePolicy.Policy.Expanding    # 垂直策略：Expanding
        )
        self.video_widget.setSizePolicy(video_size_policy)
        self.video_widget.setStyleSheet("background-color: #1A1A1A;")

        # 置顶复选框布局（右对齐）
        top_layout = QHBoxLayout()
        top_spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        top_layout.addSpacerItem(top_spacer)
        top_layout.addWidget(self.cb_topmost)
        top_layout.setContentsMargins(10, 5, 10, 5)

        # 组装布局
        main_layout.addWidget(self.video_widget)
        main_layout.addLayout(top_layout)

    def get_video_widget(self) -> QVideoWidget:
        """获取视频控件（供媒体核心使用）"""
        return self.video_widget

    def clear_subtitle(self):
        """清空字幕（预留接口）"""
        pass

    def update_subtitle_display(self, text: str):
        """更新字幕显示（预留接口）"""
        pass