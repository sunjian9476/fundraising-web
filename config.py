import pymysql

mysql_host = 'localhost'
user = 'root'
password = '123456'
db_name = 'fundraising'


def create_connection():
    conn = pymysql.connect(host=mysql_host,
                           user=user,
                           password=password,
                           db=db_name)
    return conn

