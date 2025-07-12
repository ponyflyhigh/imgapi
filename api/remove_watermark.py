import requests
import json
import os
import time

# 设置API Key
api_key = os.getenv("DASHSCOPE_API_KEY")
if not api_key:
    raise Exception("请设置DASHSCOPE_API_KEY环境变量")

# 请求配置
url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis'
headers = {
    'X-DashScope-Async': 'enable',
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
    'X-DashScope-OssResourceResolve': 'enable'
}

def perform_image_removal(base_image_url, n=1, prompt='去除水印', interval=3, max_attempts=20):
    """
    执行图片去水印并返回最终结果
    
    Args:
        base_image_url: 原始图片URL
        n: 生成结果数量
        prompt: 提示词
        interval: 轮询间隔(秒)
        max_attempts: 最大尝试次数
        
    Returns:
        包含处理结果的字典或错误信息
    """
    # 提交去水印任务
    data = {
        "model": "wanx2.1-imageedit",
        "input": {
            "function": "remove_watermark",
            "prompt": prompt,
            "base_image_url": base_image_url
        },
        "parameters": {"n": n}
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code != 200:
        return {"error": f"提交失败，状态码: {response.status_code}, 详情: {response.text}"}
    
    task_id = response.json().get('output', {}).get('task_id')
    if not task_id:
        return {"error": "未获取到任务ID", "response": response.json()}
    
    # 轮询任务状态
    for attempt in range(max_attempts):
        task_url = f'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}'
        status_response = requests.get(task_url, headers=headers)
        
        if status_response.status_code != 200:
            return {"error": f"查询失败，状态码: {status_response.status_code}, 详情: {status_response.text}"}
        
        result = status_response.json()
        status = result.get('output', {}).get('task_status', 'UNKNOWN')
        
        if status == 'SUCCEEDED':
            return result.get('output', {})
        
        if status in ['FAILED', 'CANCELED']:
            return {"error": f"任务已终止，状态: {status}", "details": result.get('output', {})}
            
        print(f"尝试 {attempt+1}/{max_attempts}: 任务状态为 {status}，等待{interval}秒...")
        time.sleep(interval)
    
    return {"error": f"轮询超时，超过最大尝试次数({max_attempts})"}

def check_task_status(task_id):
    """查询单个任务状态"""
    task_url = f'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}'
    response = requests.get(task_url, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        status = result['output']['task_status']  # 从output中获取状态
        print(f"当前状态: {status}")
        return result
    return {'status': 'ERROR', 'details': f"查询失败: {response.text}"}

def poll_task_status(task_id, interval=3, max_attempts=20):
    """轮询任务状态直到完成或超时"""
    for attempt in range(max_attempts):
        result = check_task_status(task_id)
        status = result['output']['task_status']  # 直接获取状态
        
        if status != 'RUNNING':
            return result
            
        print(f"尝试 {attempt+1}/{max_attempts}: 等待{interval}秒...")
        time.sleep(interval)
    
    return {'status': 'TIMEOUT', 'details': f"超过最大尝试次数({max_attempts})"}

# 示例调用
if __name__ == "__main__":
    image_url = "https://martin-leo.oss-cn-shenzhen.aliyuncs.com/screenshot-20250712-165040.png"
    task_id = perform_image_removal(image_url)
    
    if task_id:
        result = poll_task_status(task_id)
        final_status = result['output']['task_status']
        
        if final_status == 'SUCCEEDED':
            print("任务成功!")
            print(f"结果: {json.dumps(result['output'], indent=2)}")
        else:
            print(f"任务结束: {final_status}，详情: {result.get('details')}")