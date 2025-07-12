from flask import Flask, request, jsonify
import api.changebg as changebg
import api.changecloth as changecloth
import api.expand as expand
import api.fix as fix
import api.koutu as koutu
import api.remove_watermark as remove_watermark
import tempfile
import os,json,requests
from api.utils.photo_revize import resize_image
from api.utils.photo_convert import convert_to_png
import base64


app = Flask(__name__)


@app.route('/change_bg', methods=['POST'])
def run_changebg():
    base_image_url = request.json.get('base_image_url')
    ref_image_url = request.json.get('ref_image_url')
    ref_prompt = request.json.get('ref_prompt', "")  # 可选参数，默认为空字符串
    n = request.json.get('n', 1)  # 可选参数，默认为1

    if not base_image_url or not ref_image_url:
        return jsonify({"error": "Missing image URLs"}), 400

    try:
        task_id = changebg.start_image_synthesis(base_image_url, ref_image_url, ref_prompt, n)
        result = changebg.poll_task_status(task_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/change_cloth', methods=['POST'])
def run_changecloth():
    top_garment_url = request.json.get('top_garment_url')
    bottom_garment_url = request.json.get('bottom_garment_url')
    person_image_url = request.json.get('person_image_url')
    if not all([top_garment_url, bottom_garment_url, person_image_url]):
        return jsonify({"error": "Missing garment or person image URLs"}), 400

    try:
        task_id = changecloth.start_image_synthesis(top_garment_url, bottom_garment_url, person_image_url)
        result = changecloth.poll_task_status(task_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/expand', methods=['POST'])
def run_expand():
    base_image_url = request.json.get('base_image_url')
    top_scale = request.json.get('top_scale', 1.5)
    bottom_scale = request.json.get('bottom_scale', 1.5)
    left_scale = request.json.get('left_scale', 1.5)
    right_scale = request.json.get('right_scale', 1.5)
    prompt = request.json.get('prompt', '按照原来图片背景来操作扩展')

    if not base_image_url:
        return jsonify({"error": "Missing base image URL"}), 400

    try:
        task_id = expand.start_image_synthesis(base_image_url, top_scale, bottom_scale, left_scale, right_scale, prompt)
        result = expand.poll_task_status(task_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/fix', methods=['POST'])
def run_fix():
    base_image_url = request.json.get('base_image_url')
    prompt = request.json.get('prompt', '图像超分。')

    if not base_image_url:
        return jsonify({"error": "Missing base image URL"}), 400

    try:
        task_id = fix.start_image_synthesis(base_image_url, prompt)
        result = fix.poll_task_status(task_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/remove_bg', methods=['POST'])
def run_koutu():
    image_url = request.json.get('image_url')
    if not image_url:
        return jsonify({"error": "Missing image URL"}), 400

    try:
        result = koutu.perform_image_segmentation(image_url)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@app.route('/remove_watermark', methods=['POST'])
def run_remove_watermark():
    image_url = request.json.get('image_url')
    if not image_url:
        return jsonify({"error": "Missing image URL"}), 400

    try:
        result = remove_watermark.perform_image_removal(image_url)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/utils/convert_to_png', methods=['POST'])
def api_convert_to_png():
    """图片格式转换API（上传本地图片，返回路径和Base64）"""
    # 获取上传的文件
    file = request.files.get('image')
    if not file:
        return jsonify({"error": "请上传图片文件"}), 400
    
    # 获取可选参数
    keep_animation = request.form.get('keep_animation', 'false').lower() == 'true'
    overwrite = request.form.get('overwrite', 'false').lower() == 'true'
    
    try:
        # 保存上传的本地图片到临时文件
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.' + file.filename.split('.')[-1])
        temp_path = temp_file.name
        file.save(temp_path)
        temp_file.close()
        
        # 生成输出路径（临时文件）
        output_path = os.path.splitext(temp_path)[0] + '.png'
        
        # 执行转换
        success, msg, input_format, output_format, image_paths = convert_to_png(
            temp_path,
            output_path,
            overwrite=overwrite,
            keep_animation=keep_animation
        )
        
        # 读取转换后的图片（Base64编码返回）
        image_data = None
        if success and image_paths:
            if len(image_paths) == 1:  # 单张图片
                with open(image_paths[0], 'rb') as f:
                    image_data = base64.b64encode(f.read()).decode('utf-8')
            else:  # 多张图片（GIF拆分）
                image_data = []
                for path in image_paths:
                    with open(path, 'rb') as f:
                        image_data.append(base64.b64encode(f.read()).decode('utf-8'))
        
        # 清理临时文件（但保留路径用于返回）
        os.unlink(temp_path)
        
        # 构造响应结果
        if success:
            return jsonify({
                "success": True,
                "message": msg,
                "original_format": input_format,  # 原始格式
                "converted_format": output_format,  # 转换后格式（固定为png）
                "image_paths": image_paths,  # 服务器上的临时文件路径（短期有效）
                "image_data": image_data  # 图片的Base64编码（直接可用）
            })
        else:
            # 清理可能生成的临时文件
            for path in image_paths:
                if os.path.exists(path):
                    os.unlink(path)
            return jsonify({"success": False, "error": msg}), 500
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


#云端url
@app.route('/utils/photo_resize_url', methods=['POST'])
def run_photo_resize_url():
    """调整图片尺寸API"""
    data = request.json
    image_url = data.get('image_url')
    min_dim = data.get('min_dim', 512)
    max_dim = data.get('max_dim', 4096)

    if not image_url:
        return jsonify({"error": "Missing image URL"}), 400

    try:
        # 下载图片
        response = requests.get(image_url)
        response.raise_for_status()  # 检查请求是否成功
        
        # 创建临时文件保存原始图片
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        temp_file.write(response.content)
        temp_file.close()
        
        # 调整图片尺寸
        output_path, in_w, in_h, out_w, out_h =resize_image(temp_file.name, min_dim, max_dim)

        # 读取调整后的图片并转换为Base64
        with open(output_path, 'rb') as f:
            import base64
            encoded_image = base64.b64encode(f.read()).decode('utf-8')
        
        # 清理临时文件
        os.unlink(temp_file.name)
        if output_path != temp_file.name:
            os.unlink(output_path)
        
        # 返回结果
        result = {
            "success": True,
            "original_size": f"{in_w}x{in_h}px",
            "resized_size": f"{out_w}x{out_h}px",
            "image_data": encoded_image  # Base64编码的图片数据
        }
        
        return jsonify(result)
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to download image: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Image processing error: {str(e)}"}), 500

@app.route('/utils/photo_resize', methods=['POST'])
def run_photo_resize():
    """支持本地图片上传的尺寸调整API"""
    # 接收上传的图片文件（替代原来的 image_url）
    file = request.files.get('image')  # 前端需用 'image' 字段上传文件
    min_dim = request.form.get('min_dim', 512, type=int)  # 从表单获取参数
    max_dim = request.form.get('max_dim', 4096, type=int)

    if not file:
        return jsonify({"error": "Missing image file"}), 400

    try:
        # 保存上传的文件到临时文件
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        temp_path = temp_file.name
        file.save(temp_path)  # 直接保存上传的文件内容
        temp_file.close()

        # 调用 resize_image 处理图片
        output_path, in_w, in_h, out_w, out_h = resize_image(temp_path, min_dim, max_dim)

        # 读取处理后的图片并转为 Base64 返回
        with open(output_path, 'rb') as f:
            encoded_image = base64.b64encode(f.read()).decode('utf-8')

        # 清理临时文件
        os.unlink(temp_path)
        if output_path != temp_path:
            os.unlink(output_path)

        return jsonify({
            "success": True,
            "original_size": f"{in_w}x{in_h}px",
            "resized_size": f"{out_w}x{out_h}px",
            "image_data": encoded_image
        })

    except Exception as e:
        return jsonify({"error": f"Processing failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000,host='0.0.0.0')