"""日志格式化器（自定义日志格式）"""
import logging
from multimedia_player.constants.format_constants import (
    LOG_TIME_FORMAT,  # 日志时间格式
    LOG_MESSAGE_FORMAT  # 日志消息格式
)

class StandardLogFormatter(logging.Formatter):
    """标准日志格式化器（兼容logging模块）"""

    def __init__(self, fmt=LOG_MESSAGE_FORMAT, datefmt=LOG_TIME_FORMAT, style='%'):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)

    def format(self, record):
        """重写format方法，确保时间格式统一、级别名称对齐"""
        # 对齐日志级别名称（如INFO    | ERROR   ，便于阅读）
        record.levelname = record.levelname.ljust(8)
        # 调用父类方法完成最终格式化
        return super().format(record)

# 关键：添加CustomLogFormatter别名（兼容log_init.py的导入）
CustomLogFormatter = StandardLogFormatter