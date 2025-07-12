import os
import alibabacloud_oss_v2 as oss

# 用户配置
region = 'cn-shenzhen'
endpoint = 'https://oss-cn-shenzhen.aliyuncs.com'
bucket_name = 'myl11'
object_key = 'test.png'  # 上传后 OSS 上的文件名
local_file_path = r'tmp\changebg\test.png'  # 本地文件路径

# 初始化 OSS 客户端
cfg = oss.config.load_default()
cfg.region = region
cfg.endpoint = endpoint
cfg.credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
client = oss.Client(cfg)

# 读取并上传文件
with open(local_file_path, 'rb') as f:
    data = f.read()

client.put_object(oss.PutObjectRequest(
    bucket=bucket_name,
    key=object_key,
    body=data
))

# 构造公网 URL（前提：bucket 是公共读或配置了临时授权）
public_url = f"https://{bucket_name}.{endpoint.replace('https://', '')}/{object_key}"
print(f"文件上传成功，公网访问地址：{public_url}")
