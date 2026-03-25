"""文件树面板（显示文件列表，发射文件选择信号）"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem,
    QSizePolicy, QHeaderView
)
from PyQt6.QtCore import pyqtSignal, Qt
from multimedia_player.config.config_manager import ConfigManager
import os

class FileTreePanel(QWidget):
    # 核心：定义文件选择信号（修复报错的关键！）
    file_selected = pyqtSignal(str)

    def __init__(self, config_manager: ConfigManager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self._init_ui()

    def _init_ui(self):
        """初始化UI布局"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 文件树控件
        self.file_tree = QTreeWidget()
        self.file_tree.setHeaderHidden(True)
        self.file_tree.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        # 绑定选中事件
        self.file_tree.itemClicked.connect(self._on_item_clicked)

        layout.addWidget(self.file_tree)
        # 加载默认目录
        self._load_default_directory()

    def _load_default_directory(self):
        """加载默认目录（简易实现）"""
        root_item = QTreeWidgetItem(self.file_tree)
        root_item.setText(0, "媒体文件")
        root_item.setExpanded(True)

    def _on_item_clicked(self, item: QTreeWidgetItem, column: int):
        """文件项点击事件，发射信号"""
        # 模拟文件路径（实际可扩展为真实文件路径）
        file_name = item.text(0)
        if file_name and file_name != "媒体文件":
            # 发射文件选择信号（修复核心）
            self.file_selected.emit(file_name)