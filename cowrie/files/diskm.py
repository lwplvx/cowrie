# -* - coding: UTF-8 -* -

import os
import shutil

import cowrie
from cowrie.core.config import CONFIG


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

        for num in range(15):
            src_file = file_path + "/" + json_file_name
            self.copy_file(src_file, src_file + "_2018-04-08_" + str(num))

            src_file = file_path + "/" + log_file_name
            self.copy_file(src_file, src_file + "_2018-03-08_" + str(num))

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

diskm.test()
