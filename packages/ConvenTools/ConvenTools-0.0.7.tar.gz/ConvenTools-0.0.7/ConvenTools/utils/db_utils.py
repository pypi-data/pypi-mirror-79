import pymysql

class db_utils():

    def __init__(self,host,user,port,password,dbName):
        self.host = host
        self.user = user
        self.port = port
        self.password = password
        self.connect = pymysql.connect(host=host, port=port, user=user, passwd=password, db=dbName, charset='utf8',cursorclass=pymysql.cursors.DictCursor)

    def execute_by_sqlstr_to_jsondata(self, sqlstr):
        cursor = self.connect.cursor()
        cursor.execute(sqlstr)
        cursor.close()
        return cursor.fetchall()

    def execute_sql_to_str(self,sqlstr):
        cursor = self.connect.cursor()
        cursor.execute(sqlstr)
        return cursor

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


