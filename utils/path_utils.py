"""路径工具类（处理文件路径、大小等）"""
import os
import math
from multimedia_player.constants.format_constants import FILE_SIZE_UNITS

class PathUtils:
    """路径处理工具类（静态方法）"""

    @staticmethod
    def is_path_valid(path: str) -> bool:
        """判断路径是否有效（存在且可访问）"""
        if not path:
            return False
        return os.path.exists(path)

    @staticmethod
    def get_file_extension(path: str) -> str:
        """获取文件扩展名（小写，不带点）"""
        if not path:
            return ""
        return os.path.splitext(path)[1].lower().lstrip(".")

    @staticmethod
    def get_file_name(path: str) -> str:
        """获取文件名（含扩展名）"""
        if not path:
            return ""
        return os.path.basename(path)

    @staticmethod
    def get_file_size_mb(path: str) -> float:
        """获取文件大小（MB，保留2位小数）"""
        if not PathUtils.is_path_valid(path) or not os.path.isfile(path):
            return 0.0
        # 获取字节数
        size_bytes = os.path.getsize(path)
        # 转换为MB
        size_mb = size_bytes / (1024 * 1024)
        return round(size_mb, 2)

    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """格式化文件大小（自动转换单位：B/KB/MB/GB）"""
        if size_bytes == 0:
            return "0 B"
        # 计算单位层级
        i = int(math.floor(math.log(size_bytes, 1024)))
        # 避免超出单位列表范围
        i = min(i, len(FILE_SIZE_UNITS) - 1)
        # 转换为对应单位
        size = size_bytes / (1024 **i)
        return f"{size:.2f} {FILE_SIZE_UNITS[i]}"