"""程序入口（仅负责启动/退出，无业务逻辑）"""
import sys
import os
import shutil
import logging
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from multimedia_player.ui.main_window.main_window import MainWindow
from multimedia_player.logger.log_init import init_logging
from multimedia_player.constants.app_constants import TEMP_DIR

def main() -> None:
    """程序主入口（单一职责：启动应用）"""
    # 1. 初始化日志系统
    init_logging()

    # 2. 创建临时目录
    _create_temp_dir()

    # 3. 初始化Qt应用
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # 使用Fusion样式（跨平台一致）
    app.setApplicationName("多媒体播放器")
    app.setApplicationVersion("1.0.0")

    # 4. 创建主窗口
    window = MainWindow()
    window.show()

    # 5. 注册退出清理函数
    app.aboutToQuit.connect(_cleanup)

    # 6. 运行应用
    sys.exit(app.exec())

def _create_temp_dir() -> None:
    """创建临时目录（仅目录创建）"""
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
        logging.info(f"【程序入口】创建临时目录: {TEMP_DIR}")

def _cleanup() -> None:
    """退出清理（仅资源清理）"""
    # 删除临时目录
    try:
        if os.path.exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR)
            logging.info(f"【程序入口】清理临时目录: {TEMP_DIR}")
    except Exception as e:
        logging.warning(f"【程序入口】清理临时目录失败: {str(e)}")

    logging.info("【程序入口】播放器正常退出")

if __name__ == "__main__":
    # 确保项目根目录在Python路径中（解决导入问题）
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    main()