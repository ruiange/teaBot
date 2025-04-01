## 业务使用express开发，py真的不会写


- 功能：
    - [x] 监听微信消息
    - [ ] 统计群发言
    - [x] 下载抖音视频
    - [x] 自动回复
    - [ ] 多轮回复


### 本地启动步骤

根目录执行
```pip
pip install -r requirements.txt
```

## 运行
根目录执行
```text
python main.py
```


### 打包步骤
```text
pyinstaller --onefile --add-data "C:\Users\bombi\teaBot\.venv\Lib\site-packages\wcferry;wcferry" --hidden-import "_cffi_backend" main.py
```
