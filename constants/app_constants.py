"""应用基础常量（纯数据，无逻辑）"""
import tempfile

# 基础配置
DEFAULT_STEP_SECONDS = 10
CONFIG_FILE_NAME = "multimedia_player_config.ini"
TEMP_DIR = tempfile.mkdtemp(prefix="multimedia_player_temp_")
PROGRESS_UPDATE_INTERVAL = 50  # 进度更新间隔（毫秒）

# 分辨率配置
DEFAULT_RESOLUTION = (1000, 800)
MIN_WINDOW_SIZE = (800, 700)
BUILTIN_RESOLUTIONS = [
    (800, 600, "默认 (800x600)"),
    (1000, 800, "优化版 (1000x800)"),
    (1024, 768, "XGA (1024x768)"),
    (1280, 720, "720P (1280x720)"),
    (1280, 800, "WXGA (1280x800)"),
    (1280, 1024, "SXGA (1280x1024)"),
    (1366, 768, "WXGA+ (1366x768)"),
    (1440, 900, "WSXGA+ (1440x900)"),
    (1600, 900, "HD+ (1600x900)"),
    (1920, 1080, "1080P/1K (1920x1080)"),
    (0, 0, "屏幕分辨率 (自动)")
]

"""应用常量（纯数据，无逻辑）"""
# 窗口默认分辨率
DEFAULT_RESOLUTION = (1000, 800)
# 最小窗口分辨率
MIN_WINDOW_SIZE = (800, 600)
# 默认进度步长（秒）
DEFAULT_STEP_SECONDS = 10
# 配置文件路径
CONFIG_FILE_PATH = "./multimedia_player_config.ini"
# 临时目录
TEMP_DIR = "./temp"