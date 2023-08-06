import time

#默认的规范格式
DEFUAL_FORMAT_STR = '%Y-%m-%d %H:%M:%S'

#2020_10_10_10_10_10 一般用户生成文件夹
YYYY_MM_DD_HH_MM_SS = "%Y_%m_%d_%H_%M_%S"

# 年月日
YYYY_MM_DD = "%Y-%m-%d"


def str_to_timestamp(str_time=None, format=DEFUAL_FORMAT_STR):
    """
    把格式化时间转换成时间戳
    :param str_time:
    :param format:
    :return: 时间搓 秒级
    """
    if str_time:
        time_tuple = time.strptime(str_time, format)  # 把格式化好的时间转换成元祖
        result = time.mktime(time_tuple)  # 把时间元祖转换成时间戳
        return int(result)
    return int(time.time())


def timestamp_to_str(timestamp=None, format=DEFUAL_FORMAT_STR):
    """
    把时间戳转换成格式化
    :param timestamp:
    :param format:
    :return: 格式化的字符串
    """
    if timestamp:
        time_tuple = time.localtime(timestamp)  # 把时间戳转换成时间元祖
        result = time.strftime(format, time_tuple)  # 把时间元祖转换成格式化好的时间
        return result
    else:
        return time.strptime(format)


def get_current_to_format(format=DEFUAL_FORMAT_STR):
    """
    获取当前时间的格式化字符串
    :param format:
    :return:  格式化后的时间字符串
    """
    currentTime = time.time()
    return timestamp_to_str(currentTime,format)



def get_current_time():
    """
    获取当前时间秒数
    :return: 当前时间时间搓，秒级
    """
    return time.time()