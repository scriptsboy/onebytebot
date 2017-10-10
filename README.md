# onebytebot
Telegram机器人，开发人员的工具箱

# 运行环境
* Python3

# 第三方库

### demjson
```
pip3 install demjson
```

### requests
```
pip3 install requests
```

### threadpool
```
pip3 install threadpool
```

### python-telegram-bot
```
git clone https://github.com/python-telegram-bot/python-telegram-bot --recursive
cd python-telegram-bot
git submodule update --init --recursive
python3 setup.py install
```

# 启动服务
设置环境变量 `TELEGRAM_BOT_TOKEN` 为你的机器人Token，然后执行命令：
```python
python3 main.py
```
