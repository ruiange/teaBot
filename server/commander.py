import json
import logging
import os
import re
import time

import requests

from server.get_friends import get_friends
from server.send_image import send_image_message
from server.send_rich_text import send_rich_text_message
from utils.download import download

def statistics (roomid):
    headers = {
        "Content-Type": "application/json"
    }
    url = os.getenv("WEB_URL", "https://bot.server.ruiange.work")
    url = url + "/api/statistics"
    logging.info(url)
    data = {
        "roomid": roomid
    }
    data = json.dumps(data)
    response = requests.post(url, data=data, headers=headers)
    logging.info(response.text)
    json_res = json.loads(response.text)
    # 检查响应状态码
    if response.status_code == 200:
        print("请求成功！")
        return json_res.get("data")
    else:
        print("请求失败，状态码：", response.status_code)

def bot_commander(wcf, msg):
    logging.info("命令监听已启动，等待新命令...")
    roomid = msg.roomid

    if msg.content == "/获取好友":
        logging.info("获取好友命令已执行")
        get_friends(wcf)

    if msg.content == "统计":
        logging.info("统计命令已执行")
        content = statistics(roomid)
        logging.info(content)
        send_rich_text_message(wcf, content)


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
            logging.info(json_data.get('data').get('type'))
            if json_data.get('code') == 200:
                if json_data.get('data').get('type') == "video":
                    logging.info("=========================================================")
                    logging.info(json_data)
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
                if json_data.get('data').get('type') == "image":
                    image_list = json_data.get('data').get('image_data').get('no_watermark_image_list')
                    logging.info(image_list)
                    # 遍历打印列表中的每个元素
                    for image in image_list:
                        # 获取图片的 URL
                        image_url = image
                        # 下载图片
                        filename = str(int(time.time())) + ".jpg"
                        file_path = download(image_url, filename)
                        logging.info("下载完成: %s", file_path)
                        # 等待1秒执行
                        time.sleep(1)
                        if file_path:
                            send_image_message(wcf,msg.roomid, file_path)
        except ValueError as e:
            # 如果响应文本不是有效的 JSON，记录错误信息
            logging.error("无法解析 JSON 数据: %s", e)
            logging.info(res_data.text)







