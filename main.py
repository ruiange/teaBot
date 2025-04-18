import sys
from wcferry import Wcf
import logging
import os
import threading
from server.message_listener import listen_for_messages
import config
import uvicorn

from utils.auto_task import auto_task
from utils.webapi import app

import schedule
import time
from datetime import datetime

from utils.week_task import weekly_send_group_msg, run_schedule

# 获取用户数据目录
app_data = os.getenv('APPDATA')
app_dir = os.path.join(app_data, 'new-boy')
log_dir = os.path.join(app_dir, 'logs')

# 创建日志目录
os.makedirs(log_dir, exist_ok=True)

interval_time = 3600

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, 'robot.log'), encoding='utf-8'),
        logging.StreamHandler(sys.stdout)  # 确保输出到stdout
    ]
)

# 修改全局信息
def modify_wxid(wxid):
    config.GLOBAL_WXID = wxid
    logging.info(f"全局 wxid 设置为: {wxid}")

logging.info("出发~")

def print_login_info(wcf):
    """打印登录账号信息"""
    logging.info("\n" + "=" * 50)
    logging.info("登录账号信息：")

    wxid = wcf.get_self_wxid()
    user_info = wcf.get_user_info()
    logging.info(f"微信号: {wxid}")
    if wxid:
        modify_wxid(wxid)

    logging.info(f"昵称: {user_info.get('name', '未知')}")
    logging.info(f"备注: {user_info.get('remark', '未知')}")

    friends = wcf.get_friends()
    logging.info(f"好友数量: {len(friends) if friends else 0}")

    logging.info("=" * 50 + "\n")

def start_webapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

def hourly_task(wcf):
    """每小时执行的任务"""
    logging.info("执行每小时任务...")
    auto_task(wcf)
    threading.Timer(interval_time, hourly_task, args=(wcf,)).start()





def main():
    try:
        wcf = Wcf()
        if not wcf.is_login():
            logging.error("请先登录微信")
            return

        if not wcf.is_receiving_msg():
            logging.info("启用消息接收功能...")
            wcf.enable_receiving_msg()

        print_login_info(wcf)

        # 启动消息监听线程
        listener_thread = threading.Thread(
            target=listen_for_messages,
            args=(wcf,),
            daemon=True
        )
        listener_thread.start()
        logging.info("消息监听线程已启动")

        # 启动每小时定时任务
        threading.Timer(interval_time, hourly_task, args=(wcf,)).start()
        logging.info("每小时定时任务已启动")

        # 启动每周定时打印时间任务
        schedule_thread = threading.Thread(
            target=run_schedule(wcf),
            daemon=True
        )
        schedule_thread.start()
        logging.info("每周定时打印时间任务已启动")

        # 主循环
        while True:
            try:
                if sys.stdin.isatty():
                    command = input()
                else:
                    command = sys.stdin.readline()

            except EOFError:
                break
            except Exception as e:
                logging.error(f"处理输入时出错: {str(e)}")
                continue

    except Exception as e:
        logging.error(f"程序启动失败: {str(e)}")
        raise
    finally:
        if 'wcf' in locals():
            wcf.cleanup()


if __name__ == "__main__":
    main()
