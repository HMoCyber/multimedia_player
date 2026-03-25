"""媒体核心入口（仅组装核心组件，提供统一接口）"""
import logging
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl, QTimer, Qt
from PyQt6.QtWidgets import QWidget, QMessageBox
from multimedia_player.core.media.playback_control import PlaybackControl
from multimedia_player.core.media.progress_manager import ProgressManager
from multimedia_player.core.media.volume_manager import VolumeManager
from multimedia_player.constants.app_constants import PROGRESS_UPDATE_INTERVAL


class MediaCore:
    """媒体核心（单一职责：组装播放/进度/音量组件，提供统一接口）"""

    def __init__(self, video_widget: QVideoWidget, parent: QWidget = None):
        self.parent = parent
        self.video_widget = video_widget

        # 基础组件
        self.audio_output = QAudioOutput()
        self.media_player = QMediaPlayer()
        self.progress_timer = QTimer()

        # 核心子组件
        self.playback_control = PlaybackControl(self.media_player, self.audio_output)
        self.progress_manager = ProgressManager(self.media_player, self.progress_timer)
        self.volume_manager = VolumeManager(self.audio_output)

        # 状态变量
        self.is_seeking = False
        self.current_media_path = None

        # 回调函数（解耦UI）
        self.on_progress_updated = None  # 进度更新回调
        self.on_duration_updated = None  # 时长更新回调
        self.on_playback_state_changed = None  # 播放状态变更回调

        # 初始化
        self._init_core()
        self._bind_core_events()

    def _init_core(self) -> None:
        """初始化核心（仅基础配置）"""
        # 绑定音频/视频输出
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setVideoOutput(self.video_widget)

        # 初始化定时器
        self.progress_timer.setInterval(PROGRESS_UPDATE_INTERVAL)
        self.progress_timer.timeout.connect(self._on_progress_timer)
        self.progress_timer.start()

        logging.info("【媒体核心】初始化完成")

    def _bind_core_events(self) -> None:
        """绑定核心事件（仅事件绑定）"""
        # 媒体播放器事件
        self.media_player.errorOccurred.connect(self._on_error)
        self.media_player.playbackStateChanged.connect(self._on_playback_state_changed)
        self.media_player.durationChanged.connect(self._on_duration_changed)

        # 进度管理器回调
        self.progress_manager.on_progress_updated = self._on_progress_updated

    # ========== 核心事件处理 ==========
    def _on_error(self, error, error_string) -> None:
        """错误事件（仅日志+弹窗）"""
        logging.error(f"【媒体核心】播放错误 | 类型: {error} | 信息: {error_string}")
        QMessageBox.warning(
            self.parent, "播放警告",
            f"媒体预览失败:\n{error_string}\n请确认文件完整且格式支持"
        )

    def _on_playback_state_changed(self, state) -> None:
        """播放状态变更（仅转发回调）"""
        if self.on_playback_state_changed:
            self.on_playback_state_changed(state)

    def _on_duration_changed(self, duration: int) -> None:
        """时长变更（仅转发回调）"""
        if duration > 0 and self.on_duration_updated:
            self.on_duration_updated(duration)
            from multimedia_player.utils.time_utils import TimeUtils
            total_time = TimeUtils.format_ms(duration)
            logging.info(f"【媒体核心】时长解析完成 | 总时长: {total_time} ({duration / 1000 / 60:.2f}分钟)")

    def _on_progress_timer(self) -> None:
        """进度定时器（仅转发到进度管理器）"""
        if not self.is_seeking and self.media_player.duration() > 0:
            self.progress_manager.update_progress()

    def _on_progress_updated(self, current_pos: int) -> None:
        """进度更新（仅转发回调）"""
        if self.on_progress_updated:
            self.on_progress_updated(current_pos)

    # ========== 对外接口（转发到子组件） ==========
    def load_media(self, file_path: str) -> None:
        """加载媒体文件（转发到播放控制）"""
        self.current_media_path = file_path
        self.playback_control.load_media(file_path)

    def play(self) -> None:
        """播放（转发到播放控制）"""
        self.playback_control.play()

    def pause(self) -> None:
        """暂停（转发到播放控制）"""
        self.playback_control.pause()

    def stop(self) -> None:
        """停止（转发到播放控制）"""
        self.playback_control.stop()

    def replay(self) -> None:
        """重播（转发到播放控制）"""
        self.playback_control.replay()

    def set_position(self, ms: int) -> None:
        """设置播放位置（转发到进度管理器）"""
        self.progress_manager.set_position(ms)

    def set_volume(self, volume: int) -> None:
        """设置音量（转发到音量管理器）"""
        self.volume_manager.set_volume(volume)

    # ========== 拓展接口（预留） ==========
    def set_playlist(self, file_paths: list) -> None:
        """设置播放列表（预留接口）"""
        logging.warning("【媒体核心】播放列表功能暂未实现")

    def set_playback_rate(self, rate: float) -> None:
        """设置播放倍速（预留接口）"""
        logging.warning("【媒体核心】倍速播放功能暂未实现")