"""对话框基类（仅通用对话框逻辑）"""
from PyQt6.QtWidgets import QDialog, QWidget
from PyQt6.QtCore import Qt

class DialogBase(QDialog):
    """对话框基类（单一职责：通用对话框配置）"""
    def __init__(self, title: str, parent: QWidget = None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)  # 模态对话框
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)  # 移除帮助按钮

    def set_fixed_size(self, width: int, height: int) -> None:
        """设置固定大小"""
        self.setFixedSize(width, height)