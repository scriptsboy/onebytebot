# onebytebot
onebytebot([http://t.me/onebyte_bot](http://t.me/onebyte_bot))是基于Telegram Bot实现一个开发人员的工具箱。支持以下命令：
* run - 运行一段代码
* zip - 打包下载stickers集合
* fmt - 格式化json/xml格式文件
* info - 输出当前对话框信息


# 运行环境
* Python3.5

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
