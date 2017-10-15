# -*- coding:utf-8 -*-

import re
import logging
from stickers import workers
from .config import ConfigManager

def handle(bot, update):
    """
    处理下载stickers集合
    """
    try:
        _handle(bot, update)
    except Exception as e:
        logging.error(e)

def _handle(bot, update):
    message = update.message
    message_id = update.message.message_id
    if message.reply_to_message == None:
        r = re.match('^/zip (\w+)$', message.text)
        if r == None:
            username = ConfigManager().username
            pattern = '^/zip@{0} (\w+)$'.format(username)
            r = re.match(pattern, message.text)
        if r == None:
            text = ConfigManager().zip.get('use')
            update.message.reply_text(text, reply_to_message_id=message_id)
        else:
            setname = r.groups()[0]
            chat = update.message.chat
            workers.async(message, setname, lambda setname, error : message.reply_text(error, reply_to_message_id=message_id))      
    else:
        sticker = message.reply_to_message.sticker
        if sticker == None or message.text != '/zip':
            text = ConfigManager().zip.get('use')
            update.message.reply_text(text, reply_to_message_id=message_id) 
        else:
            if sticker.set_name == None or sticker.set_name == '':
                update.message.reply_text('无法下载此Stickers集合。', reply_to_message_id=message_id) 
            else:
                setname = sticker.set_name
                chat = update.message.chat
                workers.async(message, setname, lambda setname, error : message.reply_text(error, reply_to_message_id=message_id))  
