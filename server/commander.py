import json
import logging
import os
import re
import time

import requests

from server.get_chatroom_members import get_chatroom_members
from server.get_dbs import get_dbs
from server.get_friends import get_friends
from server.get_tables import get_tables
from server.query_db import query_db
from server.send_image import send_image_message
from server.send_rich_text import send_rich_text_message
from server.send_text import send_text_message
from server.send_xml import send_xml_message
from utils.download import download

VOICE_XML = """<?xml version="1.0"?>
   <msg>
       <appmsg appid="" sdkver="0">
           <title>点我下单，开启甜蜜一天！</title>
           <des>蜜雪冰城</des>
           <type>33</type>
           <url>https://mp.weixin.qq.com/mp/waerrpage?appid=wx7696c66d2245d107&amp;type=upgrade&amp;upgradetype=3#wechat_redirect</url>
           <appattach>
               <cdnthumburl>3057020100044b30490201000204165ac44b02032f59e1020490c7587d020467ee8310042461346463626563302d346364352d343866382d393930382d3832306263643861643230610204051408030201000405004c50b900</cdnthumburl>
               <cdnthumbmd5>988ade2e67db1f30449b7c59be4a8ea6</cdnthumbmd5>
               <cdnthumblength>71619</cdnthumblength>
               <cdnthumbwidth>514</cdnthumbwidth>
               <cdnthumbheight>411</cdnthumbheight>
               <cdnthumbaeskey>c02a590d7ca8d0d3ccec4487d9001fae</cdnthumbaeskey>
               <aeskey>c02a590d7ca8d0d3ccec4487d9001fae</aeskey>
               <encryver>0</encryver>
               <filekey>52602527714@chatroom_171_1743759397</filekey>
           </appattach>
           <sourceusername>gh_c5110cb8e4ba@app</sourceusername>
           <sourcedisplayname>蜜雪冰城</sourcedisplayname>
           <md5>988ade2e67db1f30449b7c59be4a8ea6</md5>
           <weappinfo>
               <username><![CDATA[gh_c5110cb8e4ba@app]]></username>
               <appid><![CDATA[wx7696c66d2245d107]]></appid>
               <type>2</type>
               <version>153</version>
               <weappiconurl><![CDATA[http://mmbiz.qpic.cn/mmbiz_png/nIXRlsiagnD95icQUiafpKbjbQZPZHsrK0ArJia2Y5IRvbUkFLpKhuKUd3zj3zVuZhKWiaiaDY4Wg3mkoM41hn332Orw/640?wx_fmt=png&wxfrom=200]]></weappiconurl>
               <pagepath><![CDATA[pages/index/index.html?_um_ssrc=o6pFE5ag-IN2x8owXC71XPIXtTio&_um_sts=1743759395688]]></pagepath>
               <shareId><![CDATA[0_wx7696c66d2245d107_ef58478d34b8c8af3b65cb3c2152a692_1743759396_0]]></shareId>
               <appservicetype>0</appservicetype>
               <brandofficialflag>0</brandofficialflag>
               <showRelievedBuyFlag>103967</showRelievedBuyFlag>
               <hasRelievedBuyPlugin>0</hasRelievedBuyPlugin>
               <flagshipflag>0</flagshipflag>
               <wxaTradeCommentScore>0</wxaTradeCommentScore>
               <subType>0</subType>
               <isprivatemessage>0</isprivatemessage>
               <weapppagethumbrawurl><![CDATA[https://mxsa-oss.mxbc.net/oss/ad/20250329/1db198f0019f4eda97f6b98252508d2d.jpg]]></weapppagethumbrawurl>
           </weappinfo>
       </appmsg>
       <fromusername>ruiangel</fromusername>
       <scene>0</scene>
       <appinfo>
           <version>1</version>
           <appname></appname>
       </appinfo>
       <commenturl></commenturl>
   </msg>"""


