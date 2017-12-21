# -*- coding:utf-8 -*-

import io
import os
import time
import zipfile
import logging
import threading
import threadpool
from typing import Callable
from telegram.bot import Bot

class WorkerPool(object):
    """
    工作线程池
    用于异步POST请求

    """
    def __init__(self, num_workers):
        self._clean = False
        self._finished = False
        self._pool = threadpool.ThreadPool(num_workers)
        self._thread = threading.Thread(target=self._run)
        self._thread.start()

    def async(self, frommsg: object, setname: str, callback: Callable[[str, str], None]):
        """
        异步POST请求
        """
        message = ([frommsg, setname, callback], None)
        messages = threadpool.makeRequests(self._request, [message], self._response)
        self._pool.putRequest(messages[0])

    def terminate(self):
        if not self._finished:
            self._finished = True
            while not self._clean:
                time.sleep(0.001)

    def _run(self):
        while not self._finished:
            try:
                self._pool.poll()
                time.sleep(0.001)
            except threadpool.NoResultsPending as e:
                pass
            except threadpool.NoWorkersAvailable as e:
                pass
        self._clean = True

    def _download_stickers_set(self, setname: str):
        """s
        下载stickers集合
        """
        files = []
        emojis = []
        bot = Bot(os.environ['TELEGRAM_BOT_TOKEN'])
        sticker_set = bot.get_sticker_set(setname)
        for sticker in sticker_set.stickers: 
            file = bot.get_file(sticker.file_id)
            buffer = io.BytesIO()
            file.download(out=buffer)
            filename = os.path.basename(file.file_path)
            _, ext = os.path.splitext(filename)
            if ext == '':
                filename = filename + '.webp'
            files.append((filename, buffer))
            if sticker.emoji != None:
                if len(sticker.emoji) == 1:
                    emojis.append((filename, sticker.emoji))
                else:
                    emojis.append((filename, sticker.emoji[0]))
        return files, emojis

    def _zip_stickers_set(self, files : list, emojis : list):
        """
        打包stickers为压缩文件
        """
        stickers = ''
        for idx, pair in enumerate(emojis):
            filename, emoji = pair
            stickers = stickers + filename + ' ---- ' + emoji
            if idx != len(emojis) - 1:
                stickers = stickers + '\n'

        buffer = io.BytesIO()
        zip = zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED)
        for file in files:
            filename, fileio = file
            zip.writestr(filename, fileio.getvalue())
        zip.writestr('emojis.txt', stickers)
        zip.close()
        buffer.seek(0)
        return buffer

    def _request(self, frommsg, setname, callback):
        """
        执行下载请求
        """
        try:
            message_id = frommsg.message_id
            files, emojis = self._download_stickers_set(setname)
            zipbytes = self._zip_stickers_set(files, emojis)
            bot = Bot(os.environ['TELEGRAM_BOT_TOKEN'])
            bot.send_document(frommsg.chat.id, zipbytes, setname+'.zip', 'Stickers集合压缩包', reply_to_message_id=message_id)
            return None
        except Exception as e:
            logging.error(e)
            return '下载Stickers集合失败，请稍后重试！'

    def _response(slef, request, error):
        """
        请求下载结果
        """
        try:
            _, setname, callback = request.args
            if error != None:
                callback(setname, error)
        except Exception as e:
            logging.error(e)
