# -*- coding:utf-8 -*-

import io
import json
import demjson
import logging
from xml.dom import minidom
from telegram import ParseMode
from .config import ConfigManager

def handle(bot, update):
    """
    处理格式化代码请求
    """
    try:
        _handle(bot, update)
    except Exception as e:
        logging.error(e)

def _handle(bot, update):
    message = update.message
    message_id = update.message.message_id
    reply_to_message = message.reply_to_message
    if reply_to_message == None:
        message.reply_text('必须 *Reply* 文本消息', ParseMode.MARKDOWN, reply_to_message_id=message_id)
    else:
        reply = '不支持的文本格式。'
        text = ConfigManager().format.get('res')
        if _is_xml(reply_to_message.text):
            reply = _format_xml(reply_to_message.text)
            reply = text.format(reply)
        elif _is_json(reply_to_message.text):
            reply = _format_json(reply_to_message.text)
            reply = text.format(reply)
        message.reply_text(reply, ParseMode.MARKDOWN, reply_to_message_id=message_id)

def _is_xml(xml: str):
    """
    是否xml
    """
    try:
        xmlio = io.StringIO(xml)
        minidom.parse(xmlio)
        return True
    except Exception as e:
        return False

def _is_json(jsb: str):
    """
    是否json
    """
    try:
        demjson.decode(jsb)
        return True
    except demjson.JSONException as e:
        return False

def _format_xml(xml: str):
    """
    格式化xml
    """
    try:
        out = io.StringIO()
        xmlio = io.StringIO(xml)
        doc = minidom.parse(xmlio)
        doc.writexml(out, addindent='  ', newl='\n', encoding='utf-8')
        return out.getvalue()
    except Exception as e:
        return e.args[0]

def _format_json(jsb: bytearray):
    """
    格式化json
    """
    try:
        loads = demjson.decode(jsb)
        return json.dumps(loads, indent=4, sort_keys=False, ensure_ascii=False)
    except demjson.JSONException as e:
        reason, field = e.args
        return "'{0}', '{1}'".format(reason, field)
