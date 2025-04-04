import json
import logging
import os

import requests


def get_friends(wcf):
    logging.info("开始获取好友列表")
    # 打印等待动画
    headers = {
        "Content-Type": "application/json"
    }
    url = os.getenv("WEB_URL", "https://bot.server.ruiange.work")
    url = url + "/api/friends"
    logging.info(url)
    friends = wcf.get_friends()
    params = {
        "friends": friends
    }
    params = json.dumps(params)
    requests.post(url, data=params, headers=headers)
    logging.info("获取好友列表完成")