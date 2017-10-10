# -*- coding:utf-8 -*-

import time
import logging
import requests
import threading
import threadpool
from typing import Callable
from .supported import table

headers = {"content-type": "text/plain"}
url = 'https://www.runoob.com/api/compile.php'

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

    def async(self, lang: str, code: str, callback: Callable[[str], None]):
        """
        异步POST请求
        """
        lang_code = table.get(lang)
        if lang_code == None:
            callback('不支持此语言')
        else:
            message = ([lang_code, code, callback], None)
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

    def _request(self, lang_code, code, callback):
        """
        执行Post请求
        """
        try:
            data = {'language': lang_code, 'code': code}
            req = requests.post(url, data=data, headers=headers)
            if req.status_code != 200:
                return '运行错误，请稍后重试'
            d = req.json()
            if d['output'] == '':
                return d['errors']
            return d['output']
        except Exception as e:
            logging.error(e)
            return '运行错误，请稍后重试'

    def _response(slef, request, response):
        """
        Post请求响应事件
        """
        try:
            _, _, callback = request.args
            callback(response)
        except Exception as e:
            logging.error(e)
