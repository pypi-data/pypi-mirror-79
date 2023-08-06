# 数据库设计报告生成器
# 根据数据库，反向生成数据库报告

from ConvenTools.utils.db_utils.MySQL_util import MySQLUtil
import time
from docxtpl import DocxTemplate




class DbDesignGenerator:
    """
    使用要求，数据库必须设置主键，外键，表名称备注中文，字段备注中文
    """

    def __init__(self, host, port, user, password, dbName):
        """
        初始化操作
        :param host: 主机
        :param port: 端口号
        :param user:  用户名
        :param password: 密码
        :param dbName: 数据库名称
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.dbName = dbName

    def init_sql_utils(self):
        self.sqlUtil = MySQLUtil(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            dbName=self.dbName)

    def get_table_list(self):
        tablesSql = "show tables"
        return self.sqlUtil.execute_to_Json(tablesSql)

    def get_db_structure_data(self):
        sql = "SELECT distinct a.table_name, a.table_comment, b.COLUMN_NAME, b.column_comment, b.column_type, b.column_key " \
              "FROM information_schema.TABLES a,information_schema.COLUMNS b " \
              "WHERE a.table_name = b.TABLE_NAME " \
              "AND a.table_schema = '{0}' " \
              "AND b.table_schema = '{0}' " \
              "AND b.column_comment is not NULL " \
              "AND b.column_comment <> ''".format(self.dbName)
        return self.sqlUtil.execute_to_Json(sql)


    def generate(self,db_design_data, template_File_Path, out_File_Path = "./Simple.docx"):

        tpl = DocxTemplate(template_File_Path)

        context = {
            "tableList": db_design_data,
        }

        tpl.render(context)
        tpl.save(out_File_Path)

    def simple_generate(self,template_File_Path, out_File_Path = "./Simple.docx"):
        #获取表表列表数据
        table_list = self.get_table_list()
        #获取数据库结构逻辑
        db_structure_data = self.get_db_structure_data()

        #拼接数据
        new_table_list = []
        for tableItem in table_list:
            tableName = list(tableItem.values())[0]
            # print(tableName)
            new_table_item = {
                "name": tableName,
                "table_comment": tableName,
                "columnList": []
            }
            columnList = []
            for dataItem in db_structure_data:
                if (dataItem["table_name"] == tableName):
                    columnitem = dataItem
                    column_type = columnitem["column_type"]
                    # print(column_type)
                    try:
                        columnitem["len"] = column_type[column_type.index("(") + 1:-1]
                        columnitem["column_only_type"] = column_type[0:column_type.index("(")]
                    except:
                        columnitem["len"] = ''
                        columnitem["column_only_type"] = column_type
                    columnList.append(columnitem)
            new_table_item["columnList"] = columnList
            # 填充
            if (len(columnList) != 0 and columnList[0]["table_comment"] != ""):
                new_table_item["table_comment"] = columnList[0]["table_comment"]

            new_table_item["index"] = len(new_table_item) + 1
            new_table_list.append(new_table_item)
        #生成报告
        self.generate(db_design_data=new_table_list,template_File_Path=template_File_Path,out_File_Path=out_File_Path)










