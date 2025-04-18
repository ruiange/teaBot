import json
import logging
import os
import requests
from server.query_db import query_db


def get_friends(wcf):
    logging.info("开始获取好友列表")
    friends = wcf.get_friends()
    logging.info("获取好友列表完成")
    headers = {
        "Content-Type": "application/json"
    }
    url = os.getenv("WEB_URL", "http://156.225.18.227:3000")
    url = url + "/api/friends"
    params = {
        "friends": friends
    }
    params = json.dumps(params)

    requests.post(url, data=params, headers=headers)
    if friends:
        logging.info('获取好友列表成功')
        logging.info(friends)
        return friends
    else:
        logging.info('获取好友列表失败')
        return None
