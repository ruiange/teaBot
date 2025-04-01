import logging
import re
import time

import requests

from server.send_image import send_image_message
from utils.download import download


def bot_commander(wcf, msg):
    logging.info("命令监听已启动，等待新命令...")
    if "douyin" in msg.content:
        logging.info(msg.content)
        # 使用正则表达式匹配URL
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, msg.content)
        url = ""
        if len(urls):
            url = urls[0]
        logging.info(url)
        get_url = "http://101.126.92.189:8090/api/hybrid/video_data?url=" + url + "/&minimal=true"
        res_data = requests.get(get_url)
        try:
            # 尝试将响应文本解析为 JSON 对象
            json_data = res_data.json()
            # 将 JSON 对象格式化为字符串并记录日志
            # new_data = json.dumps(json_data, ensure_ascii=False, indent=4)
            logging.info(json_data.get('code'))
            if json_data.get('code') == 200:
                rq_url = json_data.get('data').get('video_data').get('wm_video_url_HQ')
                logging.info("=========================================================")
                # 时间戳当文件名
                filename = str(int(time.time())) + ".mp4"
                file_path = download(rq_url, filename)
                logging.info("下载完成: %s", file_path)
                # 等待1秒执行
                time.sleep(1)
                if file_path:
                   send_image_message(wcf, msg.roomid, file_path)
        except ValueError as e:
            # 如果响应文本不是有效的 JSON，记录错误信息
            logging.error("无法解析 JSON 数据: %s", e)
            logging.info(res_data.text)
    if "bilibili" in msg.content:
        logging.info(msg.content)




