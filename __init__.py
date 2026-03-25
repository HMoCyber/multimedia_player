"""多媒体播放器项目包"""
__version__ = "1.0.1"

# 导出核心组件（简化上层导入）
from multimedia_player.core.media.media_core import MediaCore
from multimedia_player.ui.main_window.main_window import MainWindow
from multimedia_player.config.config_manager import ConfigManager