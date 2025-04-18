# 发言总结
import json
import logging
import os

import config
import requests

from server.send_text import send_text_message


def summary_presentation(wcf, roomid):
    """
    功能：根据发言记录生成总结
    参数：
        - wcf: 聊天机器人对象
        - roomid: 聊天室ID
    返回值：
        - summary: 总结结果
    """
    logging.info("请求发言总结")
    headers = {
        "Content-Type": "application/json"
    }
    url = os.getenv("WEB_URL", "http://156.225.18.227:3000")
    url = url + "/api/summary"
    params = {
        "roomid": roomid,
        "wxid":config.GLOBAL_WXID
    }
    logging.info(url)
    params = json.dumps(params)
    res = requests.post(url, data=params, headers=headers)
    json_data = res.json()



    reply = json_data.get("data")

    if reply:
        logging.info(f'发言总结成功{reply}')
        send_text_message(wcf, roomid, reply)
        return res
    else:
        logging.info('获取发言总结失败')
        return None