# -*- encoding:utf-8 -*-
"""
    日志辅助类
"""

import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from ..core.storage import context
from ..core import env
from ..core.env import EModeType
from ..core.producer import LogProduce

level_num_dic = {"error":"0", "warn":"1", "info":"2", "debug":"3", "fatal":"4"}

class LogHelper:
    def __init__(self):
        self._pool = ThreadPoolExecutor(max_workers=10)

    @classmethod
    def info(self, msg):
        log_info = "{0} {1}: {2}".format(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),'[INFO]',msg)
        level_num = level_num_dic["info"]
        logging.info(msg)
        print(log_info)
        now_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")

        if env.get_mode == EModeType.BACKTEST:
            LogProduce((context.backtestid, log_info, level_num, now_time, now_time))
        else:
            LogProduce((context.paperid, log_info, level_num, now_time, now_time))

    @classmethod
    def error(self,msg, error = ""):
        log_info = "{0} {1}: {2} {3}".format(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),'[ERROR] ',msg, error)
        level_num = level_num_dic["error"]
        now_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")

        if env.get_mode == EModeType.BACKTEST:
            LogProduce((context.backtestid, log_info, level_num, now_time, now_time))
        else:
            LogProduce((context.paperid, log_info, level_num, now_time, now_time))
        print(str(log_info))
        logging.error(msg)

    @classmethod
    def debug(self, msg):
        log_info = "{0} {1}: {2}".format(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),'[DEBUG]',msg)
        level_num = level_num_dic["debug"]
        logging.debug(msg)
        print(log_info)
        now_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")

        if env.get_mode == EModeType.BACKTEST:
            LogProduce((context.backtestid, log_info, level_num, now_time, now_time))
        else:
            LogProduce((context.paperid, log_info, level_num, now_time, now_time))

    @classmethod
    def warn(self, msg):
        log_info = "{0} {1}: {2}".format(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),'[WARN]',msg)
        level_num = level_num_dic["warn"]
        logging.warn(msg)
        print(log_info)
        now_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")

        if env.get_mode == EModeType.BACKTEST:
            LogProduce((context.backtestid, log_info, level_num, now_time, now_time))
        else:
            LogProduce((context.paperid, log_info, level_num, now_time, now_time))

    @classmethod
    def fatal(self,msg):
        log_info = "{0} {1}: {2}".format(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),'[FATAL]',msg)
        level_num = level_num_dic["fatal"]
        logging.critical(msg)
        print(log_info)
        now_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")

        if env.get_mode == EModeType.BACKTEST:
            LogProduce((context.backtestid, log_info, level_num, now_time, now_time))
        else:
            LogProduce((context.paperid, log_info, level_num, now_time, now_time))