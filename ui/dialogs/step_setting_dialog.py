"""步长设置对话框（仅步长设置逻辑/布局）"""
from PyQt6.QtWidgets import QFormLayout, QSpinBox, QDialogButtonBox
from multimedia_player.ui.dialogs.dialog_base import DialogBase
from multimedia_player.constants.app_constants import DEFAULT_STEP_SECONDS

class StepSettingDialog(DialogBase):
    """步长设置对话框（单一职责：设置进度步长）"""
    def __init__(self, current_step: int = DEFAULT_STEP_SECONDS, parent=None):
        super().__init__("自定义进度调整步长", parent)
        self.current_step = current_step
        self.step_spin = None
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化UI（仅布局）"""
        self.set_fixed_size(300, 150)
        layout = QFormLayout()
        self.setLayout(layout)

        # 步长选择器
        self.step_spin = QSpinBox()
        self.step_spin.setRange(1, 60)
        self.step_spin.setValue(self.current_step)
        self.step_spin.setSuffix(" 秒")
        layout.addRow("进度调整步长：", self.step_spin)

        # 按钮
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            Qt.Orientation.Horizontal, self
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_step(self) -> int:
        """获取设置的步长（仅取值）"""
        return self.step_spin.value() if self.step_spin else DEFAULT_STEP_SECONDS