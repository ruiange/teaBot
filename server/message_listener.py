import json
import logging
import time
import threading  # ✅ 新增
from queue import Empty

import requests
import config
from server.commander import bot_commander
from server.send_text import send_text_message
from server.system_message_execution import system_message_execution
from utils.ai_reply import ai_reply

import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

def get_msg_type(type_id):
    """将消息类型ID转换为可读的中文描述"""
    msg_types = {
        1: "文本消息",
        3: "图片消息",
        34: "语音消息",
        43: "视频消息",
        47: "表情消息",
        49: "应用消息",
        10000: "系统消息"
    }
    return msg_types.get(type_id, f"未知类型({type_id})")


def listen_for_messages(wcf):
    """监听消息并打印消息详情"""
    logging.info("消息监听已启动，等待新消息...")

    while True:
        try:
            # 获取消息
            msg = wcf.get_msg()

            if msg:
                up_data = json.dumps(msg.__dict__, indent=4, ensure_ascii=False)

                # ✅ 使用线程异步执行 make_request
                threading.Thread(target=make_request, args=(up_data,)).start()

                logging.info('---------------begin--------------------')
                logging.info(f"id：{msg.id}")
                logging.info(f"消息类型: {get_msg_type(msg.type)} {msg.type}")
                logging.info(f"消息发送者: {msg.sender}")
                logging.info(f"群 id: {msg.roomid}")
                logging.info(f"内容: {msg.content}")
                logging.info('消息来源: 群聊' if msg.from_group() else '消息来源: 私聊')
                logging.info(f"来自自己: {msg.from_self()}")
                logging.info(f"是否@: {msg.is_at(config.GLOBAL_WXID)}")
                logging.info(f"是否文本: {msg.is_text()}")

                formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(msg.ts)))
                logging.info(f"消息时间: {formatted_time}")

                logging.info(f"当前时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")

                # 系统消息处理
                if msg.type == 10000:
                    system_message_execution(wcf, msg)

                # 群聊 @ 自己时回复
                if msg.from_group() and msg.is_at(config.GLOBAL_WXID):
                    reply = ai_reply(msg.content)
                    logging.info(reply)
                    if reply and config.GLOBAL_WXID:
                        send_text_message(wcf, msg.roomid, reply)

                # 处理指令
                if msg.is_text():
                    bot_commander(wcf, msg)

                logging.info('---------------end--------------------')

        except Empty:
            time.sleep(0.5)
            continue

        except KeyboardInterrupt:
            logging.info("消息监听已停止")
            break

        except Exception as e:
            logging.error(f"消息监听出错: {str(e)}")
            time.sleep(1)
            continue


def make_request(data):
    url = os.getenv("WEB_URL", "http://156.225.18.227:3000")

    if not url:
        logging.error("WEB_URL not found in .env file,.env里没有配置WEB_URL")
        return

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 200:
            print("请求成功！")
            print("响应内容：", response.text)
        else:
            print("请求失败，状态码：", response.status_code)
    except requests.RequestException as e:
        logging.error(f"发送请求失败: {str(e)}")
