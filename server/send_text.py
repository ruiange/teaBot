import logging
import os


def send_text_message(wcf, recipient, content, at_users=None, callback=None):
    """
    发送消息给指定的接收者
    :param wcf: WeChatFeatures 实例
    :param recipient: 接收者
    :param content: 消息内容
    :param at_users: 需要 @ 的用户列表
    :param callback: 回调函数，接收参数 (success: bool, error_msg: str)
    :return: (bool, str) 元组，表示 (是否成功, 错误信息)
    """

    no_send = os.getenv("NO_SEND",0)
    # no_send 转为整数类型
    no_send = int(no_send)
    logging.info(f"no_send{no_send}")
    if no_send == 1:
        logging.info("不发送")
        return True

    try:
        # 发送文本消息
        if at_users:
            result = wcf.send_text(content, recipient, at_users)
        else:
            result = wcf.send_text(content, recipient)

        if result == 0:
            logging.info(f"已发送消息给 {recipient}: {content}")
            if callback:
                callback(True, "")
            return True, ""
        else:
            error_msg = f"发送消息失败，错误代码: {result}"
            logging.error(error_msg)
            if callback:
                callback(False, error_msg)
            return False, error_msg
            
    except Exception as e:
        error_msg = f"发送消息失败: {str(e)}"
        logging.error(error_msg)
        if callback:
            callback(False, error_msg)
        return False, error_msg 