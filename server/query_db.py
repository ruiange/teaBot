import logging


def query_db(wcf, db,sql):
    res = wcf.query_sql(db,sql)
    if res:
        logging.info('查询数据库成功')
        return res
    else:
        logging.info('查询数据库失败')
        return False
