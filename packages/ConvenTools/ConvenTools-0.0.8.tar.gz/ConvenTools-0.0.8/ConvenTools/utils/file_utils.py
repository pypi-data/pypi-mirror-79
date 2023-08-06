import os
from pathlib import Path
import shutil
import json


#-----------------   文件夹工具  ------------------------
def mkdirs(path):
    """
    创建多级目录
    :param path:
    :return: True or false
    """
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False


def get_child(path):
    """
    获取文件夹下面的文件夹和文件，一级获取
    :param path:
    :return:
    """
    return os.listdir(path)


def get_child_dir(path):
    """
    获取文件夹下面的子文件夹,一级获取
    :param path:
    :return: 全部文件夹列表，如果没有返回空数组
    """
    list =get_child(path)
    newList = []
    for item in list:
        newStr = r"{0}\{1}".format(path, item)
        if (os.path.isdir(newStr)):
            newList.append(newStr)
    return newList


def get_child_file(path):
    """
    获取文件夹下的子文件，一级获取
    :param path:
    :return:
    """
    list = get_child(path)
    newList = []
    for item in list:
        newStr = r"{0}\{1}".format(path, item)
        if (os.path.isdir(newStr) == False):
            newList.append(newStr)
    return newList



# 获取文件夹下面的全部文件,返回文件绝对路径数组
def get_child_file_all(path):
    """
    获取文件夹下面的全部文件，
    :param path:
    :return:
    """
    newFileList = []
    for root, dirs, files in os.walk(path):
        newFileList += [root + "\\" + fileName for fileName in files]
    return newFileList


#-----------------------   文件操作  --------------------------
def mknod(filePath):
    """
    创建文件
    :param filePath:
    :return:
    """
    my_file = Path(filePath)
    if(my_file.exists()):
        print("文件已经存在")
    else:
        os.mknod(filePath)

def write(filePath,content,mode = "w+"):
    """
    创建文件，并将内容写入到文件
    mode is an optional string that specifies the mode in which the file
    is opened. It defaults to 'r' which means open for reading in text
    mode.  Other common values are 'w' for writing (truncating the file if
    it already exists), 'x' for creating and writing to a new file, and
    'a' for appending (which on some Unix systems, means that all writes
    append to the end of the file regardless of the current seek position).
    In text mode, if encoding is not specified the encoding used is platform
    dependent: locale.getpreferredencoding(False) is called to get the
    current locale encoding. (For reading and writing raw bytes use binary
    mode and leave encoding unspecified.) The available modes are:

    :param filePath:
    :param content:
    :return:
    """
    with open(filePath, mode) as f:
        f.write(content)

def write_json_file(filePath,jsonContent):
    """
    写入json文件
    :param filePath:
    :param jsonContent:
    :return:
    """
    with open(filePath, "w+") as f:
        f.write(json.dumps(jsonContent, indent=4,ensure_ascii=False))


def read(filePath):
    """
    读文件
    :param filePath:
    :return: 返回文件内容
    """
    data = ""
    with open(filePath, 'r') as f:
        data = f
    return data


def read_json_file(filePath):
    """
    读取json文件内容
    :param filePath:
    :return: json dist对象
    """
    data = {}
    with open(filePath, 'r') as f:
        data = json.load(f)
    return data


#-----------   copy remove del -----------------------
# 删除文件，文件夹，复制拷贝，移动


