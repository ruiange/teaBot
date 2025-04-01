import os
import requests  # 确保已安装 requests 库
from tqdm import tqdm  # 用于显示进度条
import logging

def download(url,filename):
    # 获取项目根目录
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # 获取项目根目录
    file_dir = os.path.join(root_dir, 'file')  # 拼接出 file 文件夹的路径

    # 如果 file 目录不存在，则创建该目录
    os.makedirs(file_dir, exist_ok=True)


    file_path = os.path.join(file_dir, filename)

    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer':url
    }

    # 使用会话保持状态
    with requests.Session() as session:
        # 下载文件，使用流式请求
        response = session.get(url, stream=True, headers=headers, allow_redirects=True)
        
        # 检查响应状态码
        if response.status_code == 403:
            logging.error("访问被拒绝，可能是防盗链问题。")
            return None
        
        response.raise_for_status()  # 对于错误的响应抛出异常

        # 获取文件大小
        total_size = int(response.headers.get('content-length', 0))

        # 使用 tqdm 创建进度条
        with open(file_path, 'wb') as file, \
             tqdm(desc=filename,
                  total=total_size,
                  unit='iB',
                  unit_scale=True,
                  unit_divisor=1024) as pbar:
            for data in response.iter_content(chunk_size=1024):
                size = file.write(data)
                pbar.update(size)

    # 返回下载文件的绝对路径
    return os.path.abspath(file_path)


