import json
import logging
import os

import requests


from server.query_db import query_db
from server.send_text import send_text_message


def get_chatroom_members(wcf, roomid,is_send = True):
    query_data = query_db(wcf, "MicroMsg.db", "SELECT * FROM ContactHeadImgUrl")
    res = wcf.get_chatroom_members(roomid)


    logging.info('获取群成员信息')

    headers = {
        "Content-Type": "application/json"
    }
    url = os.getenv("WEB_URL", "https://bot.server.ruiange.work")
    url = url + "/api/friends/members"
    params = {
        "members": res,
        "query_data": query_data,
        "roomid": roomid
    }
    logging.info(url)
    params = json.dumps(params)
    requests.post(url, data=params, headers=headers)
    if res:
        logging.info('获取群成员信息成功')
        logging.info(res)
        if is_send:
            send_text_message(wcf, roomid, "更新群成员信息成功")
        return res
    else:
        logging.info('获取群成员信息失败')
        return None
