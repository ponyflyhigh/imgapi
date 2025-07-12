# 图像处理 API 使用文档

## 基础信息
- **服务地址**：`http://43.100.21.199:5000'
- **请求方式**：所有接口均使用 `POST` 方法
- **数据格式**：请求/响应均为 JSON 格式


## 接口列表

### 1. 更换背景
- **接口地址**：`/change_bg`
- **功能**：将原图背景替换为参考图背景
- **请求参数**：
  | 参数名          | 类型   | 必需 | 描述                     | 默认值 |
  |-----------------|--------|------|--------------------------|--------|
  | base_image_url  | string | 是   | 主体图像 URL（需保留主体） | -      |
  | ref_image_url   | string | 是   | 参考背景图像 URL         | -      |
  | ref_prompt      | string | 否   | 背景替换提示词           | 空字符串 |
  | n               | int    | 否   | 生成结果数量             | 1      |
- **响应示例**：
  ```json
  {
  "end_time": "2025-07-08 09:45:19.598",
  "results": [
    {
      "url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/466b5214/20250708/094518_0_v3_a75dfb4b-d89b-4912-985e-645f5a7844cf.png?Expires=1752025519&OSSAccessKeyId=LTAI5tQZd8AEcZX6KZV4G8qL&Signature=SuCWVbRlGz9dIkHEAqr6%2Bz91x%2B0%3D"
    }
  ],
  "scheduled_time": "2025-07-08 09:45:07.665",
  "submit_time": "2025-07-08 09:45:07.614",
  "task_id": "a75dfb4b-d89b-4912-985e-645f5a7844cf",
  "task_metrics": {
    "FAILED": 0,
    "SUCCEEDED": 1,
    "TOTAL": 1
  },
  "task_status": "SUCCEEDED"
}
  ```


### 2. 更换衣物
- **接口地址**：`/change_cloth`
- **功能**：为人物图像更换上衣和下装
- **请求参数**：
  | 参数名             | 类型   | 必需 | 描述               |
  |--------------------|--------|------|--------------------|
  | top_garment_url    | string | 是   | 上衣图像 URL       |
  | bottom_garment_url | string | 是   | 下装图像 URL       |
  | person_image_url   | string | 是   | 人物原始图像 URL   |
- **响应示例**：
  ```json
  {
  "end_time": "2025-07-08 09:45:23.442",
  "image_url": "http://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/1d/81/20250708/4a32110a/09f95059-c02e-4696-905c-1b7735727ab8_tryon.jpg?Expires=1752025523&OSSAccessKeyId=LTAI5tKPD3TMqf2Lna1fASuh&Signature=OPjXEYErfFFM5zf4lQZY%2FOUex0w%3D",
  "scheduled_time": "2025-07-08 09:45:07.233",
  "submit_time": "2025-07-08 09:45:07.197",
  "task_id": "09f95059-c02e-4696-905c-1b7735727ab8",
  "task_status": "SUCCEEDED"
}
  ```


### 3. 图像扩展
- **接口地址**：`/expand`
- **功能**：扩展图像边缘，保持背景风格一致
- **请求参数**：


| 参数名          | 类型   | 必需 | 默认值                 | 描述                     |
|-----------------|--------|------|------------------------|--------------------------|
| base_image_url  | string | 是   | -                      | 原始图像 URL             |
| top_scale       | float  | 否   | 1.5                    | 顶部扩展比例（>1 为扩展） |
| bottom_scale    | float  | 否   | 1.5                    | 底部扩展比例             |
| left_scale      | float  | 否   | 1.5                    | 左侧扩展比例             |
| right_scale     | float  | 否   | 1.5                    | 右侧扩展比例             |
| prompt          | string | 否   | "按照原来图片背景来操作扩展" | 扩展风格提示词           |

- **响应示例**：
  ```json
  {
  "end_time": "2025-07-08 09:45:28.007",
  "results": 
    {
      "url": "https://dashscope-result-wlcb-acdr-1.oss-cn-wulanchabu-acdr-1.aliyuncs.com/1d/86/20250708/90d73410/a9b424c9-0108-4474-a2a2-07b1dc7cf217-1.png?Expires=1752025527&OSSAccessKeyId=LTAI5tKPD3TMqf2Lna1fASuh&Signature=zOJvHL7pM4NqhQ1%2FRQkcDhZc0WQ%3D"
    },
  "scheduled_time": "2025-07-08 09:45:06.684",
  "submit_time": "2025-07-08 09:45:06.639",
  "task_id": "b543b38f-92f1-4a6f-b6e8-0e92269bdcd4",
  "task_metrics": {
    "FAILED": 0,
    "SUCCEEDED": 1,
    "TOTAL": 1
  },
  "task_status": "SUCCEEDED"
}

  ```


### 4. 图像修复
- **接口地址**：`/fix`
- **功能**：对图像进行超分/修复处理
- **请求参数**：
  | 参数名         | 类型   | 必需 | 描述           | 默认值       |
  |----------------|--------|------|----------------|--------------|
  | base_image_url | string | 是   | 原始图像 URL   | -            |
  | prompt         | string | 否   | 修复提示词     | "图像超分。" |
- **响应示例**：
  ```json
   {
  "end_time": "2025-07-08 09:50:14.731",
  "results": [
    {
      "url": "https://dashscope-result-wlcb-acdr-1.oss-cn-wulanchabu-acdr-1.aliyuncs.com/1d/25/20250708/90d73410/28bae28d-ef6d-4240-9f2f-15fc363d4e0b-1.png?Expires=1752025814&OSSAccessKeyId=LTAI5tKPD3TMqf2Lna1fASuh&Signature=Ozzb9BaoauVlCXmiD4AToY1INU0%3D"
    }
  ],
  "scheduled_time": "2025-07-08 09:50:05.853",
  "submit_time": "2025-07-08 09:50:05.810",
  "task_id": "ad11dd62-7f71-4d3c-a6dc-fba7e8c4d846",
  "task_metrics": {
    "FAILED": 0,
    "SUCCEEDED": 1,
    "TOTAL": 1
  },
  "task_status": "SUCCEEDED"
}
  ```


### 5. 移除背景
- **接口地址**：`/remove_bg`
- **功能**：移除图像背景，保留主体
- **请求参数**：
  | 参数名       | 类型   | 必需 | 描述         |
  |--------------|--------|------|--------------|
  | image_url    | string | 是   | 原始图像 URL |


## 错误响应格式
所有接口错误响应统一格式：
```json
{
  "error": "错误描述信息"
}
```
- 状态码 `400`：参数缺失或无效
- 状态码 `500`：服务器处理异常


根据readme.md的格式，我将为[remove_watermark](file://c:\Users\86132\Desktop\副业\imgapi-master\api\remove_watermark.py#L0-L0)、[photo_resize](file://c:\Users\86132\Desktop\副业\imgapi-master\utils\photo_resize.py#L0-L0)和[photo_convert](file://c:\Users\86132\Desktop\副业\imgapi-master\test\photo_convert.py#L0-L0)接口整理请求文档。以下是整理后的内容：

## 6. 移除水印
- **接口地址**：`/remove_watermark`
- **功能**：移除图像中的水印，保留主体内容
- **请求参数**：
  | 参数名         | 类型   | 必需 | 描述           |
  |----------------|--------|------|----------------|
  | image_url      | string | 是   | 原始图像 URL   |
- **响应示例**：
  ```json
  {
    "end_time": "2025-07-12 18:23:31.000",
    "results": [
      {
        "url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/466b5214/20250712/182330_0_v3_a75dfb4b-d89b-4912-985e-645f5a7844cf.png?Expires=1752025519&OSSAccessKeyId=LTAI5tQZd8AEcZX6KZV4G8qL&Signature=SuCWVbRlGz9dIkHEAqr6%2Bz91x%2B0%3D"
      }
    ],
    "scheduled_time": "2025-07-12 18:23:19.665",
    "submit_time": "2025-07-12 18:23:19.614",
    "task_id": "a75dfb4b-d89b-4912-985e-645f5a7844cf",
    "task_metrics": {
      "FAILED": 0,
      "SUCCEEDED": 1,
      "TOTAL": 1
    },
    "task_status": "SUCCEEDED"
  }
  ```

## 7. 调整尺寸（！！！可选云端URL）
- **接口地址**：`/utils/photo_resize_url`
- **功能**：通过图片 URL 调整图片尺寸
- **请求参数**：
  | 参数名         | 类型   | 必需 | 默认值 | 描述                     |
  |----------------|--------|------|--------|--------------------------|
  | image_url      | string | 是   | -      | 原始图像 URL             |
  | min_dim        | int    | 否   | 512    | 最小尺寸限制             |
  | max_dim        | int    | 否   | 4096   | 最大尺寸限制             |
- **响应示例**：
  ```json
  {
    "success": true,
    "original_size": "1024x768px",
    "resized_size": "512x384px",
    "image_data": "base64_encoded_image"
  }
  ```

## 8. 调整尺寸（本地上传） 
- **接口地址**：`/utils/photo_resize`
- **功能**：通过上传本地图片调整图片尺寸
- **请求参数**：
  | 参数名         | 类型   | 必需 | 默认值 | 描述                     |
  |----------------|--------|------|--------|--------------------------|
  | image          | file   | 是   | -      | 原始图像文件             |
  | min_dim        | int    | 否   | 512    | 最小尺寸限制             |
  | max_dim        | int    | 否   | 4096   | 最大尺寸限制             |
- **响应示例**：
  ```json
  {
    "success": true,
    "original_size": "1024x768px",
    "resized_size": "512x384px",
    "image_data": "base64_encoded_image"
  }
  ```

## 9. 格式转换（包含jpg、webp、svg、tiff、gif、bmp转为png格式）
- **接口地址**：`/utils/convert_to_png`
- **功能**：将上传的图片转换为 PNG 格式
- **请求参数**：
  | 参数名           | 类型   | 必需 | 默认值 | 描述                     |
  |------------------|--------|------|--------|--------------------------|
  | image            | file   | 是   | -      | 需要转换的原始图片       |
  | keep_animation   | bool   | 否   | false  | 是否保留 GIF 动画拆分     |
  | overwrite        | bool   | 否   | false  | 是否覆盖已存在的输出文件 |
- **响应示例**：
  ```json
  {
    "success": true,
    "message": "转换成功",
    "original_format": "jpeg",
    "converted_format": "png",
    "image_paths": ["/tmp/resized_image.png"],
    "image_data": "base64_encoded_image"
  }
