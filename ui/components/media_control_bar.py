"""播放控制栏（仅控制栏UI/逻辑）"""
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QSlider, QLabel,
    QStyle
)
from PyQt6.QtCore import Qt
from multimedia_player.ui.styles.dark_style import STYLESHEETS, get_slider_style
from multimedia_player.constants.style_constants import (
    CONTROL_BTN_SIZE, VOLUME_SLIDER_WIDTH, TIME_LABEL_WIDTH
)
from multimedia_player.constants.app_constants import DEFAULT_STEP_SECONDS


class MediaControlBar(QWidget):
    """播放控制栏（单一职责：播放控制UI/操作）"""

    def __init__(self, step_seconds=DEFAULT_STEP_SECONDS, parent=None):
        super().__init__(parent)
        self.step_seconds = step_seconds
        self.btn_play_pause = None
        self.btn_replay = None
        self.progress_slider = None
        self.volume_slider = None
        self.time_label = None
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化UI（仅布局）"""
        layout = QHBoxLayout(self)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 5, 0, 5)

        # 播放/暂停按钮
        self.btn_play_pause = QPushButton()
        self.btn_play_pause.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.btn_play_pause.setFixedSize(*CONTROL_BTN_SIZE)
        self.btn_play_pause.setStyleSheet(STYLESHEETS["push_button"])
        self.btn_play_pause.setEnabled(False)
        layout.addWidget(self.btn_play_pause)

        # 进度条
        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.progress_slider.setRange(0, 100)
        self.progress_slider.setStyleSheet(get_slider_style())
        layout.addWidget(self.progress_slider, stretch=1)

        # 时间标签
        self.time_label = QLabel(f"00:00:00,000 / 00:00:00,000 (步长：{self.step_seconds}秒)")
        self.time_label.setFixedWidth(TIME_LABEL_WIDTH)
        self.time_label.setStyleSheet(STYLESHEETS["label"])
        layout.addWidget(self.time_label)

        # 音量控制
        lbl_volume = QLabel("音量:")
        lbl_volume.setStyleSheet(STYLESHEETS["label"])
        layout.addWidget(lbl_volume)

        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(80)
        self.volume_slider.setFixedWidth(VOLUME_SLIDER_WIDTH)
        self.volume_slider.setStyleSheet(get_slider_style())
        layout.addWidget(self.volume_slider)

        # 重播按钮
        self.btn_replay = QPushButton("重播")
        self.btn_replay.setStyleSheet(STYLESHEETS["push_button"])
        self.btn_replay.setEnabled(False)
        layout.addWidget(self.btn_replay)

    # ========== 状态更新方法 ==========
    def update_time_display(self, current_ms: int, total_ms: int) -> None:
        """更新时间显示（仅更新UI）"""
        from multimedia_player.utils.time_utils import TimeUtils
        current_time = TimeUtils.format_ms(current_ms)
        total_time = TimeUtils.format_ms(total_ms)
        self.time_label.setText(f"{current_time} / {total_time} (步长：{self.step_seconds}秒)")

    def update_play_button_state(self, is_playing: bool) -> None:
        """更新播放按钮图标（仅更新UI）"""
        if is_playing:
            self.btn_play_pause.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
        else:
            self.btn_play_pause.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))

    def set_step_seconds(self, step: int) -> None:
        """设置步长（仅更新值）"""
        self.step_seconds = step
        # 更新时间标签
        current_text = self.time_label.text().split(" (步长：")[0]
        self.time_label.setText(f"{current_text} (步长：{step}秒)")

    def enable_controls(self, enabled: bool) -> None:
        """启用/禁用控制按钮（仅更新状态）"""
        self.btn_play_pause.setEnabled(enabled)
        self.btn_replay.setEnabled(enabled)