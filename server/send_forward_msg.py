import logging
import os


def send_forward_msg (wcf, msg_id ,receiver):
    logging.info("发送转发消息")
    # 打印参数的类型
    logging.info("msg_id类型: %s" % type(msg_id))
    logging.info("receiver类型: %s" % type(receiver))
    status = wcf.forward_msg(msg_id, receiver)
    if status == 1:
        logging.info("转发消息成功")
        return True, ""
    else:
        logging.error("转发消息失败")
        return False, "转发消息失败"