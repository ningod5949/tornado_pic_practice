from sqlalchemy import create_engine
# 数据库ORM工具               工具
from sqlalchemy.ext.declarative import declarative_base
                # 扩展 说明
from sqlalchemy.orm import sessionmaker


HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'test1'
USERNAME = 'admin'
PASSWORD = 'Root110qwe'

DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
    USERNAME, PASSWORD, HOST, PORT, DATABASE
)

engine = create_engine(DB_URI)

Base = declarative_base(engine)
Session = sessionmaker(bind=engine)
# bind 捆绑

if __name__ == '__main__':
    connection = engine.connect()
    result = connection.execute('select 1')
    print(result.fetchone())