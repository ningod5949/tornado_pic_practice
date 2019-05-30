from datetime import datetime
from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import exists
from models.db import Base, Session


session = Session()
class User(Base):
    __tablename__ = 'users'                     # 表名 users

    id = Column(Integer, primary_key=True, autoincrement=True) # 第一列 id 整数 主键 自增长
    name = Column(String(50), unique=True, nullable=False)     # 第二列 name 字符串
    password = Column(String(50))                              # 第三列password 字符串
    createtime = Column(DateTime, default=datetime.now)        # 第四列createtime 时间日期
    email = Column(String(50))

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

    id = Column(Integer, primary_key=True, autoincrement=True) # 第一列 id 整数 主键 自增长
    image_url = Column(String(200))                            # 第二列 image_url 字符串
    user_id = Column(Integer, ForeignKey('users.id'))          # 第三列 user_id 整数 外键关联 users.id
    user = relationship('User', backref='posts', uselist=False, cascade='all')

    def __repr__(self):
        return "<Post:#{}>".format(self.id)

if __name__ == '__main__':
    Base.metadata.create_all()