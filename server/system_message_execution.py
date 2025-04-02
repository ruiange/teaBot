import logging
import re

from utils.welcome import welcome


def system_message_execution(wcf, msg):
    # 如果msg.content里包含 "邀请" 并且包含 “加入了群聊”
    if "邀请" in msg.content and "加入了群聊" in msg.content:
        logging.info('有人加入了群聊')
        logging.info(msg.content)
        username = re.findall(r'"(.*?)"', msg.content)
        logging.info(username)
        welcome(wcf,msg,username[0])