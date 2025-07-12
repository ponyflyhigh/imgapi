import requests
import json
import os
import time

# 设置API Key
api_key = os.getenv("DASHSCOPE_API_KEY")
if not api_key:
    raise Exception("请设置DASHSCOPE_API_KEY环境变量")

# 请求的URL
url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/background-generation/generation/'

# 请求头
headers = {
    'X-DashScope-Async': 'enable',
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
    'X-DashScope-OssResourceResolve': 'enable'
}

def start_image_synthesis(base_image_url, ref_image_url, ref_prompt="", n=1):
    """
    启动图像合成任务
    :param base_image_url: 基础图片 URL
    :param ref_image_url: 参考图片 URL
    :param ref_prompt: 参考提示，可选，默认为空字符串
    :param n: 生成图片的数量，可选，默认为1
    :return: task_id 或 None
    """
    data = {
        "model": "wanx-background-generation-v2",
        "input": {
            "base_image_url": base_image_url,
            "ref_image_url": ref_image_url,
            "ref_prompt": ref_prompt  # 使用传入的 ref_prompt 参数
        },
        "parameters": {
            "model_version": "v3",
            "n": n,  # 使用传入的 n 参数
            "noise_level": 300
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        response_json = response.json()
        task_id = response_json.get('output', {}).get('task_id')
        if task_id:
            print(f"任务ID: {task_id}")
            return task_id
        else:
            print("未找到任务ID")
            return None
    else:
        print(f"请求失败，状态码：{response.status_code}，响应内容：{response.text}")
        return None


def check_task_status(task_id):
    """
    查询任务状态
    :param task_id: 任务 ID
    :return: 任务结果或错误信息
    """
    task_url = f'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}'
    response = requests.get(task_url, headers=headers)
    
    if response.status_code == 200:
        response_json = response.json()
        status = response_json.get('status', '未知状态')
        print(f"任务状态: {status}")
        result = response_json.get('output', {})
        print(f"任务完成，结果: {json.dumps(result, indent=2)}")
        return result
    else:
        print(f"查询失败，状态码：{response.status_code}，响应内容：{response.text}")
        return {"error": response.text}


def poll_task_status(task_id, interval=3):
    """
    轮询任务状态直到完成
    :param task_id: 任务 ID
    :param interval: 轮询间隔秒数
    :return: 最终任务结果
    """
    while True:
        result = check_task_status(task_id)
        if result.get('task_status') != 'RUNNING':
            return result
        time.sleep(interval)