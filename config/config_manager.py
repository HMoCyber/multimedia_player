"""配置管理器（处理配置读写）"""
import configparser
import os
from multimedia_player.constants.app_constants import (
    DEFAULT_RESOLUTION,
    DEFAULT_STEP_SECONDS,
    CONFIG_FILE_PATH
)

class ConfigManager:
    """配置管理类（统一读写配置文件）"""

    def __init__(self):
        self.config = configparser.ConfigParser()
        # 初始化配置文件（不存在则创建）
        self._init_config_file()

    def _init_config_file(self):
        """初始化配置文件（不存在则创建并写入默认值）"""
        if not os.path.exists(CONFIG_FILE_PATH):
            # 创建默认配置
            self.config["General"] = {
                "topmost": "True",
                "width": str(DEFAULT_RESOLUTION[0]),
                "height": str(DEFAULT_RESOLUTION[1]),
                "step_seconds": str(DEFAULT_STEP_SECONDS),
                "last_directory": ""
            }
            # 保存到文件
            with open(CONFIG_FILE_PATH, "w", encoding="utf-8") as f:
                self.config.write(f)
        else:
            # 读取现有配置
            self.config.read(CONFIG_FILE_PATH, encoding="utf-8")

    def get_topmost(self) -> bool:
        """获取窗口置顶状态（默认True）"""
        return self.config.getboolean("General", "topmost", fallback=True)

    def get_resolution(self) -> tuple[int, int]:
        """获取窗口分辨率（默认DEFAULT_RESOLUTION）"""
        width = self.config.getint("General", "width", fallback=DEFAULT_RESOLUTION[0])
        height = self.config.getint("General", "height", fallback=DEFAULT_RESOLUTION[1])
        return (width, height)

    def get_step_seconds(self) -> int:
        """获取进度步长（默认10秒）"""
        return self.config.getint("General", "step_seconds", fallback=DEFAULT_STEP_SECONDS)

    def get_last_directory(self) -> str:
        """获取上次打开的目录（默认空）"""
        return self.config.get("General", "last_directory", fallback="")

    def set_step_seconds(self, step: int):
        """设置进度步长"""
        self.config["General"]["step_seconds"] = str(step)
        self._save_config()

    def set_resolution(self, width: int, height: int):
        """设置分辨率"""
        self.config["General"]["width"] = str(width)
        self.config["General"]["height"] = str(height)
        self._save_config()

    def update_section(self, section: str, data: dict):
        """更新配置节"""
        if section not in self.config:
            self.config[section] = {}
        self.config[section].update(data)
        self._save_config()

    def _save_config(self):
        """保存配置到文件"""
        with open(CONFIG_FILE_PATH, "w", encoding="utf-8") as f:
            self.config.write(f)