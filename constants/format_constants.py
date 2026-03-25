"""格式常量（纯数据，无逻辑）"""
import re

# ===================== 日志相关常量 =====================
# 日志级别（DEBUG/INFO/WARNING/ERROR/CRITICAL）
LOG_LEVEL = "INFO"
# 日志文件存储目录
LOG_FILE_DIR = "./logs"
# 日志文件名格式（strftime格式，%Y-%m-%d等是合法的）
LOG_FILE_NAME_FORMAT = "multimedia_player_%Y%m%d_%H%M%S.log"
# 日志消息格式（logging标准格式符，必须用%(xxx)s）
LOG_MESSAGE_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
# 日志时间显示格式（strftime格式）
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
# log_formatter.py需要的LOG_TIME_FORMAT（别名）
LOG_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# ===================== 文件格式常量 =====================
# 支持的媒体文件格式（小写）
SUPPORTED_MEDIA_FORMATS = (
    "mp3", "mp4", "avi", "mkv", "flv", "wmv", "mov", "wav", "ogg", "m4a"
)
# 支持的字幕文件格式（小写）
SUPPORTED_SUBTITLE_FORMATS = ("srt", "txt", "ass")

# ===================== 时间格式常量 =====================
# 播放时间显示格式（用于UI，兼容旧的TIME_DISPLAY_FORMAT）
PLAY_TIME_FORMAT = "%H:%M:%S"
# time_utils.py需要的TIME_DISPLAY_FORMAT（和PLAY_TIME_FORMAT一致）
TIME_DISPLAY_FORMAT = "%H:%M:%S"
# 文件大小显示单位
FILE_SIZE_UNITS = ("B", "KB", "MB", "GB")

# ===================== 字幕解析常量 =====================
# SRT字幕解析正则表达式（匹配：序号 + 时间戳 + 内容）
SRT_PATTERN = re.compile(
    r'(\d+)\r?\n'  # 序号（如1、2、3）
    r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\r?\n'  # 时间戳（00:00:01,000 --> 00:00:05,000）
    r'([\s\S]*?)(?:\r?\n\r?\n|$)',  # 字幕内容（支持多行）
    re.MULTILINE
)
# SRT时间戳格式（用于转换为毫秒）
SRT_TIME_FORMAT = "%H:%M:%S,%f"