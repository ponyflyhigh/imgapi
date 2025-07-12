import os
from PIL import Image

def check_image_size(image_path, min_dim=512, max_dim=4096):
    """校验图片尺寸并返回结果"""
    with Image.open(image_path) as img:
        width, height = img.size
        valid = (min_dim <= width <= max_dim) and (min_dim <= height <= max_dim)
        return width, height, valid

def resize_image_if_needed(image_path, min_dim=512, max_dim=4096):
    """调整图片尺寸并返回处理后的路径"""
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

        # 调整尺寸并保存
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        temp_path = os.path.splitext(image_path)[0] + f"_resized.png"
        resized_img.save(temp_path)
        
        return temp_path, input_width, input_height, new_width, new_height

if __name__ == "__main__":
    # 测试用例：替换为你的图片路径
    test_images = [r"tmp\fixed\screenshot_2025-07-07_11-19-52.png"]
    
    for image_path in test_images:
        if not os.path.exists(image_path):
            print(f"❌ 测试图片不存在: {image_path}")
            continue
        
        print(f"\n=== 测试图片: {image_path} ===")
        output_path, in_w, in_h, out_w, out_h = resize_image_if_needed(image_path)
        
        if output_path == image_path:
            print(f"输入尺寸: {in_w}×{in_h}px → 无需调整")
        else:
            print(f"输入尺寸: {in_w}×{in_h}px → 输出尺寸: {out_w}×{out_h}px")
            print(f"调整后的图片: {output_path}")