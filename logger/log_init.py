"""日志系统初始化（最终修复版：解决CustomLogFormatter导入错误）"""
import logging
import os
from datetime import datetime

# 导入格式常量
from multimedia_player.constants.format_constants import (
    LOG_LEVEL,
    LOG_FILE_DIR,
    LOG_FILE_NAME_FORMAT,
    LOG_MESSAGE_FORMAT,
    LOG_DATE_FORMAT
)
# 关键：导入CustomLogFormatter（现在log_formatter.py中已定义别名）
from multimedia_player.logger.log_formatter import CustomLogFormatter
from multimedia_player.utils.path_utils import PathUtils

def init_logging():
    """初始化日志系统（控制台+文件日志）"""
    # 1. 创建日志目录（兼容Windows/Linux，exist_ok避免重复创建报错）
    if not os.path.exists(LOG_FILE_DIR):
        os.makedirs(LOG_FILE_DIR, exist_ok=True)

    # 2. 生成日志文件名（按时间戳命名）
    log_file_name = datetime.now().strftime(LOG_FILE_NAME_FORMAT)
    log_file_path = os.path.join(LOG_FILE_DIR, log_file_name)

    # 3. 重置根日志器（清除默认处理器，避免重复输出）
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    # 将字符串级别转为logging常量（兼容写法，避免手动判断）
    log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    root_logger.setLevel(log_level)

    # 4. 控制台日志处理器（使用自定义格式化器）
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    # 使用CustomLogFormatter（兼容旧代码）
    console_formatter = CustomLogFormatter(
        fmt=LOG_MESSAGE_FORMAT,
        datefmt=LOG_DATE_FORMAT
    )
    console_handler.setFormatter(console_formatter)

    # 5. 文件日志处理器（UTF-8编码避免中文乱码）
    file_handler = logging.FileHandler(
        log_file_path,
        mode="a",  # 追加模式
        encoding="utf-8"
    )
    file_handler.setLevel(log_level)
    file_formatter = CustomLogFormatter(
        fmt=LOG_MESSAGE_FORMAT,
        datefmt=LOG_DATE_FORMAT
    )
    file_handler.setFormatter(file_formatter)

    # 6. 添加处理器到根日志器
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # 验证日志初始化
    logging.info("【系统初始化】日志系统初始化完成")
    logging.info(f"【系统初始化】日志文件路径：{log_file_path}")