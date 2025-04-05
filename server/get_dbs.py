import logging


def get_dbs(wcf):
    logging.info('获取数据库列表')
    res = wcf.get_dbs()
    if res:
        logging.info('获取数据库列表成功')
        logging.info(res)
        return res
    else:
        logging.info('获取数据库列表失败')
        return False