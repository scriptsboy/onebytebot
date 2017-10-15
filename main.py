# -*- coding:utf-8 -*-
import os
import signal
import logging

import runoob
import stickers

from handlers import handlefmt
from handlers import handlerun
from handlers import handlezip
from handlers import handleinfo

from telegram.ext import Updater
from telegram.ext import CommandHandler

def signal_handler(signum, frame):
    runoob.workers.terminate()
    stickers.workers.terminate()
    logging.info("服务器已停止")

def main():
    """
    主函数
    """

    # 初始化日志库
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=format)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 监听终止信号
    stop_signals = (signal.SIGTERM, signal.SIGINT, signal.SIGABRT)
    for sig in stop_signals:
        signal.signal(sig, signal_handler)

    # 监听消息更新
    updater = Updater(os.environ['TELEGRAM_BOT_TOKEN'])
    updater.dispatcher.add_handler(CommandHandler('run', handlerun.handle))
    updater.dispatcher.add_handler(CommandHandler('fmt', handlefmt.handle))
    updater.dispatcher.add_handler(CommandHandler('zip', handlezip.handle))
    updater.dispatcher.add_handler(CommandHandler('info', handleinfo.handle))
    updater.start_polling()
    logging.info('机器人服务启动成功')
    updater.idle(stop_signals)

if __name__ == '__main__':
    main()