def update_group_info(f_data,wcf,roomid):
    headers = {
        "Content-Type": "application/json"
    }
    url = os.getenv("WEB_URL", "https://bot.server.ruiange.work")
    url = url + "/api/friends/room"

    # 循环f_data，取出strNickName和strUsrName报错为新数组
    list_data = []
    for item in f_data:
        if "strNickName" in item and "strUsrName" in item:
            list_data.append({
                "strNickName": item["strNickName"],
                "strUsrName": item["strUsrName"]
            })
        else:
            print("Error: Missing 'strNickName' or 'strUsrName' in item")
            continue
    params = {
        "list_data": list_data
    }
    params = json.dumps(params)
    response = requests.post(url, data=params, headers=headers)
    if response.status_code == 200:
        send_text_message(wcf, roomid, "更新群信息成功")
    else:
        print("请求失败，状态码：", response.status_code)



def statistics (roomid):
    headers = {
        "Content-Type": "application/json"
    }
    url = os.getenv("WEB_URL", "https://bot.server.ruiange.work")
    url = url + "/api/statistics"
    logging.info(url)
    data = {
        "roomid": roomid
    }
    data = json.dumps(data)
    response = requests.post(url, data=data, headers=headers)
    logging.info(response.text)
    json_res = json.loads(response.text)
    # 检查响应状态码
    if response.status_code == 200:
        print("请求成功！")
        return json_res.get("data")
    else:
        print("请求失败，状态码：", response.status_code)


def bot_commander(wcf, msg):
    logging.info("命令监听已启动，等待新命令...")
    roomid = msg.roomid
    sender = msg.sender
    if msg.content == '/更新群'and sender=="ruiangel":
       test_data =  query_db(wcf, 'MicroMsg.db', 'select * from Session')
       update_group_info(test_data,wcf,roomid)
    if msg.content == "/更新群成员" and sender=="ruiangel":
        get_chatroom_members(wcf, roomid)
    if msg.content == "/获取表" and sender=="ruiangel":
        get_tables(wcf,'MicroMsg.db')
    if msg.content == "/获取数据库" and sender=="ruiangel":
        get_dbs(wcf)
    if msg.content == "/发小程序" and sender=="ruiangel":
        send_xml_message(wcf, roomid, VOICE_XML, 0x21)

    if msg.content == "/获取好友" and sender=="ruiangel":
        logging.info("获取好友命令已执行")
        get_friends(wcf)



    if msg.content == "统计":
        logging.info("统计命令已执行")
        content = statistics(roomid)
        logging.info(content)
        send_rich_text_message(wcf, content)


    if "douyin" in msg.content:
        logging.info(msg.content)
        # 使用正则表达式匹配URL
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, msg.content)
        url = ""
        if len(urls):
            url = urls[0]
        logging.info(url)
        get_url = "http://101.126.92.189:8090/api/hybrid/video_data?url=" + url + "/&minimal=true"
        res_data = requests.get(get_url)
        try:
            # 尝试将响应文本解析为 JSON 对象
            json_data = res_data.json()
            # 将 JSON 对象格式化为字符串并记录日志
            # new_data = json.dumps(json_data, ensure_ascii=False, indent=4)
            logging.info(json_data.get('data').get('type'))
            if json_data.get('code') == 200:
                if json_data.get('data').get('type') == "video":
                    logging.info("=========================================================")
                    logging.info(json_data)
                    rq_url = json_data.get('data').get('video_data').get('wm_video_url_HQ')
                    logging.info("=========================================================")
                    # 时间戳当文件名
                    filename = str(int(time.time())) + ".mp4"
                    file_path = download(rq_url, filename)
                    logging.info("下载完成: %s", file_path)
                    # 等待1秒执行
                    time.sleep(1)
                    if file_path:
                        send_image_message(wcf, msg.roomid, file_path)
                if json_data.get('data').get('type') == "image":
                    image_list = json_data.get('data').get('image_data').get('no_watermark_image_list')
                    logging.info(image_list)
                    # 遍历打印列表中的每个元素
                    for image in image_list:
                        # 获取图片的 URL
                        image_url = image
                        # 下载图片
                        filename = str(int(time.time())) + ".jpg"
                        file_path = download(image_url, filename)
                        logging.info("下载完成: %s", file_path)
                        # 等待1秒执行
                        time.sleep(1)
                        if file_path:
                            send_image_message(wcf,msg.roomid, file_path)
        except ValueError as e:
            # 如果响应文本不是有效的 JSON，记录错误信息
            logging.error("无法解析 JSON 数据: %s", e)
            logging.info(res_data.text)







