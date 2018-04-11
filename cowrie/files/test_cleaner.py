from cowrie.files.cleaner import Cleaner


def test():
    """

    :return:
    """
    dirs = "/Users/luweiping/PycharmProjects/cowrie/log"
    base = "cleanlog.log"
    cleaner = Cleaner(dirs, base)
    cleaner.start()
    cleaner.check_disk(80)


test()