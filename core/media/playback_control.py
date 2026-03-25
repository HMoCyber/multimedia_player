"""播放控制（仅负责播放/暂停/重播/加载媒体）"""
import logging
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl, QTimer
from multimedia_player.utils.path_utils import PathUtils


class PlaybackControl:
    """播放控制器（单一职责：处理播放/暂停/重播/加载逻辑）"""

    def __init__(self, media_player: QMediaPlayer, audio_output: QAudioOutput):
        self.media_player = media_player
        self.audio_output = audio_output
        self.last_volume = 80  # 默认音量

    def load_media(self, file_path: str) -> None:
        """加载媒体文件（仅加载逻辑）"""
        try:
            file_name = PathUtils.get_file_name(file_path)
            # 停止当前播放
            if self.media_player.isPlaying():
                self.stop()
                logging.info(f"【播放控制】停止当前播放 | 准备加载: {file_name}")

            # 设置媒体源
            self.media_player.setSource(QUrl.fromLocalFile(file_path))
            # 延迟播放（确保加载完成）
            QTimer.singleShot(500, self.play)

            logging.info(f"【播放控制】加载媒体成功 | 文件名: {file_name} | 路径: {file_path}")

        except Exception as e:
            logging.error(f"【播放控制】加载失败 | 路径: {file_path} | 错误: {str(e)}")
            raise RuntimeError(f"加载媒体失败: {str(e)}")

    def play(self) -> None:
        """播放（仅播放逻辑）"""
        if self.media_player.playbackState() != QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.play()
            from multimedia_player.utils.time_utils import TimeUtils
            current_pos = TimeUtils.format_ms(self.media_player.position())
            logging.info(f"【播放控制】开始播放 | 当前进度: {current_pos}")

    def pause(self) -> None:
        """暂停（仅暂停逻辑）"""
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.pause()
            from multimedia_player.utils.time_utils import TimeUtils
            current_pos = TimeUtils.format_ms(self.media_player.position())
            logging.info(f"【播放控制】暂停播放 | 当前进度: {current_pos}")

    def stop(self) -> None:
        """停止（仅停止逻辑）"""
        self.media_player.stop()
        logging.info(f"【播放控制】停止播放")

    def replay(self) -> None:
        """重播（仅重播逻辑）"""
        self.media_player.setPosition(0)
        self.play()
        logging.info(f"【播放控制】重播媒体")