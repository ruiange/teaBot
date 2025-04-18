import logging
import time
from datetime import datetime

import schedule

from server.send_text import send_text_message


# 启动 schedule 循环任务
def run_schedule(wcf):
    schedule.every().monday.at("20:00:05").do(lambda: weekly_send_group_msg(wcf, '57222992702@chatroom'))
    schedule.every().monday.at("20:01:10").do(lambda: weekly_send_group_msg(wcf, '39332279895@chatroom'))
    while True:
        schedule.run_pending()
        time.sleep(1)


def weekly_send_group_msg(wcf, roomid):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"【每周任务】当前时间是：{now}")
    send_text_message(wcf, roomid, '''
1. 遵守法律法规、抵制不良骑行行为和恶意引战行为。
2. 禁止以营销为目的的人入群，严禁散播违法内容和发布各种营销广告。
3. 进群请看群公告，按要求修改群名片（如，地区+摩托范用户名）
4. 群内不提倡各种二手交易、过户代办、保险推销等行为，有需要请走正规平台更有保障。
5. 还没有做车辆认证的摩友鼓励大家去做好车辆认证，更多真实摩友的分享才更具有参考性呢！


注：本群信息较多，如有打扰屏蔽或退出即可。        
        禁止🚫高速开车，禁止🚫聊政治话题。
聊天内容不雅（包括图片视频表情文字）屡教不改者踢出群聊，如果被踢。就是公告没看明白！
       本群为遵纪守法群，网络不是法外之地，美好网络环境需你我共创，望大家配合。''')
