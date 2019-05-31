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

def authenticate(username, password):
    return User.get_password(username) == hashed(password)


def add_post(image_url, username):
    session = Session()
    user = session.query(User).filter_by(name=username).first()
    post = Post(image_url=image_url, user=user)
    session.add(post)
    session.commit()
    post_id = post.id
    session.close()
    return post_id

