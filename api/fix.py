import requests
import json
import os
import time

# 设置API Key
api_key = os.getenv("DASHSCOPE_API_KEY")
if not api_key:
    raise Exception("请设置DASHSCOPE_API_KEY环境变量")

# 请求的URL
url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis'

# 请求头
headers = {
    'X-DashScope-Async': 'enable',
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
    'X-DashScope-OssResourceResolve': 'enable'
}

def start_image_synthesis(base_image_url,prompt="图像超分。"):
    data = {
        "model": "wanx2.1-imageedit",
        "input": {
            "function": "super_resolution",
            "prompt": prompt,
            "base_image_url": base_image_url
        },
        "parameters": {
            "upscale_factor": 1,
            "n": 1
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
    while True:
        result = check_task_status(task_id)
        if result.get('task_status') != 'RUNNING':
            return result
        time.sleep(interval)