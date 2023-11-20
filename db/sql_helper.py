import pyodbc

class SQLHelper(object):

    @staticmethod
    def open():
        # 使用配置文件中的数据库设置
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=BBS;UID=Hynog1;PWD=123456;CHARSET=UTF-8')
        cursor = conn.cursor()
        return conn, cursor

    @staticmethod
    def close(conn, cursor):
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def fetch_one(cls, sql, args=None):
        conn, cursor = cls.open()
        cursor.execute(sql, args)
        obj = cursor.fetchone()
        cls.close(conn, cursor)
        return obj

    @classmethod
    def fetch_all(cls, sql, args=None):
        conn, cursor = cls.open()
        cursor.execute(sql, args)
        obj = cursor.fetchall()
        cls.close(conn, cursor)
        return obj

    @classmethod
    def execute(cls, sql, args=None):
        conn, cursor = cls.open()
        effect_row = cursor.execute(sql, args)
        cls.close(conn, cursor)
        return effect_row
