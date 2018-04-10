# -* - coding: UTF-8 -* -

import os


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


print(str(disk_usage("/")) + "%")