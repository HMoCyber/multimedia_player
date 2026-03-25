"""进度管理（仅负责进度条/播放位置控制）"""
import logging
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtCore import QTimer
from multimedia_player.utils.time_utils import TimeUtils


class ProgressManager:
    """进度管理器（单一职责：处理播放进度逻辑）"""

    def __init__(self, media_player: QMediaPlayer, progress_timer: QTimer):
        self.media_player = media_player
        self.progress_timer = progress_timer
        self.on_progress_updated = None  # 进度更新回调

    def update_progress(self) -> None:
        """更新进度（仅进度更新逻辑）"""
        current_pos = self.media_player.position()
        if self.on_progress_updated:
            self.on_progress_updated(current_pos)

    def set_position(self, ms: int) -> None:
        """设置播放位置（仅位置设置逻辑）"""
        if not self.media_player or self.media_player.duration() == 0:
            return

        # 边界检查
        new_pos = max(0, min(ms, self.media_player.duration()))
        old_pos = self.media_player.position()

        # 设置位置
        self.media_player.setPosition(new_pos)

        # 日志
        old_pos_str = TimeUtils.format_ms(old_pos)
        new_pos_str = TimeUtils.format_ms(new_pos)
        diff_seconds = abs(new_pos - old_pos) / 1000

        if new_pos > old_pos:
            logging.info(f"【进度管理】前进 {diff_seconds:.1f} 秒 | 从 {old_pos_str} 至 {new_pos_str}")
        elif new_pos < old_pos:
            logging.info(f"【进度管理】后退 {diff_seconds:.1f} 秒 | 从 {old_pos_str} 至 {new_pos_str}")
        else:
            logging.info(f"【进度管理】进度无变化 | 当前: {old_pos_str}")