import os
from pathlib import Path


#创建文件目录
def mkdir(path):
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


#创建文件
def mknod(filePath):
    my_file = Path(filePath)
    if(my_file.exists()):
        print("文件已经存在")
    else:
        os.mknod(filePath)

# 获取文件夹下面的子文件夹
def get_child_dir(path):
    list = os.listdir(path)
    newList = []
    for item in list:
        newStr = r"{0}\{1}".format(path, item)
        if (os.path.isdir(newStr)):
            newList.append(newStr)
    return newList


# 获取文件夹下面的全部文件,返回文件绝对路径数组
def get_allFile_by_path(path):
    newFileList = []
    for root, dirs, files in os.walk(path):
        print(root)
        print(dirs)
        print(files)
        newFileList += [root + "\\" + fileName for fileName in files]
    return newFileList



#创建并编辑文件
def write(filePath,content):
    with open(filePath, 'w+') as f:
        f.write(content)