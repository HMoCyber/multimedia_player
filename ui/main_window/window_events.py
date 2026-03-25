"""主窗口事件绑定（仅处理UI交互事件，单一职责）"""
import logging
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox
from multimedia_player.ui.main_window.window_logic import WindowLogic
from multimedia_player.core.media.media_core import MediaCore

class WindowEvents:
    """主窗口事件管理器（统一绑定所有交互事件）"""
    def __init__(self, main_window, ui_layout, logic: WindowLogic, media_core: MediaCore):
        self.main_window = main_window  # 主窗口
        self.ui_layout = ui_layout      # 正确属性名：ui_layout（修复核心）
        self.logic = logic              # 业务逻辑
        self.media_core = media_core    # 媒体核心

        # 绑定所有事件
        self._bind_all_events()

    def _bind_all_events(self):
        """绑定所有UI交互事件（修复属性名 + 规范绑定）"""
        # 1. 窗口置顶复选框事件
        self.ui_layout.video_playback_panel.cb_topmost.toggled.connect(
            self.on_topmost_toggled
        )
        # 2. 文件树选择事件
        self.ui_layout.file_tree_panel.file_selected.connect(
            self.on_file_selected
        )
        # 3. 媒体播放状态监听
        self.media_core.media_player.playbackStateChanged.connect(
            self.on_playback_state_changed
        )
        # 4. 进度更新监听
        self.media_core.progress_manager.on_progress_updated = self.on_progress_updated

    def on_topmost_toggled(self, checked: bool):
        """窗口置顶复选框切换事件"""
        self.main_window.set_window_topmost(checked)
        self.main_window.config_manager.update_section("General", {"topmost": str(checked)})
        logging.info(f"【事件】窗口置顶: {'开启' if checked else '关闭'}")

    def on_file_selected(self, file_path: str):
        """文件树选择文件事件"""
        self.logic.handle_file_selection(file_path)

    def on_playback_state_changed(self, state):
        """播放状态变更事件"""
        state_map = {
            0: "停止",
            1: "播放",
            2: "暂停"
        }
        logging.info(f"【事件】播放状态: {state_map.get(state, '未知')}")

    def on_progress_updated(self, current_ms: int):
        """播放进度更新事件"""
        self.logic.update_subtitle_display(current_ms)

    def on_step_setting(self):
        """步长设置菜单事件（预留）"""
        self.logic.handle_step_setting()

    def on_resolution_setting(self):
        """分辨率设置菜单事件（预留）"""
        self.logic.handle_resolution_setting()

    def on_reset_settings(self):
        """重置设置菜单事件（预留）"""
        self.logic.handle_reset_settings()