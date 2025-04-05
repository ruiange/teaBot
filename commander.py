def test_fun(data):
    headers = {
        "Content-Type": "application/json"
    }
    url = os.getenv("WEB_URL", "https://bot.server.ruiange.work")
    url = url + "/api/friends/room"
    # 确保 data 是可以被 JSON 序列化的对象
    if isinstance(data, bytes):
        data = data.decode('utf-8')
    params = {
        "data": data,
    }
    logging.info(url)
    params = json.dumps(params)
    response = requests.post(url, data=params, headers=headers)