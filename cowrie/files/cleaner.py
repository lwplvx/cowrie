# -* - coding: UTF-8 -* -

# 功能:读取指定目录下特定类型的文件名列表
# Data: 2018-04-08,星期日
# Author:lwp

import json
import os.path
import datetime
import calendar


class Cleaner:
    """
        Docstring class
    """
    path = ""
    _filename = '/cleanlog.log'

    def __init__(self, path, fn):
        """
        :param path:
        :return:
        """

        self.path = path
        self._filename = self.path + "/" + fn

    def get_file_list(self, flags):
        """
         获取目录中指定的文件名
        :param flags: flags=['json','log'] 要求文件名称中包含这些字符串
        :return: 默认直接返回所有文件名,返回指定类型的文件名
        """

        import os
        file_list = []
        file_names = os.listdir(self.path)
        if len(file_names) > 0:
            for fn in file_names:
                if len(flags) > 0:
                    #  返回文件名包含指定字符
                    if Cleaner.has_substring(flags, fn):
                        full_file_name = os.path.join(self.path, fn)
                        file_list.append(full_file_name)
        return file_list

    def write_log(self, msg):
        """
        记录下日志
        :param msg:
        :return: 不返回
        """

        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')  # 现在
        data = now_time + "  " + msg + "\n"
        with open(self._filename, "a") as f:
            f.write(data)
            # f.flush()
            f.close()
        print(data)
        return

    def check_disk(self, free_percent):
        """
        删除一个月 检查一次剩余空间，满足条件就停止
        检查磁盘剩余空间，删除时间久的文件
        保证磁盘剩余可用剩余量在  如：35%（这个看情况调整）以上

        :param free_percent 希望保持的剩余空间的百分比
        :return:
        """
        # 如果清理功能的日志文件不存在就创建
        if not (os.path.exists(self._filename)):
            self.start()
            self.write_log("The file '" + self._filename + "' not exists,so create it \n")

        # 如果剩余用量不满足条件
        if not self.is_free_percent_ok(free_percent):
            # 时间，往前推 500 天 开始找文件
            now = datetime.datetime.now()
            today = datetime.date(now.year, now.month, now.day)
            pre_500_days = now - datetime.timedelta(days=500)
            first_day_of_delete_month = Cleaner.get_first_day_of_pre_month(pre_500_days)
            while (not self.is_free_percent_ok(free_percent)) and first_day_of_delete_month < today:
                self.delete_one_month(first_day_of_delete_month)
                first_day_of_delete_month = Cleaner.get_first_day_of_next_month(first_day_of_delete_month)

            usage = Cleaner.disk_usage(self.path)
            self.write_log("After deleted, disk usage is " + str(usage) + "% , ^_^ \n")
        else:
            usage = Cleaner.disk_usage(self.path)
            self.write_log("Checking done! disk usage " + str(usage) + "% , Do not to delete any file.\n")

    def is_free_percent_ok(self, free_percent):
        """

        :param free_percent:
        :return:
        """

        usage = Cleaner.disk_usage(self.path)
        # 如果用量 大于指定的用量
        if usage > (100 - int(free_percent)):
            return False
        return True

    def delete_one_month(self, first_day_of_month):
        """

        :param first_day_of_month:
        :return:
        """
        date_flag = first_day_of_month.strftime('%Y-%m')
        print(date_flag, "   date_flag  115 ")

        file_list = self.get_file_list([date_flag])

        print(date_flag + " , this month has files:" + str(len(file_list)))
        if len(file_list) > 0:
            self.write_log("The folder is '" + self.path + "'")
            self.write_log("Try to delete the month " + date_flag + " files:")
            self.write_log(date_flag + " files count:" + str(len(file_list)))
            can_delete_files = Cleaner.except_extension(file_list, [".json", ".log"])
            self.do_delete_files(can_delete_files)

    def do_delete_files(self, can_delete_files):
        """

        :param can_delete_files:
        :param file_list:
        :return:
        """
        if len(can_delete_files) > 0:
            # 执行删除相关
            delete_list = Cleaner.delete_files(can_delete_files)
            self.write_log("Success deleted files (count:" + str(len(delete_list)) + "):")
            self.write_log(json.dumps(delete_list) + "\n")

        else:
            self.write_log("Can delete files is 0.  ~_~ !")

    def start(self):
        """
        清除 扫描日志文件，加入一行文件建立日志
        :return: 不返回
        """
        usage = Cleaner.disk_usage(self.path)
        with open(self._filename, "w") as f:
            import datetime
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f  ')  # 现在

            f.write("--start-----------------------------------------\n")
            f.write("_filename : " + self._filename + "\n")
            f.write("path: " + self.path + "\n")
            f.write("start_disk_cleaner_log at " + now_time + "\n")

            f.write("Total:" + str(Cleaner.disk_total(self.path) / 1024 / 1024 / 1024) + "GB ")
            f.write("   Free:" + str(Cleaner.disk_free(self.path) / 1024 / 1024 / 1024) + "GB ")
            f.write("   Used:" + str(Cleaner.disk_used(self.path) / 1024 / 1024 / 1024) + "GB \n")
            f.write("Usage:" + str(usage) + "% \n")
            f.write("-------------------------------------------end--\n")

            f.close()

        file_list = self.get_file_list(["json", "log"])
        self.write_log("The folder is '" + self.path + "'")
        self.write_log("Files(" + str(len(file_list)) + ")\n")

    def stop(self):
        """

        :return:
        """
        pass

    @staticmethod
    def get_first_day_of_pre_month(time):
        """
        获取指定时间的前一个月的最后一天
        :param time:
        :return: pre_month_last_day 前一个月的最后一天
        """
        # 求该月第一天
        first_day = datetime.date(time.year, time.month, 1)
        # 求前一个月的第一天
        pre_month_last_day = first_day - datetime.timedelta(days=1)  # timedelta是一个不错的函数
        # 前一个月的第一天
        first_day_of_pre_month = datetime.date(pre_month_last_day.year, pre_month_last_day.month, 1)
        return first_day_of_pre_month

    @staticmethod
    def get_first_day_of_next_month(time):
        """

        :param time:
        :return:
        """
        # 求该月第一天
        first_day = datetime.date(time.year, time.month, 1)
        # 求后一个月的第一天
        days_num = calendar.monthrange(first_day.year, first_day.month)[1]  # 获取一个月有多少天
        first_day_of_next_month = first_day + datetime.timedelta(days=days_num)  # 当月的最后一天只需要days_num-1即可
        return first_day_of_next_month

    @staticmethod
    def delete_files(file_list):
        """

        :param file_list:
        :return: delete file list
        """
        delete_list = []

        if len(file_list) > 0:
            for fn in file_list:
                os.remove(fn)
                delete_list.append(fn)
        return delete_list

    @staticmethod
    def file_extension(filename):
        """
        获取文件的扩展名
        :param filename:
        :return:
        """

        return os.path.splitext(filename)[1]

    @staticmethod
    def has_extensions(extensions, filename):
        """
        :param extensions: 扩展名列表
        :param filename: 文件名
        :return: True   False
        """
        flag = False
        for extension in extensions:
            if extension == Cleaner.file_extension(filename):
                flag = True
            if flag:
                break

        return flag

    @staticmethod
    def has_substring(flags, filename):
        """
        :param flags: 一些子字符串
        :param filename: 文件名
        :return: True Or False
        """
        for item_flag in flags:
            if item_flag in filename:
                return True
        return False

    @staticmethod
    def except_extension(file_names, extensions=[]):
        """
         指定扩展名除外
        :param file_names
        :param extensions:一些扩展名
        :return: 过滤后的文件名列表
        """
        file_list = []
        if len(file_names) > 0:
            for fn in file_names:
                if len(extensions) > 0:
                    #  指定扩展名除外
                    if not Cleaner.has_extensions(extensions, fn):
                        file_list.append(fn)
                else:
                    # 默认直接返回所有文件名
                    file_list.append(fn)
        return file_list

    @staticmethod
    def except_flags(file_names, flags=[]):
        """
         指定扩展名除外
        :param file_names
        :param flags:一些字符串
        :return: 过滤后的文件名列表
        """
        file_list = []
        if len(file_names) > 0:
            for fn in file_names:
                if len(flags) > 0:
                    #  包含指定字符的除外
                    if not Cleaner.has_substring(flags, fn):
                        file_list.append(fn)
                else:
                    # 默认直接返回所有文件名
                    file_list.append(fn)
        return file_list

    @staticmethod
    def disk_total(path):
        """
        Return disk total associated with path.
        :param path
        :return 总共空间

        """
        st = os.statvfs(path)
        total = (st.f_blocks * st.f_frsize)
        return total

    @staticmethod
    def disk_used(path):
        """
        Return disk uses associated with path.
        :param path
        :return used

        """
        st = os.statvfs(path)
        used = (st.f_blocks - st.f_bfree) * st.f_frsize
        return used

    @staticmethod
    def disk_free(path):
        """
        Return disk free associated with path.
        :param path
        :return free

        """
        st = os.statvfs(path)
        free = (st.f_bavail * st.f_frsize)

        return free

    @staticmethod
    def disk_usage(path):
        """
        Return disk usage associated with path.
        :param path
        :return 百分比

        """
        st = os.statvfs(path)
        total = (st.f_blocks * st.f_frsize)
        used = (st.f_blocks - st.f_bfree) * st.f_frsize
        try:
            percent = (float(used) / total) * 100
        except ZeroDivisionError:
            percent = 0

        return percent
