"""文件扫描器（仅负责目录扫描，无其他逻辑）"""
import os
from typing import Tuple, List, Dict
from multimedia_player.utils.path_utils import PathUtils
from multimedia_player.utils.file_utils import FileUtils

class FileScanner:
    """文件扫描器（单一职责：扫描目录中的媒体/字幕文件）"""
    @staticmethod
    def scan_directory(root_dir: str, media_checked: bool = True, subtitle_checked: bool = True) -> Tuple[List[str], List[Dict]]:
        """扫描目录（仅扫描逻辑）"""
        valid_dirs = []
        valid_files = []

        if not PathUtils.is_path_valid(root_dir):
            return valid_dirs, valid_files

        for dirpath, _, filenames in os.walk(root_dir):
            valid_dirs.append(dirpath)
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                # 过滤文件类型
                if (media_checked and FileUtils.is_media_file(file_path)) or \
                   (subtitle_checked and FileUtils.is_subtitle_file(file_path)):
                    valid_files.append({
                        'path': file_path,
                        'rel_path': PathUtils.get_relative_path(root_dir, file_path),
                        'name': PathUtils.get_file_name(file_path),
                        'ext': PathUtils.get_file_extension(file_path)
                    })

        return sorted(valid_dirs), valid_files

    @staticmethod
    def count_files_by_type(files: List[Dict]) -> Tuple[int, int]:
        """统计文件类型数量（仅统计逻辑）"""
        media_count = 0
        subtitle_count = 0
        for file in files:
            if file['ext'] in SUPPORTED_MEDIA_FORMATS:
                media_count += 1
            else:
                subtitle_count += 1
        return media_count, subtitle_count