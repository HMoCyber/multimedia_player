"""时间工具（仅负责时间转换/格式化）"""
import logging
from multimedia_player.constants.format_constants import TIME_DISPLAY_FORMAT

class TimeUtils:
    """时间工具类（单一职责：时间处理）"""
    @staticmethod
    def format_ms(ms: int) -> str:
        """将毫秒格式化为 HH:MM:SS,mmm"""
        if ms < 0:
            return "00:00:00,000"
        seconds = ms // 1000
        ms_remainder = ms % 1000
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return TIME_DISPLAY_FORMAT.format(
            hours=hours, minutes=minutes, secs=secs, ms_remainder=ms_remainder
        )

    @staticmethod
    def time_str_to_ms(time_str: str) -> int:
        """将时间字符串转换为毫秒"""
        try:
            if ',' in time_str:
                time_part, ms_part = time_str.split(',')
                ms = int(ms_part)
            else:
                time_part = time_str
                ms = 0
            h, m, s = map(int, time_part.split(':'))
            return h * 3600000 + m * 60000 + s * 1000 + ms
        except Exception as e:
            logging.error(f"【时间解析】解析失败 {time_str}: {str(e)}")
            return 0