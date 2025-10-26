from app.models.video_config import SubtitleStyle


class SubtitleRenderer:
    def __init__(self, style: SubtitleStyle):
        self.style = style
    
    def build_drawtext_filter(self, text: str, font_path: str = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc") -> str:
        # 处理None或空字符串的情况
        if not text:
            text = ""
        escaped_text = self.escape_text(text)
        
        font_size = self.style.font_size
        color = self.style.color
        position = self.style.position
        border_width = self.style.border_width
        border_color = self.style.border_color
        
        if position == "bottom":
            y = f"h-{font_size*2}"
        elif position == "top":
            y = str(font_size)
        else:
            y = "(h-text_h)/2"
        
        filter_str = (
            f"drawtext=text='{escaped_text}':"
            f"fontfile={font_path}:"
            f"fontsize={font_size}:"
            f"fontcolor={color}:"
            f"x=(w-text_w)/2:"
            f"y={y}:"
            f"borderw={border_width}:"
            f"bordercolor={border_color}"
        )
        
        return filter_str
    
    def escape_text(self, text: str) -> str:
        if not text:
            return ""
        text = text.replace("'", "\\'")
        text = text.replace(":", "\\:")
        text = text.replace(",", "\\,")
        return text


subtitle_renderer = SubtitleRenderer(SubtitleStyle())
