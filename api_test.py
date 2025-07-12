import asyncio
import aiohttp

# 本地 Flask 服务地址
base_url = "http://127.0.0.1:5000"
#base_url = "http://43.100.21.199:5000"


async def async_test_changebg(session):
    url = f"{base_url}/change_bg"
    payload = {
        "base_image_url": "https://myl11.oss-cn-shenzhen.aliyuncs.com/test_koutu.png",
        "ref_image_url": "https://myl11.oss-cn-shenzhen.aliyuncs.com/screenshot_2025-07-07_16-11-18.png",
        "ref_prompt": "",
        "n": 1
    }
    async with session.post(url, json=payload) as response:
        result = await response.text()  # 获取响应内容
        print(f"Change BG 响应状态码: {response.status}")
        print(f"Change BG 响应内容: {result}\n")


async def async_test_changecloth(session):
    url = f"{base_url}/change_cloth"
    payload = {
        "top_garment_url": "https://myl11.oss-cn-shenzhen.aliyuncs.com/clothes/p801332.jpeg",
        "bottom_garment_url": "https://myl11.oss-cn-shenzhen.aliyuncs.com/clothes/p801326.jpeg",
        "person_image_url": "https://myl11.oss-cn-shenzhen.aliyuncs.com/clothes/p812706.png"
    }
    async with session.post(url, json=payload) as response:
        result = await response.text()
        print(f"Change Cloth 响应状态码: {response.status}")
        print(f"Change Cloth 响应内容: {result}\n")


async def async_test_expand(session):
    url = f"{base_url}/expand"
    payload = {
        "base_image_url": "https://myl11.oss-cn-shenzhen.aliyuncs.com/clothes/resized_resized_screenshot_2025-07-07_12-07-18.png",
        "top_scale": 2.0,
        "bottom_scale": 2.0,
        "left_scale": 2.0,
        "right_scale": 2.0,
        "prompt": "按照原来图片背景来操作扩展"
    }
    async with session.post(url, json=payload) as response:
        result = await response.text()
        print(f"Expand 响应状态码: {response.status}")
        print(f"Expand 响应内容: {result}\n")


async def async_test_fix(session):
    url = f"{base_url}/fix"
    payload = {
        "base_image_url": "https://myl11.oss-cn-shenzhen.aliyuncs.com/BEC028B5-5F39-4caa-A5C0-F77D90575047.png",
        "prompt": "图像超分。"
    }
    async with session.post(url, json=payload) as response:
        result = await response.text()
        print(f"Fix 响应状态码: {response.status}")
        print(f"Fix 响应内容: {result}\n")


async def async_test_koutu(session):
    url = f"{base_url}/remove_bg"
    payload = {
        "image_url": "https://myl11.oss-cn-shenzhen.aliyuncs.com/clothes/resized_resized_screenshot_2025-07-07_12-07-18.png"
    }
    async with session.post(url, json=payload) as response:
        try:
            result = await response.json()  # 尝试解析为 JSON
            print(f"Koutu 响应状态码: {response.status}")
            print(f"Koutu 响应 JSON: {result}\n")
        except aiohttp.ContentTypeError:
            # 如果不是 JSON，返回原始文本
            result = await response.text()
            print(f"Koutu 响应状态码: {response.status}")
            print(f"Koutu 响应（非 JSON）: {result}\n")


async def async_test_remove_watermark(session):
    url = f"{base_url}/remove_watermark"
    payload = {
        "image_url": "https://martin-leo.oss-cn-shenzhen.aliyuncs.com/screenshot-20250712-165040.png"
    }
    async with session.post(url, json=payload) as response:
        try:
            result = await response.json()  # 尝试解析为 JSON
            print( result)
        except aiohttp.ContentTypeError:
            # 如果不是 JSON，返回原始文本
            result = await response.text()
            print(f"Remove Watermark 响应状态码: {response.status}")
            print(f"Remove Watermark 响应（非 JSON）: {result}\n")

async def main():
    # 创建一个异步 HTTP 会话（可复用连接，提高效率）
    async with aiohttp.ClientSession() as session:
        # 将所有异步任务添加到任务列表
        tasks = [
            # async_test_changebg(session),
            # async_test_changecloth(session),
            # async_test_expand(session),
            # async_test_fix(session),
            # async_test_koutu(session)
            async_test_remove_watermark(session)  # 添加此行
        ]
        # 并发执行所有任务（无需等待前一个完成）
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())