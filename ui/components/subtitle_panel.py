"""字幕面板（仅字幕显示UI，适配PyQt6）"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QLabel,
    QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class SubtitlePanel(QWidget):
    """字幕显示面板（单一职责：展示字幕内容）"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        """初始化界面布局"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)

        # 标题
        title_label = QLabel("字幕内容")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # 字幕文本框
        self.subtitle_text = QTextEdit()
        self.subtitle_text.setReadOnly(True)
        # 修复：直接写样式，无依赖KeyError
        self.subtitle_text.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: #FFFFFF;
                font-family: Microsoft YaHei;
                font-size: 13px;
                padding: 8px;
                border: 1px solid #444444;
            }
        """)
        # PyQt6标准尺寸策略
        size_policy = QSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self.subtitle_text.setSizePolicy(size_policy)
        main_layout.addWidget(self.subtitle_text)

    def set_subtitle_content(self, content: str):
        """设置字幕内容"""
        self.subtitle_text.setPlainText(content)

    def clear_subtitle(self):
        """清空字幕"""
        self.subtitle_text.clear()