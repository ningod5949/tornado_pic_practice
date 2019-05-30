from datetime import datetime
from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import exists
from models.db import Base, Session


session = Session()
# 定义user表
class User(Base):
    # __tablename__： 数据库中的表名
    __tablename__ = 'users'

    # Column：    用来创建表中的字段的一个方法
    # Integer：   整形，映射到数据库中的int类型
    # String：    字符类型，映射到数据库中的varchar类型，使用时，需要提供一个字符长度
    # DateTime：  时间类型
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    password = Column(String(50))
    creatime = Column(DateTime, default=datetime.now)
    email = Column(String(80))

    def __repr__(self):
        return "<User:#{}-{}>".format(self.id, self.name)

    @classmethod
    def is_exists(cls, username):
        return session.query(exists().where(cls.name == username)).scalar()

    @classmethod
    def get_password(cls, username):
        user = session.query(cls).filter_by(name=username).first()
        if user:
            return user.password
        else:
            return ''


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(String(200))
    # thumb_url = Column(String(200))

    user_id = Column(Integer, ForeignKey('users.id'))
    # backref 反向引用
    user = relationship('User', backref='posts', uselist=False, cascade='all')

    def __repr__(self):
        return "<Post:#{}>".format(self.id)
    # In [6]: ps = session.query(Post).all()
    # In [7]: ps
    # Out[7]: [<Post:#1>]

    # In [1]: from models.auth import *
    # In [2]: ps = session.query(Post).all()
    # In [3]: ps
    # Out[3]: [<models.auth.Post at 0x7f390c0c5a58>]


if __name__ == '__main__':
    # 创建表
    Base.metadata.create_all()

