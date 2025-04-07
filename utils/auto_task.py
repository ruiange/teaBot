import logging
from lib2to3.pgen2.tokenize import group

from server.get_chatroom_members import get_chatroom_members
from server.query_db import query_db


def auto_task(wcf):
    logging.info('自动执行任务~~~')
    group_new_list = []
    group_list =query_db(wcf, 'MicroMsg.db', 'select * from Session')
    for i in group_list:
        if "@chatroom" in i['strUsrName']:
            group_new_list.append(i['strUsrName'])
            get_chatroom_members(wcf, i['strUsrName'])
    logging.info(group_new_list)
