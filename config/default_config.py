"""默认配置（纯字典，无逻辑）"""
from multimedia_player.constants.app_constants import DEFAULT_STEP_SECONDS, DEFAULT_RESOLUTION

DEFAULT_CONFIG = {
    "General": {
        "step_seconds": str(DEFAULT_STEP_SECONDS),
        "topmost": "True",
        "last_directory": "",
        "width": str(DEFAULT_RESOLUTION[0]),
        "height": str(DEFAULT_RESOLUTION[1])
    },
    "UI": {
        "theme": "dark",
        "font_size": "9"
    }
}