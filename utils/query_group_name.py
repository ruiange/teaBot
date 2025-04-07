import logging

from server.query_db import query_db

def query_group_name(wcf,roomid):
    test_data = query_db(wcf, 'MicroMsg.db', 'select * from Session')
    # 遍历test_data 如果 strUsrName 等于roomid 返回strNickName
    for i in test_data:
        if i['strUsrName'] == roomid:
            logging.info(i['strNickName'])
            return i['strNickName']