# -*- coding:utf-8 -*-

import re
import logging
from runoob import workers
from telegram import ParseMode
from .config import ConfigManager

def handle(bot, update):
    """
    处理执行代码请求
    """
    try:
        _handle(bot, update)
    except Exception as e:
        logging.error(e)

def _handle(bot, update):
    message = update.message
    message_id = update.message.message_id
    if message.reply_to_message == None:
        r = re.match('^/run (\w+) ([\s\S]*?)$', message.text)
        if r == None:
            username = ConfigManager().username
            pattern = '^/run@{0} (\w+) ([\s\S]*?)$'.format(username)
            r = re.match(pattern, message.text)
        if r == None:
            text = ConfigManager().runcode.get('use')
            update.message.reply_text(text, reply_to_message_id=message_id)
        else:
            lang, code = r.groups()
            text = ConfigManager().runcode.get('res')
            workers.async(lang, code, lambda res: message.reply_text(text.format(res), ParseMode.MARKDOWN, reply_to_message_id=message_id))
    else:
        r = re.match('^/run (\w+)$', message.text)
        if r == None:
            username = ConfigManager().username
            pattern = '^/run@{0} (\w+)$'.format(username)
            r = re.match(pattern, message.text)
        if r == None:
            text = ConfigManager().runcode.get('use')
            update.message.reply_text(text, reply_to_message_id=message_id)
        else:
            lang = r.groups()[0]
            code = message.reply_to_message.text
            text = ConfigManager().runcode.get('res')
            workers.async(lang, code, lambda res: message.reply_to_message.reply_text(text.format(res), ParseMode.MARKDOWN, reply_to_message_id=message_id))
