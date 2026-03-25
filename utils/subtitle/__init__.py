"""字幕解析器入口（统一获取解析器）"""
from multimedia_player.utils.subtitle.srt_parser import SRTParser
from multimedia_player.utils.subtitle.txt_parser import TXTParser
from multimedia_player.utils.subtitle.subtitle_base import SubtitleParserBase

# 注册所有支持的解析器
PARSER_MAP = {
    "srt": SRTParser(),
    "txt": TXTParser()
}

def get_subtitle_parser(ext: str) -> SubtitleParserBase | None:
    """
    根据文件扩展名获取对应的字幕解析器
    :param ext: 文件扩展名（如srt、txt）
    :return: 解析器实例，不支持则返回None
    """
    if not ext:
        return None
    # 转为小写，兼容大小写扩展名（如SRT、Txt）
    ext_lower = ext.lower().lstrip(".")
    return PARSER_MAP.get(ext_lower)