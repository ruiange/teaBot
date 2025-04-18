import json
import logging
import os

import requests

from server.get_chatroom_members import get_chatroom_members
from server.send_text import send_text_message
from utils.query_group_name import query_group_name


def welcome(wcf,msg,name):
    roomid = msg.roomid
    room_name = query_group_name(wcf,roomid)
    welcome_text = " 欢迎新朋友【" + name + "】加入【"+ room_name+"】"
    send_text_message(wcf, roomid, welcome_text)
    get_chatroom_members(wcf, roomid, False)
    headers = {
        "Content-Type": "application/json"
    }
    url = os.getenv("WEB_URL", "http://156.225.18.227:3000")
    url = url + "/api/friends/room"
    params = {
        "roomid": roomid
    }
    params = json.dumps(params)
    res_data = requests.get(url, data=params, headers=headers)
    json_data = res_data.json()
    logging.info(json_data.get("data"))
    if json_data.get("code")==200:
        logging.info('获取群信息成功')
        info_data = json_data.get("data")
        welcome_text= info_data.get("welcome")
        if welcome:
            send_text_message(wcf, roomid, welcome_text)
    else:
        logging.info('获取群信息失败')
        return None





