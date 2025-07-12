from flask import Flask, request, jsonify
from PIL import Image
import requests
from io import BytesIO
import os
import tempfile

app = Flask(__name__)

def check_image_size(image_path, min_dim=512, max_dim=4096):
    """校验图片尺寸"""
    with Image.open(image_path) as img:
        width, height = img.size
        valid = (min_dim <= width <= max_dim) and (min_dim <= height <= max_dim)
        return width, height, valid

def resize_image(image_path, min_dim=512, max_dim=4096):
    """调整图片尺寸"""
    input_width, input_height, is_valid = check_image_size(image_path, min_dim, max_dim)
    
    if is_valid:
        return image_path, input_width, input_height, input_width, input_height
    
    with Image.open(image_path) as img:
        # 计算缩放比例
        scale_width_min = min_dim / input_width
        scale_height_min = min_dim / input_height
        scale_min = max(scale_width_min, scale_height_min)

        scale_width_max = max_dim / input_width
        scale_height_max = max_dim / input_height
        scale_max = min(scale_width_max, scale_height_max)

        # 确定最终缩放比例
        if input_width < min_dim or input_height < min_dim:
            scale = scale_min
        else:
            scale = scale_max

        # 计算新尺寸
        new_width = int(round(input_width * scale))
        new_height = int(round(input_height * scale))
        new_width = max(min_dim, min(new_width, max_dim))
        new_height = max(min_dim, min(new_height, max_dim))

        # 调整尺寸并保存到临时文件
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        temp_path = temp_file.name
        resized_img.save(temp_path)
        
        return temp_path, input_width, input_height, new_width, new_height


if __name__ == '__main__':
    app.run(debug=True)