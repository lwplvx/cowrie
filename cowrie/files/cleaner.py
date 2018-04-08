# -* - coding: UTF-8 -* -

# 功能:读取指定目录下特定类型的文件名列表
# Data: 2018-04-08,星期日
# Author:lwp

import json
import os.path
import datetime


class Cleaner:
    """
        Docstring class
    """
    path = ""
    _filename = '/disk_cleaner.log'

    def __init__(self, path):
        """

        :param path:
        :return:
        """

        self.path = path
        self._filename = self.path + self._filename
        self.start()
        self.check_disk()

    def get_file_list(self, flags=[]):
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
                else:
                    # 默认直接返回所有文件名
                    full_file_name = os.path.join(self.path, fn)
                    file_list.append(full_file_name)

        # 对文件名排序
        # if (len(FileList)>0):
        #     FileList.sort()

        return file_list

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

    def write_log(self, msg):
        """
        记录下日志
        :param msg:
        :return: 不返回
        """
        with open(self._filename, "a") as f:
            import datetime
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')  # 现在
            f.write(now_time + "  " + msg)
            f.write('\n')
            # f.flush()
            f.close()
        return

    def check_disk(self, free_percent=35):
        """
        检查磁盘剩余空间，删除时间久的文件
        保证磁盘剩余可用剩余量在 35%（这个看情况调整）以上

        :param free_percent 希望保持的剩余空间的百分比
        :return:
        """

        if not (os.path.exists(self._filename)):
            self.start()
            self.write_log("The file '" + self._filename + "' not exists,so create it \n")

        usage = Cleaner.disk_usage(self.path)
        if (100 - usage) < free_percent:
            file_list = self.get_file_list(["json", "log"])
            # -------------

            time = datetime.datetime.now()
            # 求该月第一天
            first_day = datetime.date(time.year, time.month, 1)

            # 求前一个月的第一天
            pre_month = first_day - datetime.timedelta(days=1)  # timedelta是一个不错的函数

            # 前一个月的第一天
            first_day_of_pre_month = datetime.date(pre_month.year, pre_month.month, 1)

            # 前一个月的 日志名称包含的字符串
            flag = first_day_of_pre_month.strftime('%Y-%m')

            file_list = self.get_file_list([flag])

            can_delete_files = self.except_extension(file_list, [".json", ".log"])

            # -----------

            if len(can_delete_files) > 0:
                json_str = json.dumps(file_list)
                self.write_log("The free_percent is " + str(free_percent))
                self.write_log("The folder is '" + self.path + "'")
                self.write_log("All files (count:" + str(file_list.__len__()) + "): \n" + json_str + "\n")

                self.write_log("disk usage " + str(usage) + "%, Try to delete the old files ……")

                json_str = json.dumps(can_delete_files)
                self.write_log("Can delete files (count:" + str(can_delete_files.__len__()) + "): \n" + json_str + "\n")

                # 执行删除相关
                delete_list = Cleaner.delete_files(can_delete_files)
                json_str = json.dumps(delete_list)
                self.write_log("Success delete files (count:" + str(delete_list.__len__()) + "): \n" + json_str + "\n")

                usage = Cleaner.disk_usage(self.path)
                self.write_log("After delete, disk usage " + str(usage) + "%  ^_^ .")

        else:
            self.write_log("disk usage " + str(usage) + "% , Do not need to delete any file.")

        pass

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
            f.write("start_disk_cleaner_log at " + now_time + "\n")

            f.write("Total:" + str(Cleaner.disk_total(self.path) / 1024 / 1024 / 1024) + "GB ")
            f.write("   Free:" + str(Cleaner.disk_free(self.path) / 1024 / 1024 / 1024) + "GB ")
            f.write("   Used:" + str(Cleaner.disk_used(self.path) / 1024 / 1024 / 1024) + "GB \n")
            f.write("Usage:" + str(usage) + "% \n")
            f.write("-------------------------------------------end--\n \n")

            f.close()

        file_list = self.get_file_list(["json", "log"])
        json_str = json.dumps(file_list)

        self.write_log("The folder is '" + self.path + "'")
        self.write_log("All files (count:" + str(file_list.__len__()) + "): \n" + json_str + "\n")

    def stop(self):
        """

        :return:
        """
        pass

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
    def has_substring(substring, filename):
        """
        :param substring: 子字符串
        :param filename: 文件名
        :return: True   False
        """
        flag = False
        for item_string in substring:
            if item_string in filename:
                flag = True
            if flag:
                break

        return flag

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
            percent = ret = (float(used) / total) * 100
        except ZeroDivisionError:
            percent = 0

        return percent
