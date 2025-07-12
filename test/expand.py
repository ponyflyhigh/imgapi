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
   'X-DashScope-OssResourceResolve': 'enable',
}

# 请求的数据
data = {
    "model": "wanx2.1-imageedit",
    "input": {
        "function": "expand",
        "prompt": "按照原来图片背景来操作扩展",
        "base_image_url": "oss://dashscope-instant/48e7eaa5f7819e30ae68c59bf34f5b42/2025-07-07/0d1c9227-13ae-9831-8284-c8d3a433bd4b/resized_screenshot_2025-07-07_12-07-18.png"
    },
     "parameters": {
    "top_scale": 1.5,
    "bottom_scale": 1.5,
    "left_scale": 1.5,
    "right_scale": 1.5,
    "n": 2
  }
}

# 发送POST请求
def start_image_synthesis():
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        response_json = response.json()  # 使用 .json() 解析 JSON 数据
        task_id = response_json.get('output', {}).get('task_id')  # 获取 task_id
        if task_id:
            print(f"任务ID: {task_id}")
            return task_id
        else:
            print("未找到任务ID")
            return None
    else:
        print(f"请求失败，状态码：{response.status_code}，响应内容：{response.text}")
        return None

# 查询任务状态
def check_task_status(task_id):
    task_url = f'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}'
    response = requests.get(task_url, headers=headers)
    
    if response.status_code == 200:
        response_json = response.json()
        status = response_json.get('status', '未知状态')
        print(f"任务状态: {status}")
        
        # 如果任务完成，返回最终结果
        
        result = response_json.get('output', {})
        print(f"任务完成，结果: {json.dumps(result, indent=2)}")
        return result

    else:
        print(f"查询失败，状态码：{response.status_code}，响应内容：{response.text}")
        return None

# 轮询任务状态
def poll_task_status(task_id, interval=3):
    while True:
        result = check_task_status(task_id)
        
        if result['task_status']!='RUNNING':  # 如果任务完成，返回结果
            return result
        time.sleep(interval)  # 等待3秒钟后继续查询

# 主函数
if __name__ == "__main__":
    task_id = start_image_synthesis()
    
    if task_id:
        # 等待任务完成并获取结果
        poll_task_status(task_id, interval=3)
