"""TXT字幕解析器（仅处理简单的TXT格式）"""
from multimedia_player.constants.format_constants import SUPPORTED_SUBTITLE_FORMATS
from multimedia_player.utils.subtitle.subtitle_base import SubtitleParserBase

class TXTParser(SubtitleParserBase):
    """TXT格式字幕解析器（简单按行解析，无时间戳时按播放进度均分）"""

    @staticmethod
    def supports_extension(ext: str) -> bool:
        """判断是否支持该扩展名"""
        return ext.lower() in ("txt",)

    def parse(self, content: str) -> tuple[list[dict], str]:
        """
        解析TXT字幕内容（简单按行分割，默认每行显示3秒）
        :param content: 字幕文件的文本内容
        :return: (解析后的字幕列表, 原始内容)
        """
        if not content:
            return [], ""

        subtitles = []
        # 按行分割，过滤空行
        lines = [line.strip() for line in content.split("\n") if line.strip()]
        # 每行字幕默认显示3秒（3000ms）
        default_duration = 3000

        for idx, line in enumerate(lines, 1):
            start_ms = (idx - 1) * default_duration
            end_ms = idx * default_duration
            subtitles.append({
                "index": idx,
                "start_ms": start_ms,
                "end_ms": end_ms,
                "text": line
            })

        return subtitles, content