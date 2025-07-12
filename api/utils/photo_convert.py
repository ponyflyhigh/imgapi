from flask import Flask, request, jsonify
import os
import tempfile
import base64
from PIL import Image

app = Flask(__name__)

def convert_to_png(input_path, output_path=None, overwrite=False, keep_animation=False):
    """核心转换函数（复用原有逻辑）"""
    if not os.path.exists(input_path):
        return False, "文件不存在"
    
    if os.path.isdir(input_path):
        return False, "输入路径是目录"
    
    if not output_path:
        base_name, _ = os.path.splitext(input_path)
        output_path = f"{base_name}.png"
    
    if os.path.exists(output_path) and not overwrite:
        return False, "输出文件已存在"
    
    try:
        img = Image.open(input_path)
        input_format = (img.format or "").lower()  # 原始格式（小写）
        output_format = "png"  # 转换后格式固定为PNG
        
        # 处理不同格式
        if input_format == 'gif':
            if keep_animation:
                output_dir = os.path.splitext(output_path)[0]
                os.makedirs(output_dir, exist_ok=True)
                frames = []
                try:
                    while True:
                        frames.append(img.copy())
                        img.seek(len(frames))
                except EOFError:
                    pass
                frame_paths = []
                for i, frame in enumerate(frames):
                    frame_path = os.path.join(output_dir, f"frame_{i:03d}.png")
                    frame.save(frame_path, "PNG")
                    frame_paths.append(frame_path)
                return True, f"GIF拆分为{len(frames)}帧PNG", input_format, output_format, frame_paths
            else:
                img = img.convert("RGBA")
        
        elif input_format in ['jpg', 'jpeg', 'webp', 'bmp']:
            img = img.convert("RGBA")
        
        elif input_format == 'png':
            if img.mode not in ['RGBA', 'LA']:
                img = img.convert("RGBA")
        
        elif input_format in ['tiff', 'ico']:
            img = img.convert("RGBA")
        
        else:
            img = img.convert("RGBA")
        
        # 保存转换结果
        img.save(output_path, "PNG")
        return True, "转换成功", input_format, output_format, [output_path]
    
    except Exception as e:
        return False, str(e), None, None, []


if __name__ == '__main__':
    app.run(debug=True)