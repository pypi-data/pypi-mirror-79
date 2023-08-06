import pymysql

class MySQLUtil():
    """
    MySQL 数据库工具类
    """
    def __init__(self,host,user,port,password,dbName):
        """
        初始化操作
        :param host: 主机
        :param user:  用户名
        :param port: 端口号
        :param password: 密码
        :param dbName: 数据库名称
        """
        self.host = host
        self.user = user
        self.port = port
        self.password = password
        self.connect = pymysql.connect(host=host, port=port, user=user, passwd=password, db=dbName, charset='utf8',cursorclass=pymysql.cursors.DictCursor)

    def execute_to_Json(self, sqlstr):
        """
        执行sql返回json对象
        :param sqlstr:
        :return:
        """
        cursor = self.connect.cursor()
        cursor.execute(sqlstr)
        cursor.close()
        return cursor.fetchall()

    def close(self):
        self.connect.close()

    def execute_sql_list(self,sqlList):
        """
        执行多个sql
        :param sqlList:
        :return:
        """
        cursor = self.connect.cursor()
        try:
            for sqlItem in sqlList:
                cursor.execute(sqlItem)
        except Exception as e:
            print('事务处理失败', e)
        else:
            self.connect.commit()  # 事务提交
            print('事务处理成功', cursor.rowcount)  # 关闭连接
            cursor.close()


