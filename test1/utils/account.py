import hashlib
from models.auth import User, Post
from models.db import Session


def hashed(text):
    return hashlib.md5(text.encode('utf8')).hexdigest()


def register(username, password):
    session = Session()
    session.add(User(name=username, password=hashed(password)))
    session.commit()
    session.close()

