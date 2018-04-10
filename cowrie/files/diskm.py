# -* - coding: UTF-8 -* -
import datetime
import os
import random
import shutil


class diskM:
    """
    Docstring class

    """

    def __int__(self):
        """

        :return:
        """
        pass

    def test(self):
        """

        :return:
        """

        file_path = "/Users/luweiping/PycharmProjects/cowrie/log"

        json_file_name = "cowrie.json"
        log_file_name = "cowrie.log"

        for num in range(12):
            src_file = file_path + "/" + json_file_name
            self.copy_file(src_file, src_file + "_2018-02-08_" + str(num))

            src_file = file_path + "/" + log_file_name
            self.copy_file(src_file, src_file + "_2018-03-08_" + str(num))

    def generate_days_log(self, days):
        """

        :return:
        """
        file_path = "/Users/luweiping/PycharmProjects/cowrie/log"

        json_file_name = "data_120m.json"
        log_file_name = "data_120m.log"
        src_file_json = file_path + "/" + json_file_name
        src_file_log = file_path + "/" + log_file_name

        date = datetime.datetime.now() - datetime.timedelta(days=2)
        for num in range(days):
            date_str = date.strftime('.%Y-%m-%d')
            self.copy_file(src_file_json, file_path+"/cowrie.json" + date_str)
            self.copy_file(src_file_log, file_path+"/cowrie.log" + date_str)
            date = date - datetime.timedelta(days=1)  # 减少一天 timedelta是一个不错的函数

    def genSizeFile(self, fileName, fileSize):
        # file path
        root_path = "/Users/luweiping/PycharmProjects/cowrie/log"
        filePath = root_path + "/Data" + fileName + ".txt"

        # 生成固定大小的文件
        # date size
        ds = 0
        with open(filePath, "w") as f:
            while ds < fileSize:
                f.write(str(round(random.uniform(-1000, 1000), 2)))
                f.write("\n")
                ds = os.path.getsize(filePath)
        # print(os.path.getsize(filePath))

    @staticmethod
    def pre_month_last_day(time):
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
        # first_day_of_pre_month = datetime.date(pre_month.year, pre_month.month, 1)
        return pre_month_last_day

    def dirlist(self):
        """

        :return:
        """
        dirs = [d for d in os.listdir('../../var/log/cowrie')]
        print(dirs)

    @staticmethod
    def copy_file(src_file, dst_file):
        """

        :param src_file:
        :param dst_file:
        :return:
        """

        if not os.path.isfile(src_file):
            print "%s not exist!" %src_file
        else:
            file_path, file_name = os.path.split(dst_file)  # 分离文件名和路径
            if not os.path.exists(file_path):
                os.makedirs(file_path)  # 创建路径
            shutil.copyfile(src_file, dst_file)  # 复制文件
            print "copy %s -> %s" % (src_file, dst_file)


diskm = diskM()

diskm.generate_days_log(55)

# genSizeFile("1k",1*1024)
# diskm.genSizeFile("_50M_", 1 * 1024*1024*50)
