# -*- coding: utf-8 -*-
# 引入依赖包
# pip install alibabacloud_imageseg20191230

import os
from urllib.request import urlopen
from alibabacloud_imageseg20191230.client import Client
from alibabacloud_imageseg20191230.models import SegmentCommonImageAdvanceRequest
from alibabacloud_tea_openapi.models import Config
from alibabacloud_tea_util.models import RuntimeOptions


def perform_image_segmentation(image_url):
    """
    执行图像抠图操作
    :param image_url: 输入图片的公网 URL
    :return: 包含处理结果或错误信息的字典
    """

    # 检查环境变量
    access_key_id = os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID')
    access_key_secret = os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
    if not access_key_id or not access_key_secret:
        return {"error": "缺少 ALIBABA_CLOUD_ACCESS_KEY_ID 或 ALIBABA_CLOUD_ACCESS_KEY_SECRET 环境变量"}

    # 构建客户端配置
    config = Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        endpoint='imageseg.cn-shanghai.aliyuncs.com',
        region_id='cn-shanghai'
    )

    try:
        # 下载图片
        print(f"正在下载图片: {image_url}")
        img = urlopen(image_url).read()

        # 构建请求对象
        request_obj = SegmentCommonImageAdvanceRequest()
        request_obj.image_urlobject = open("temp_image.jpg", "wb+")  # 临时写入文件
        request_obj.image_urlobject.write(img)
        request_obj.image_urlobject.seek(0)
        request_obj.return_form = 'crop'

        # 设置运行时选项
        runtime = RuntimeOptions()

        # 调用接口
        client = Client(config)
        print("正在调用图像分割接口...")
        response = client.segment_common_image_advance(request_obj, runtime)

        # 关闭临时文件流
        request_obj.image_urlobject.close()

     
        return {"status": "success", "result_url": str(response.body)}
      
    except Exception as error:
        return {
            "status": "error",
            "code": getattr(error, "code", None),
            "message": str(error)
        }