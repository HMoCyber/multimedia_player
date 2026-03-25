"""字幕管理（预留拓展：统一管理字幕显示/切换/样式）"""
import logging
from typing import List, Dict


class SubtitleManager:
    """字幕管理器（单一职责：处理字幕逻辑，预留拓展）"""

    def __init__(self):
        self.subtitles: List[Dict] = []
        self.current_subtitle_index = -1
        self.subtitle_style = {
            "font_size": 18,
            "color": "white",
            "background": "rgba(0,0,0,0.7)"
        }
        logging.info("【字幕管理】初始化完成（预留功能）")

    def load_subtitles(self, subtitles: List[Dict]) -> None:
        """加载字幕列表（预留）"""
        self.subtitles = subtitles
        self.current_subtitle_index = -1
        logging.info(f"【字幕管理】加载字幕 | 条数: {len(subtitles)}")

    def get_current_subtitle(self, current_ms: int) -> str:
        """获取当前时间点的字幕（预留）"""
        if not self.subtitles:
            return ""

        current_sub = None
        for idx, sub in enumerate(self.subtitles):
            if sub['start'] <= current_ms <= sub['end']:
                current_sub = sub
                self.current_subtitle_index = idx
                break

        return current_sub['text'] if current_sub else ""

    def set_subtitle_style(self, style: Dict) -> None:
        """设置字幕样式（预留）"""
        self.subtitle_style.update(style)
        logging.info(f"【字幕管理】更新字幕样式 | 样式: {style}")