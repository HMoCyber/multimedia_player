"""日志面板（仅显示日志UI，适配PyQt6）"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QLabel,
    QSizePolicy
)
from PyQt6.QtCore import Qt
from multimedia_player.logger.standard_logger import StandardLogger

class LogPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.log_handler = StandardLogger()
        self._init_ui()
        self._bind_log()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # 标题
        title = QLabel("运行日志")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # 日志文本框
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #2C2C2C;
                color: #FFFFFF;
                font-family: Consolas;
                font-size: 12px;
                padding: 5px;
                border: 1px solid #444444;
            }
        """)
        # PyQt6标准尺寸策略
        log_policy = QSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self.log_text.setSizePolicy(log_policy)
        layout.addWidget(self.log_text)

    def _bind_log(self):
        """绑定日志信号"""
        def append_log(msg):
            self.log_text.append(msg)
            self.log_text.verticalScrollBar().setValue(
                self.log_text.verticalScrollBar().maximum()
            )
        self.log_handler.get_log_signal().connect(append_log)

    def get_log_handler(self):
        """获取日志处理器"""
        return self.log_handler