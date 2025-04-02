from server.send_text import send_text_message


def welcome(wcf,msg,name):
    reply = " ⚠️新进群的朋友⚠️\n\n ⚠️请及时修改昵称（地区+摩托范昵称），以防被踢⚠️"
    welcome_text = " 欢迎新朋友【" + name + "】加入[摩托范 巧格i全国2群]🎇🎇🎇"
    send_text_message(wcf, msg.roomid, welcome_text)
    send_text_message(wcf, msg.roomid, reply)
