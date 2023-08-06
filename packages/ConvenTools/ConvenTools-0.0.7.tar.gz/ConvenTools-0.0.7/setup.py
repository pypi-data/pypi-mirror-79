import setuptools

setuptools.setup(
    name='ConvenTools',
    version='0.0.7',
    author='lueans',
    author_email='2427770136@qq.com',
    description='This is a python toolbox，It is mainly used for database operation and excel operation',

    url='https://www.github.com/lueans',
    packages=setuptools.find_packages(),  # 这里是所有代码所在的文件夹名称
    install_requires=[
        'jdcal', 'et-xmlfile', 'openpyxl', 'PyMySQL', 'xlrd',
        'xlutils', 'xlwt'
    ],
)
