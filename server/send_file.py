import logging

def send_file_message(wcf, recipient, path, callback=None):
    logging.info(path)
    """
    发送文件消息给指定的接收者
    :param wcf: WeChatFeatures 实例
    :param recipient: 接收者
    :param path: 文件路径
    :param callback: 回调函数，接收参数 (success: bool, error_msg: str)
    :return: (bool, str) 元组，表示 (是否成功, 错误信息)
    """
    try:
        # 发送文件消息
        # 假设 wcf 有一个 send_file 方法
        wcf.send_file(path,recipient)
        success = True
        error_msg = ""
        
        # 如果有回调函数，调用它
        if callback:
            callback(success, error_msg)
        
        return success, error_msg

    except Exception as e:
        logging.error(f"发送文件失败: {str(e)}")
        success = False
        error_msg = str(e)
        
        # 如果有回调函数，调用它
        if callback:
            callback(success, error_msg)
        
        return success, error_msg

