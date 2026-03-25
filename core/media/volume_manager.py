"""音量管理（仅负责音量控制）"""
import logging
from PyQt6.QtMultimedia import QAudioOutput


class VolumeManager:
    """音量管理器（单一职责：处理音量逻辑）"""

    def __init__(self, audio_output: QAudioOutput):
        self.audio_output = audio_output
        self.last_volume = 80  # 初始音量（0-100）
        # 设置初始音量
        self.audio_output.setVolume(self.last_volume / 100)

    def set_volume(self, volume: int) -> None:
        """设置音量（仅音量设置逻辑）"""
        # 边界检查
        volume = max(0, min(volume, 100))
        if volume == self.last_volume:
            return

        # 设置音量
        self.audio_output.setVolume(volume / 100)
        logging.info(f"【音量管理】更新音量 | 旧值: {self.last_volume}% | 新值: {volume}%")
        self.last_volume = volume

    def get_volume(self) -> int:
        """获取当前音量（仅取值）"""
        return self.last_volume

    def mute(self) -> None:
        """静音（预留拓展）"""
        current_volume = self.last_volume
        self.set_volume(0)
        logging.info(f"【音量管理】静音 | 原音量: {current_volume}%")

    def unmute(self, restore_volume: int = None) -> None:
        """取消静音（预留拓展）"""
        restore_volume = restore_volume or self.last_volume
        self.set_volume(restore_volume)
        logging.info(f"【音量管理】取消静音 | 恢复音量: {restore_volume}%")