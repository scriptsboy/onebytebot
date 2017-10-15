# -*- coding:utf-8 -*-

import logging
from .config import ConfigManager

def handle(bot, update):
    """
    处理获取当前对话框信息
    """
    try:
        _handle(bot, update)
    except Exception as e:
        logging.error(e)

def _handle(bot, update):
    chat = update.message.chat
    message_id = update.message.message_id
    if chat.type == 'private':
        text = ConfigManager().info.get('user')
        reply = text.format(chat.id, chat.username, chat.first_name)
        update.message.reply_text(reply, reply_to_message_id=message_id)
    elif chat.type == 'group':
        text = ConfigManager().info.get('chat')
        update.message.reply_text(text.format(chat.id, chat.title), reply_to_message_id=message_id)
    elif chat.type == 'supergroup':
        text = ConfigManager().info.get('channel')
        update.message.reply_text(text.format(chat.id, chat.title), reply_to_message_id=message_id)
