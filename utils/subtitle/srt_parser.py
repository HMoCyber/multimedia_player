"""SRT字幕解析器（仅处理SRT格式）"""
import re
from datetime import datetime
from multimedia_player.constants.format_constants import (
    SRT_PATTERN,
    SRT_TIME_FORMAT,
    SUPPORTED_SUBTITLE_FORMATS
)
from multimedia_player.utils.time_utils import TimeUtils
from multimedia_player.utils.subtitle.subtitle_base import SubtitleParserBase

class SRTParser(SubtitleParserBase):
    """SRT格式字幕解析器（继承基础解析器）"""

    @staticmethod
    def supports_extension(ext: str) -> bool:
        """判断是否支持该扩展名"""
        return ext.lower() in ("srt",)

    def parse(self, content: str) -> tuple[list[dict], str]:
        """
        解析SRT字幕内容
        :param content: 字幕文件的文本内容
        :return: (解析后的字幕列表, 原始内容)
        """
        if not content:
            return [], ""

        subtitles = []
        # 使用正则匹配所有SRT块
        matches = SRT_PATTERN.findall(content)
        for match in matches:
            try:
                # 解析匹配结果：序号、开始时间、结束时间、内容
                index = int(match[0])
                start_time_str = match[1]
                end_time_str = match[2]
                text = match[3].strip().replace("\r\n", "\n")  # 处理换行

                # 将SRT时间戳转换为毫秒（00:00:01,000 → 1000ms）
                start_ms = self._time_str_to_ms(start_time_str)
                end_ms = self._time_str_to_ms(end_time_str)

                # 构造字幕项
                subtitles.append({
                    "index": index,
                    "start_ms": start_ms,
                    "end_ms": end_ms,
                    "text": text
                })
            except (ValueError, IndexError) as e:
                # 忽略解析失败的条目，不中断整体解析
                continue

        return subtitles, content

    @staticmethod
    def _time_str_to_ms(time_str: str) -> int:
        """将SRT时间戳（00:00:01,000）转换为毫秒"""
        try:
            # 替换逗号为点，适配datetime解析（%f匹配微秒）
            time_str = time_str.replace(",", ".")
            dt = datetime.strptime(time_str, SRT_TIME_FORMAT)
            # 计算总毫秒：时*3600000 + 分*60000 + 秒*1000 + 毫秒
            total_ms = (
                dt.hour * 3600000 +
                dt.minute * 60000 +
                dt.second * 1000 +
                int(dt.microsecond / 1000)  # 微秒转毫秒
            )
            return total_ms
        except ValueError:
            # 解析失败返回0
            return 0