from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
# 创建会话
from sqlalchemy.orm import sessionmaker


HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'tudo36'
USERNAME = 'admin'
PASSWORD = 'Root110qwe'

DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
    USERNAME, PASSWORD, HOST, PORT, DATABASE
)

engine = create_engine(DB_URI)


Base = declarative_base(engine)
# 创建会话
Session = sessionmaker(bind=engine)

if __name__ == '__main__':
    connection = engine.connect()
    result = connection.execute('select 1')
    print(result.fetchone())
