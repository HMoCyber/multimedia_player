"""深色样式表（仅样式表字符串，无逻辑）"""
from multimedia_player.constants.style_constants import COLORS, STYLE_TEMPLATES

# 组件样式表
STYLESHEETS = {
    "main_window": f"QMainWindow {{ background-color: {COLORS['main_bg']}; }}",
    "splitter": f"QSplitter {{ background-color: {COLORS['main_bg']}; }}",
    "splitter_handle": f"QSplitter::handle {{ background-color: {COLORS['border']}; }}",
    "push_button": f"""
        QPushButton {{
            background-color: {COLORS['border']};
            color: {COLORS['text']};
            border: none;
            padding: 5px;
        }}
        QPushButton:hover {{
            background-color: {COLORS['highlight']};
        }}
    """,
    "checkbox": f"QCheckBox {{ color: {COLORS['text']}; }}",
    "label": f"QLabel {{ color: {COLORS['text']}; }}",
    "tree_widget": f"""
        QTreeWidget {{
            background-color: {COLORS['main_bg']};
            color: {COLORS['text']};
            border: 1px solid {COLORS['border']};
        }}
        QTreeWidget::item {{ padding: 2px; }}
        QTreeWidget::item:selected {{ background-color: {COLORS['highlight']}; }}
        QHeaderView::section {{
            background-color: {COLORS['border']};
            color: {COLORS['text']};
            border: 1px solid {COLORS['border']};
        }}
    """,
    "subtitle_label": f"""
        QLabel {{
            background-color: {COLORS['subtitle_bg']};
            color: white;
            font-size: 18pt;
            padding: 8px;
            border-radius: 3px;
            margin: 0;
        }}
    """,
    "video_widget": f"QVideoWidget {{ border: 1px solid {COLORS['border']}; background-color: #000; }}",
    "slider_groove": STYLE_TEMPLATES["slider_groove"].format(border=COLORS['border']),
    "slider_handle": STYLE_TEMPLATES["slider_handle"].format(highlight=COLORS['highlight'])
}

def get_slider_style() -> str:
    """获取滑块样式表"""
    return f"{STYLESHEETS['slider_groove']}\n{STYLESHEETS['slider_handle']}"