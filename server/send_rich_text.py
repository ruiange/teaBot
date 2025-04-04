import json
import logging


def send_rich_text_message(wcf, content):
    logging.info("发送卡片消息")

    name = content.get("name")
    account = content.get("account")
    title = content.get("title")
    digest = content.get("digest")
    url = content.get("url")
    thumburl = content.get("thumburl")
    receiver = content.get("receiver")
    wcf.send_rich_text(name, account, title, digest, url, thumburl, receiver)