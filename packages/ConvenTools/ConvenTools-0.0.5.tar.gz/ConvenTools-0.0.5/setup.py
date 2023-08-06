from setuptools import find_packages, setup

setup(
    name='ConvenTools',
    version='0.0.5',
    description='This is a python toolbox，It is mainly used for database operation and excel operation',
    author='lueans',  # 作者
    author_email='2427770136@qq.com',
    url='https://www.github.com/lueans',
    packages=['ConvenTools'],  # 这里是所有代码所在的文件夹名称
    install_requires=[
        'jdcal', 'et-xmlfile', 'openpyxl', 'PyMySQL','xlrd',
        'xlutils', 'xlwt'
                      ],
)
