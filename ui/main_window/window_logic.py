"""主窗口业务逻辑（仅逻辑，无UI/事件）"""
import logging
import os
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtCore import Qt  # 补充Qt Key常量导入
# 正确导入项目内的工具类（核心修复）
from multimedia_player.utils.time_utils import TimeUtils
from multimedia_player.ui.dialogs.step_setting_dialog import StepSettingDialog
from multimedia_player.ui.dialogs.resolution_setting_dialog import ResolutionSettingDialog
from multimedia_player.utils.path_utils import PathUtils
from multimedia_player.utils.file_utils import FileUtils
from multimedia_player.utils.subtitle import get_subtitle_parser
from multimedia_player.constants.app_constants import DEFAULT_RESOLUTION, MIN_WINDOW_SIZE
from multimedia_player.constants.style_constants import COLORS

class WindowLogic:
    """主窗口业务逻辑（单一职责：处理业务逻辑）"""
    def __init__(self, main_window, ui_layout, config_manager, media_core):
        self.main_window = main_window
        self.ui_layout = ui_layout  # 已同步改为ui_layout（避免和内置方法冲突）
        self.config_manager = config_manager
        self.media_core = media_core
        self.subtitles = []
        self.subtitle_raw_content = ""
        self.current_subtitle_index = -1

    # ========== 目录/文件逻辑 ==========
    def handle_file_selection(self, file_path: str) -> None:
        """处理文件选择（仅逻辑）"""
        if not PathUtils.is_path_valid(file_path):
            logging.warning(f"【文件操作】文件无效: {file_path}")
            return

        ext = PathUtils.get_file_extension(file_path)
        if FileUtils.is_media_file(file_path):
            self._load_media_file(file_path)
        elif FileUtils.is_subtitle_file(file_path) and self.media_core.current_media_path:
            self._load_subtitle_file(file_path)

    def _load_media_file(self, file_path: str) -> None:
        """加载媒体文件（仅逻辑）"""
        file_name = PathUtils.get_file_name(file_path)
        file_size = PathUtils.get_file_size_mb(file_path) or 0.0

        logging.info(
            f"【播放逻辑】加载媒体 | 文件名: {file_name} | "
            f"大小: {file_size:.2f}MB | 路径: {file_path}"
        )

        # 重置字幕状态
        self._reset_subtitle_state()
        # 加载媒体到核心
        self.media_core.load_media(file_path)
        # 启用控制栏
        self.ui_layout.media_control_bar.enable_controls(True)

    def _load_subtitle_file(self, file_path: str) -> None:
        """加载字幕文件（仅逻辑）"""
        try:
            # 获取解析器
            ext = PathUtils.get_file_extension(file_path)
            parser = get_subtitle_parser(ext)
            if not parser:
                logging.error(f"【字幕逻辑】不支持的字幕格式: {ext}")
                QMessageBox.critical(
                    self.main_window, "字幕错误",
                    f"不支持的字幕格式：{ext}"
                )
                return

            # 读取文件内容
            content = FileUtils.read_file_content(file_path)
            # 解析字幕
            self.subtitles, self.subtitle_raw_content = parser.parse(content)

            # 更新UI（通过回调）
            self.ui_layout.subtitle_panel.set_subtitle_content(self.subtitle_raw_content)
            logging.info(
                f"【字幕逻辑】解析完成 | 文件名: {PathUtils.get_file_name(file_path)} | "
                f"字幕条数: {len(self.subtitles)}"
            )
            QMessageBox.information(
                self.main_window, "字幕加载成功",
                f"成功加载字幕文件：\n{PathUtils.get_file_name(file_path)}\n共解析出 {len(self.subtitles)} 条字幕"
            )

        except Exception as e:
            logging.error(f"【字幕逻辑】加载失败: {str(e)}")
            QMessageBox.critical(
                self.main_window, "字幕加载失败",
                f"加载字幕失败：\n{str(e)}\n请检查文件格式和编码"
            )

    def _reset_subtitle_state(self) -> None:
        """重置字幕状态（仅逻辑）"""
        self.subtitles = []
        self.subtitle_raw_content = ""
        self.current_subtitle_index = -1
        self.ui_layout.subtitle_panel.clear_subtitle()
        self.ui_layout.video_playback_panel.clear_subtitle()

    # ========== 设置项逻辑 ==========
    def handle_step_setting(self) -> None:
        """处理步长设置（仅逻辑）"""
        current_step = self.config_manager.get_step_seconds()
        dialog = StepSettingDialog(current_step, self.main_window)
        if dialog.exec():
            new_step = dialog.get_step()
            old_step = current_step
            # 更新配置
            self.config_manager.set_step_seconds(new_step)
            # 更新控制栏
            self.ui_layout.media_control_bar.set_step_seconds(new_step)
            # 日志
            logging.info(f"【设置逻辑】更新步长 | 旧值: {old_step}秒 | 新值: {new_step}秒")
            QMessageBox.information(
                self.main_window, "步长设置成功",
                f"进度调整步长已设置为 {new_step} 秒！\n快捷键：←/A 后退，→/D 前进"
            )

    def handle_resolution_setting(self) -> None:
        """处理分辨率设置（仅逻辑）"""
        current_res = self.config_manager.get_resolution()
        screen_res = (
            self.main_window.screen.geometry().width(),
            self.main_window.screen.geometry().height()
        )
        dialog = ResolutionSettingDialog(
            self.main_window, current_res, screen_res
        )
        if dialog.exec():
            new_width, new_height = dialog.get_resolution()
            old_width, old_height = current_res
            # 验证最小尺寸
            new_width = max(new_width, MIN_WINDOW_SIZE[0])
            new_height = max(new_height, MIN_WINDOW_SIZE[1])
            # 更新配置
            self.config_manager.set_resolution(new_width, new_height)
            # 更新窗口大小
            self.main_window.resize(new_width, new_height)
            self.main_window.setWindowTitle(
                f"多媒体播放器 v1.0 - {new_width}x{new_height}"
            )
            # 日志
            logging.info(
                f"【设置逻辑】更新分辨率 | 旧值: {old_width}x{old_height} | "
                f"新值: {new_width}x{new_height}"
            )
            QMessageBox.information(
                self.main_window, "分辨率设置成功",
                f"播放器分辨率已设置为 {new_width}x{new_height}！"
            )

    def handle_reset_settings(self) -> None:
        """处理重置设置（仅逻辑）"""
        reply = QMessageBox.question(
            self.main_window, "确认重置",
            "是否要将所有设置重置为默认值？\n"
            "- 窗口置顶：开启\n"
            "- 进度步长：10秒\n"
            "- 分辨率：1000x800\n"
            "- 清空最后选择的目录",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            # 记录旧值
            old_topmost = self.config_manager.get_topmost()
            old_step = self.config_manager.get_step_seconds()
            old_res = self.config_manager.get_resolution()
            old_dir = self.config_manager.get_last_directory()

            # 重置配置
            self.config_manager.update_section("General", {
                "step_seconds": 10,
                "topmost": "True",
                "width": DEFAULT_RESOLUTION[0],
                "height": DEFAULT_RESOLUTION[1],
                "last_directory": ""
            })

            # 更新UI状态
            self.main_window.set_window_topmost(True)
            self.ui_layout.video_playback_panel.cb_topmost.setChecked(True)
            self.ui_layout.media_control_bar.set_step_seconds(10)
            self.main_window.resize(*DEFAULT_RESOLUTION)
            self.main_window.setWindowTitle(
                f"多媒体播放器 v1.0 - {DEFAULT_RESOLUTION[0]}x{DEFAULT_RESOLUTION[1]}"
            )
            self.ui_layout.file_tree_panel.lbl_current_dir.setText("未选择目录")
            self.ui_layout.file_tree_panel.file_tree.clear()

            # 日志
            logging.info(f"""【设置逻辑】重置所有设置 | 
  置顶状态: {old_topmost} → True | 
  进度步长: {old_step}秒 → 10秒 | 
  分辨率: {old_res[0]}x{old_res[1]} → {DEFAULT_RESOLUTION[0]}x{DEFAULT_RESOLUTION[1]} | 
  工作目录: {old_dir or '无'} → 清空""")
            QMessageBox.information(
                self.main_window, "重置成功",
                "所有设置已重置为默认值！"
            )

    # ========== 字幕显示逻辑 ==========
    def update_subtitle_display(self, current_ms: int) -> None:
        """更新字幕显示（仅逻辑）"""
        if not self.subtitles:
            self.ui_layout.video_playback_panel.clear_subtitle()
            return

        current_sub = None
        for idx, sub in enumerate(self.subtitles):
            if sub['start'] <= current_ms <= sub['end']:
                current_sub = sub
                self.current_subtitle_index = idx
                break

        if current_sub:
            self.ui_layout.video_playback_panel.update_subtitle_display(current_sub['text'])
        elif self.current_subtitle_index != -1:
            self.ui_layout.video_playback_panel.clear_subtitle()
            self.current_subtitle_index = -1

    # ========== 快捷键逻辑 ==========
    def handle_shortcut(self, key_event) -> bool:
        """处理快捷键（仅逻辑，返回是否处理）"""
        if not self.media_core.current_media_path or self.media_core.media_player.duration() == 0:
            return False

        step_seconds = self.config_manager.get_step_seconds()
        step_ms = step_seconds * 1000
        current_pos = self.media_core.media_player.position()
        max_pos = self.media_core.media_player.duration()

        # 后退
        if key_event.key() in (Qt.Key.Key_Left, Qt.Key.Key_A):
            new_pos = max(0, current_pos - step_ms)
            self.media_core.set_position(new_pos)
            logging.info(
                f"【快捷键逻辑】进度后退 {step_seconds} 秒 | "
                f"从 {TimeUtils.format_ms(current_pos)} 至 {TimeUtils.format_ms(new_pos)}"
            )
            return True
        # 前进
        elif key_event.key() in (Qt.Key.Key_Right, Qt.Key.Key_D):
            new_pos = min(max_pos, current_pos + step_ms)
            self.media_core.set_position(new_pos)
            logging.info(
                f"【快捷键逻辑】进度前进 {step_seconds} 秒 | "
                f"从 {TimeUtils.format_ms(current_pos)} 至 {TimeUtils.format_ms(new_pos)}"
            )
            return True
        # 播放/暂停
        elif key_event.key() == Qt.Key.Key_Space:
            if self.media_core.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
                self.media_core.pause()
            else:
                self.media_core.play()
            return True

        return False