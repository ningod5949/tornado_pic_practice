from datetime import datetime
from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey)
from models.db import Base, Session
from sqlalchemy.sql import exists
from sqlalchemy.orm import relationship


session = Session()
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    password = Column(String(50))
    createtime = Column(DateTime, default=datetime.now)
    email = Column(String(50))


    def __repr__(self):
        return '<User:#{}-{}>'.format(self.id, self.name)

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

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='posts', uselist=False, cascade='all')

    def __repr__(self):
        return "<Post:#{}>".format(self.id)


if __name__ == '__main__':
    Base.metadata.create_all()