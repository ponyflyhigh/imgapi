from PIL import Image
import os

def convert_to_png(input_path, output_path=None, overwrite=False, keep_animation=False, verbose=True):
    """
    将任意图片格式转换为PNG格式
    
    参数:
        input_path: 输入图片路径
        output_path: 输出PNG路径，默认为输入路径替换扩展名
        overwrite: 是否覆盖已存在的输出文件
        keep_animation: 是否保留GIF动画（拆分为多帧PNG）
        verbose: 是否显示详细信息
    """
    # 检查输入文件是否存在
    if not os.path.exists(input_path):
        if verbose:
            print(f"错误: 文件 '{input_path}' 不存在")
        return False
    
    # 检查输入文件是否为目录
    if os.path.isdir(input_path):
        if verbose:
            print(f"错误: '{input_path}' 是一个目录，需要输入文件路径")
        return False
    
    # 自动生成输出路径（如果未指定）
    if not output_path:
        base_name, _ = os.path.splitext(input_path)
        output_path = f"{base_name}.png"
    
    # 检查输出文件是否已存在
    if os.path.exists(output_path) and not overwrite:
        if verbose:
            print(f"跳过: 文件 '{output_path}' 已存在")
        return False
    
    try:
        # 打开图片
        img = Image.open(input_path)
        
        # 获取图片格式（转换为小写）
        input_format = (img.format or "").lower()
        
        # 处理不同格式的特殊情况
        if input_format == 'gif':
            if keep_animation:
                # 保留动画：将每一帧保存为单独的PNG
                output_dir = os.path.splitext(output_path)[0]
                os.makedirs(output_dir, exist_ok=True)
                
                frames = []
                try:
                    while True:
                        frames.append(img.copy())
                        img.seek(len(frames))  # 移动到下一帧
                except EOFError:
                    pass  # 所有帧处理完毕
                
                for i, frame in enumerate(frames):
                    frame_path = os.path.join(output_dir, f"frame_{i:03d}.png")
                    frame.save(frame_path, "PNG")
                
                if verbose:
                    print(f"成功将GIF拆分为 {len(frames)} 帧PNG，保存在 '{output_dir}'")
                return True
            else:
                # 不保留动画：只保存第一帧
                img = img.convert("RGBA")  # 确保支持透明度
        
        elif input_format in ['jpg', 'jpeg', 'webp', 'bmp']:
            # 这些格式可能需要转换为RGBA以保留透明度信息
            img = img.convert("RGBA")
        
        elif input_format == 'png':
            # PNG已经是PNG格式，但可能需要转换模式
            if img.mode not in ['RGBA', 'LA']:
                img = img.convert("RGBA")
        
        elif input_format == 'tiff':
            # TIFF格式可能有多种模式，统一转换为RGBA
            img = img.convert("RGBA")
        
        elif input_format == 'ico':
            # 图标文件通常有多个尺寸，选择最大的一个
            sizes = img.info.get('sizes', [])
            if sizes:
                largest_size = max(sizes, key=lambda s: s[0] * s[1])
                img = img.resize(largest_size)
            img = img.convert("RGBA")
        
        else:
            # 其他格式默认转换为RGBA
            if verbose:
                print(f"警告: 未知格式 '{input_format}'，将尝试转换为RGBA")
            img = img.convert("RGBA")
        
        # 保存为PNG
        img.save(output_path, "PNG")
        
        if verbose:
            print(f"成功将 '{input_path}' ({input_format}) 转换为 '{output_path}'")
        return True
    
    except Exception as e:
        if verbose:
            print(f"转换失败: {e}")
        return False

# 示例用法
if __name__ == "__main__":
    # 转换BMP到PNG
    convert_to_png(r"tmp\photo_invert\test.gif",'photo1.png')
    
    # 转换TIFF到PNG
    convert_to_png(r"tmp\photo_invert\test.jpg", "photo2.png")
    
    # 转换ICO到PNG
    convert_to_png(r"tmp\photo_invert\test.bmp", "photo3.png")
    
    convert_to_png(r"tmp\photo_invert\test.svg", "photo4.png")

    convert_to_png(r"tmp\photo_invert\test.webp", "photo5.png")

    convert_to_png(r"tmp\photo_invert\test.tiff", "photo6.png")
