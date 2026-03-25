"""UI日志处理器（修复Qt生命周期错误，适配PyQt6）"""
import logging
from PyQt6.QtCore import Qt, pyqtSignal, QObject

class LogSignalEmitter(QObject):
    """独立的信号发射器（解决Qt对象生命周期问题）"""
    log_signal = pyqtSignal(str)

class StandardLogger(logging.Handler):
    """标准UI日志处理器（无多重继承冲突）"""
    def __init__(self):
        super().__init__()
        self.emitter = LogSignalEmitter()
        self.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s: %(message)s"))

    def emit(self, record):
        """发送日志信号到UI"""
        try:
            msg = self.format(record)
            self.emitter.log_signal.emit(msg)
        except Exception:
            pass

    def get_log_signal(self):
        """获取日志信号"""
        return self.emitter.log_signal