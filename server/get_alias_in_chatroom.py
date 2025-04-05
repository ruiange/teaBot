import logging


def get_alias_in_chatroom (wcf, wxid,roomid):
    res = wcf.get_alias_in_chatroom(wxid,roomid)
    logging.info('获取群成员名片================')
    if res:
        logging.info('获取群成员名片成功')
        logging.info(res)
    else:
        logging.info('获取群成员名片失败')
    return res