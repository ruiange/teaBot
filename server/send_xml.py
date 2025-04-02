def send_xml_message(wcf, recipient, xml, xml_type, path):
    """
    receiver(str): 消息接收人，wxid或者roomid
    xml(str): xml 内容
    xml_type(int): xml类型，如：0x21为小程序 (type)
    path(str): 封面图片路径
    """
    wcf.send_xml(xml, recipient, xml_type, path)