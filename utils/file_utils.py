"""文件工具（仅负责文件基础操作）"""
import os
from typing import List, Tuple
from multimedia_player.constants.format_constants import (
    SUPPORTED_MEDIA_FORMATS, SUPPORTED_SUBTITLE_FORMATS
)
from multimedia_player.utils.path_utils import PathUtils

class FileUtils:
    """文件工具类（单一职责：文件基础操作）"""
    @staticmethod
    def is_media_file(file_path: str) -> bool:
        """判断是否为媒体文件"""
        ext = PathUtils.get_file_extension(file_path)
        return ext in SUPPORTED_MEDIA_FORMATS

    @staticmethod
    def is_subtitle_file(file_path: str) -> bool:
        """判断是否为字幕文件"""
        ext = PathUtils.get_file_extension(file_path)
        return ext in SUPPORTED_SUBTITLE_FORMATS

    @staticmethod
    def read_file_content(file_path: str, encoding: str = "utf-8") -> str:
        """读取文件内容"""
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except Exception as e:
            raise RuntimeError(f"读取文件失败: {str(e)}")

    @staticmethod
    def filter_files_by_type(file_paths: List[str], media: bool = True, subtitle: bool = True) -> List[str]:
        """按类型过滤文件"""
        filtered = []
        for path in file_paths:
            if (media and FileUtils.is_media_file(path)) or (subtitle and FileUtils.is_subtitle_file(path)):
                filtered.append(path)
        return filtered