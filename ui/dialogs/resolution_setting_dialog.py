"""分辨率设置对话框（仅分辨率设置逻辑/布局）"""
from PyQt6.QtWidgets import (
    QVBoxLayout, QLabel, QGroupBox, QVBoxLayout, QComboBox,
    QFormLayout, QSpinBox, QDialogButtonBox, QMessageBox
)
from multimedia_player.ui.dialogs.dialog_base import DialogBase
from multimedia_player.constants.app_constants import BUILTIN_RESOLUTIONS
from multimedia_player.constants.style_constants import COLORS


class ResolutionSettingDialog(DialogBase):
    """分辨率设置对话框（单一职责：设置窗口分辨率）"""

    def __init__(self, parent=None, current_res=None, screen_res=None):
        super().__init__("自定义播放器分辨率", parent)
        self.screen_width, self.screen_height = screen_res
        self.current_width, self.current_height = current_res
        self.selected_width = self.current_width
        self.selected_height = self.current_height
        self.res_combo = None
        self.width_edit = None
        self.height_edit = None
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化UI（仅布局）"""
        self.set_fixed_size(400, 300)
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # 提示标签
        tip_label = QLabel(f"屏幕最大分辨率：{self.screen_width}x{self.screen_height}\n自定义分辨率不能超过此限制")
        tip_label.setStyleSheet(f"color: red; font-weight: bold;")
        main_layout.addWidget(tip_label)

        # 预设分辨率
        preset_group = QGroupBox("预设分辨率（点击选择）")
        preset_layout = QVBoxLayout()
        preset_group.setLayout(preset_layout)

        self.res_combo = QComboBox()
        self._fill_preset_resolutions()
        preset_layout.addWidget(self.res_combo)
        main_layout.addWidget(preset_group)

        # 自定义分辨率
        custom_group = QGroupBox("自定义分辨率")
        custom_layout = QFormLayout()
        custom_group.setLayout(custom_layout)

        self.width_edit = QSpinBox()
        self.width_edit.setRange(320, self.screen_width)
        self.width_edit.setValue(self.current_width)
        custom_layout.addRow("宽度 (像素)：", self.width_edit)

        self.height_edit = QSpinBox()
        self.height_edit.setRange(500, self.screen_height)
        self.height_edit.setValue(self.current_height)
        custom_layout.addRow("高度 (像素)：", self.height_edit)

        main_layout.addWidget(custom_group)

        # 按钮
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            Qt.Orientation.Horizontal, self
        )
        buttons.accepted.connect(self._validate_and_accept)
        buttons.rejected.connect(self.reject)
        main_layout.addWidget(buttons)

    def _fill_preset_resolutions(self) -> None:
        """填充预设分辨率（仅填充逻辑）"""
        valid_resolutions = []
        for w, h, name in BUILTIN_RESOLUTIONS:
            if w == 0 and h == 0:
                w = self.screen_width
                h = self.screen_height
                name = f"屏幕分辨率 ({w}x{h})"
            if w <= self.screen_width and h <= self.screen_height:
                valid_resolutions.append((w, h, name))
                self.res_combo.addItem(name, (w, h))

        # 选中当前分辨率
        for i, (w, h, _) in enumerate(valid_resolutions):
            if w == self.current_width and h == self.current_height:
                self.res_combo.setCurrentIndex(i)
                break

        self.res_combo.currentIndexChanged.connect(self._on_preset_selected)

    def _on_preset_selected(self, index: int) -> None:
        """选择预设分辨率（仅选择逻辑）"""
        w, h = self.res_combo.currentData()
        self.width_edit.setValue(w)
        self.height_edit.setValue(h)

    def _validate_and_accept(self) -> None:
        """验证并确认（仅验证逻辑）"""
        w = self.width_edit.value()
        h = self.height_edit.value()
        if w > self.screen_width or h > self.screen_height:
            QMessageBox.warning(self, "警告", f"分辨率不能超过屏幕最大分辨率 {self.screen_width}x{self.screen_height}")
            return
        self.selected_width = w
        self.selected_height = h
        self.accept()

    def get_resolution(self) -> tuple:
        """获取选中的分辨率（仅取值）"""
        return (self.selected_width, self.selected_height)