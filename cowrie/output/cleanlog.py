# -* - coding: UTF-8 -* -

"""
Docstring
"""

from __future__ import division, absolute_import

import datetime
import os
import threading

import cowrie.core.output
import cowrie.python.logfile

from cowrie.core.config import CONFIG
from cowrie.files.cleaner import Cleaner


class Output(cowrie.core.output.Output):
    """
    Docstring class
    """

    free_percent = 50
    check_span_minutes = 30
    thread_run_time = datetime.datetime.now()

    def __init__(self):
        cowrie.core.output.Output.__init__(self)
        fn = CONFIG.get('output_cleanlog', 'logfile')
        self.free_percent = int(CONFIG.get('output_cleanlog', 'free_percent'))
        self.check_span_minutes = int(CONFIG.get('output_cleanlog', 'check_span_minutes'))
        dirs = os.path.dirname(fn)
        base = os.path.basename(fn)
        self.cleaner = Cleaner(dirs, base)
        self.cleaner.start()
        self.thread_start_check(self.free_percent, 0)

    def do_check(self, free_percent, check_span_minutes):
        """

        :return:
        """
        try:
            self.cleaner.write_log("The disk_check_minutes is: " + str(check_span_minutes))
            self.cleaner.write_log("The free_percent is: " + str(free_percent))
            self.cleaner.check_disk(free_percent)
        except IOError:
            print "Error: "
        else:
            print "do_check 执行成功"

    def thread_start_check(self, free_percent, check_span_minutes):
        """

        :return:
        """
        # 计算两个时间之间相隔的秒数

        time_span_seconds = (datetime.datetime.now()-self.thread_run_time).total_seconds()
        print(time_span_seconds)
        check_span_seconds = int(60*check_span_minutes)
        print(check_span_seconds)
        # 如果间隔大于 指定的 分钟 就 开启一次检查
        if time_span_seconds > check_span_seconds:
            t = threading.Thread(target=self.do_check,
                                 args=(free_percent, check_span_minutes))
            # 测试 先不放到线程中
            # self.do_check(free_percent, check_span_minutes)

            self.thread_run_time = datetime.datetime.now()
            t.start()

    def start(self):
        """
        """

        pass

    def stop(self):
        """
        """

    def write(self, log_entry):
        """

        """
        self.thread_start_check(self.free_percent, self.check_span_minutes)