"""UI样式常量（纯数据，无逻辑）"""
# 字体配置
LOG_FONT_NAME = "Consolas"
LOG_FONT_SIZE = 9
LOG_LINE_HEIGHT = 16
LOG_MIN_LINES = 8
LOG_MIN_HEIGHT = LOG_MIN_LINES * LOG_LINE_HEIGHT

# 尺寸配置
CONTROL_BTN_SIZE = (32, 32)
VOLUME_SLIDER_WIDTH = 100
TIME_LABEL_WIDTH = 260
SUBTITLE_LABEL_HEIGHT = 50
SPLITTER_HANDLE_WIDTH = 2

# 颜色配置（深色主题）
COLORS = {
    "main_bg": "#333333",
    "log_bg": "#1e1e1e",
    "border": "#444444",
    "text": "#ffffff",
    "highlight": "#0078d7",
    "subtitle_bg": "rgba(0, 0, 0, 0.7)"
}

# 样式表模板（占位符）
STYLE_TEMPLATES = {
    "slider_groove": "QSlider::groove:horizontal {{ background: {border}; height: 4px; }}",
    "slider_handle": "QSlider::handle:horizontal {{ background: {highlight}; width: 12px; margin: -4px 0; border-radius: 6px; }}"
}