# -*- coding:utf-8 -*-

import os
from telegram.bot import Bot
from helper import Singleton

InfoUserPath        = 'config/info/user.txt'
InfoChatPath        = 'config/info/chat.txt'
InfoChannelPath     = 'config/info/channel.txt'

FormatResPath       = 'config/fmt/res.txt'

RuncodeResPath      = 'config/run/res.txt'
RuncodeUsePath      = 'config/run/use.txt'

ZipUsePath          = 'config/zip/use.txt'

@Singleton
class ConfigManager(object):
    """
    配置文件管理器
    """
    def __init__(self):
        self.zip = {}
        self.info = {}
        self.format = {}
        self.runcode = {}
        self.username = ''

    """
    加载zip文本配置
    """
    def load_zip(self):
        with open(ZipUsePath, 'rb') as handle:
            self.zip['use'] = handle.read().decode()

    """
    加载info文本配置
    """
    def load_info(self):
        with open(InfoUserPath, 'rb') as handle:
            self.info['user'] = handle.read().decode()
        with open(InfoChatPath, 'rb') as handle:
            self.info['chat'] = handle.read().decode()
        with open(InfoChannelPath, 'rb') as handle:
            self.info['channel'] = handle.read().decode()

    """
    加载format文本配置
    """
    def load_format(self):
        with open(FormatResPath, 'rb') as handle:
            self.format['res'] = handle.read().decode()

    """
    加载runcode文本配置
    """
    def load_runcode(self):
        with open(RuncodeResPath, 'rb') as handle:
            self.runcode['res'] = handle.read().decode()
        with open(RuncodeUsePath, 'rb') as handle:
            self.runcode['use'] = handle.read().decode()

    """
    获取机器人用户名
    """
    def get_bot_username(self):
        bot = Bot(os.environ['TELEGRAM_BOT_TOKEN'])
        self.username = bot.get_me().username
        return self.username
