import os
import requests
from pathlib import Path
import json
from PIL import Image

def get_upload_policy(api_key, model_name):
    url = "https://dashscope.aliyuncs.com/api/v1/uploads"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    params = {"action": "getPolicy", "model": model_name}
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"获取上传凭证失败：{response.text}")
    return response.json()['data']

def upload_file_to_oss(policy_data, file_path):
    file_name = Path(file_path).name
    key = f"{policy_data['upload_dir']}/{file_name}"
    
    with open(file_path, 'rb') as file:
        files = {
            'OSSAccessKeyId': (None, policy_data['oss_access_key_id']),
            'Signature': (None, policy_data['signature']),
            'policy': (None, policy_data['policy']),
            'x-oss-object-acl': (None, policy_data['x_oss_object_acl']),
            'x-oss-forbid-overwrite': (None, policy_data['x_oss_forbid_overwrite']),
            'key': (None, key),
            'success_action_status': (None, '200'),
            'file': (file_name, file)
        }
        
        response = requests.post(policy_data['upload_host'], files=files)
        if response.status_code != 200:
            raise Exception(f"文件上传失败：{response.text}")
    return f"oss://{key}"

def check_image_size(image_path, min_dim=512, max_dim=4096):
    """校验图片尺寸并打印信息"""
    with Image.open(image_path) as img:
        width, height = img.size
        print(f"校验图片：{image_path}，尺寸：{width}px (宽) × {height}px (高)")
        
        if not (min_dim <= width <= max_dim and min_dim <= height <= max_dim):
            raise ValueError(
                f"尺寸不符合要求（需宽高均在 {min_dim}-{max_dim}px 之间）"
            )
        print("✅ 尺寸校验通过")
        return True

def resize_image_if_needed(image_path, min_dim=512, max_dim=4096):
    """强制调整图片尺寸，确保宽高均在 [min_dim, max_dim] 范围内"""
    with Image.open(image_path) as img:
        width, height = img.size
        print(f"原始尺寸：{width}px × {height}px")

        # 计算缩放比例：确保宽和高均 >= min_dim 且 <= max_dim
        # 情况1：宽度或高度小于最小值 → 放大
        # 情况2：宽度或高度大于最大值 → 缩小
        scale_width_min = min_dim / width  # 满足最小宽度的缩放比例
        scale_height_min = min_dim / height  # 满足最小高度的缩放比例
        scale_min = max(scale_width_min, scale_height_min)  # 取较大值确保宽高均达标

        scale_width_max = max_dim / width  # 满足最大宽度的缩放比例
        scale_height_max = max_dim / height  # 满足最大高度的缩放比例
        scale_max = min(scale_width_max, scale_height_max)  # 取较小值确保宽高均不超标

        # 最终缩放比例：根据图片当前尺寸选择放大或缩小
        if width < min_dim or height < min_dim:
            # 图片过小，需要放大
            scale = scale_min
        elif width > max_dim or height > max_dim:
            # 图片过大，需要缩小
            scale = scale_max
        else:
            # 尺寸符合要求，无需调整
            print("✅ 尺寸符合要求，无需调整")
            return image_path

        # 计算新尺寸（四舍五入为整数）
        new_width = int(round(width * scale))
        new_height = int(round(height * scale))

        # 再次确保新尺寸在范围内（避免浮点计算误差）
        new_width = max(min_dim, min(new_width, max_dim))
        new_height = max(min_dim, min(new_height, max_dim))

        # 调整尺寸并保存
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        temp_path = Path(image_path).parent / f"resized_{Path(image_path).name}"
        resized_img.save(temp_path)
        print(f"🔄 已调整尺寸：{width}×{height}px → {new_width}×{new_height}px，保存至：{temp_path}")
        return str(temp_path)

def upload_images_in_directory(api_key, model_name, directory_path, auto_resize=True):
    policy_data = get_upload_policy(api_key, model_name)
    uploaded_files_info = {}
    
    for image_path in Path(directory_path).rglob('*'):
        if image_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']:
            try:
                print(f"\n===== 处理文件：{image_path} =====")
                # 强制调整尺寸（无论是否符合，都会检查并调整）
                processed_path = resize_image_if_needed(str(image_path))
                # 二次校验调整后的尺寸
                check_image_size(processed_path)
                # 上传调整后的文件
                public_url = upload_file_to_oss(policy_data, processed_path)
                uploaded_files_info[str(image_path.relative_to(directory_path))] = public_url
                print(f"📤 上传成功：{public_url}")
            except Exception as e:
                print(f"❌ 处理失败：{str(e)}")

    result_file = Path(directory_path) / "upload_results.json"
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(uploaded_files_info, f, indent=4)
    print(f"\n处理完成，结果保存至：{result_file}")
    return result_file

if __name__ == "__main__":
    api_key = os.getenv("DASHSCOPE_API_KEY")   
    model_name = "qwen-vl-plus"
    folder_path = r"C:\Users\pony\Desktop\mine\imgapi\tmp\changebg"
    
    try:
        upload_images_in_directory(api_key, model_name, folder_path, auto_resize=True)
    except Exception as e:
        print(f"程序错误：{str(e)}")