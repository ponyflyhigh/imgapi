import requests

def test_photo_resize(local_image_path, min_dim=512, max_dim=4096):
    """
    测试图片缩放API（上传本地图片）
    
    参数:
        local_image_path: 本地图片路径
        min_dim: 最小尺寸
        max_dim: 最大尺寸
    """
    api_url = "http://localhost:5000/utils/photo_resize"
    
    try:
        # 读取本地图片并上传
        with open(local_image_path, 'rb') as f:
            response = requests.post(
                api_url,
                files={'image': f},
                data={'min_dim': min_dim, 'max_dim': max_dim}
            )
        
        # 解析响应
        result = response.json()
        
        if response.status_code == 200 and result.get('success'):
            print("测试成功:")
            print(f"原始尺寸: {result['original_size']}")
            print(f"处理后尺寸: {result['resized_size']}")
            return True
        else:
            print(f"测试失败: {result.get('error', '未知错误')}")
            return False
    
    except FileNotFoundError:
        print(f"错误: 本地图片不存在 - {local_image_path}")
        return False
    except Exception as e:
        print(f"测试出错: {str(e)}")
        return False




# 测试示例
if __name__ == "__main__":
    # 替换为你的本地图片路径
    test_image = r"C:\Users\86132\Desktop\副业\imgapi-master\tmp\photo_invert\test.png"
    
    # 执行测试
    test_photo_resize(test_image)
    
    # 测试不同尺寸参数
    # test_photo_resize(test_image, min_dim=300, max_dim=1024)