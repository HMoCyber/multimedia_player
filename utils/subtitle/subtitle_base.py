"""字幕解析器基类（定义统一接口）"""
from abc import ABC, abstractmethod

class SubtitleParserBase(ABC):
    """字幕解析器抽象基类（所有字幕解析器必须实现该接口）"""

    @staticmethod
    @abstractmethod
    def supports_extension(ext: str) -> bool:
        """判断是否支持指定的文件扩展名"""
        pass

    @abstractmethod
    def parse(self, content: str) -> tuple[list[dict], str]:
        """
        解析字幕内容
        :param content: 字幕文件的文本内容
        :return: (解析后的字幕列表, 原始内容)
        字幕列表项格式：{"index": 序号, "start_ms": 开始毫秒, "end_ms": 结束毫秒, "text": 字幕内容}
        """
        pass