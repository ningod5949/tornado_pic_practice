import hashlib
from models.auth import User, Post
from models.db import Session


def hashed(text):
    return hashlib.md5(text.encode('utf8')).hexdigest()

def authenticate(username, password):
    # session = Session()
    # user = session.query(User).filter_by(name=username).first()
    # 登录密码用hash md5加密
    return User.get_password(username) == hashed(password)


def register(username, password):
    session = Session()
    session.add(User(name=username, password=hashed(password)))
    session.commit()
    session.close()


def add_post(image_url, username):
    session = Session()
    user = session.query(User).filter_by(name=username).first()
    post = Post(image_url=image_url, user=user)
    # session.add(Post(image_url=image_url, user_id=user.id))
    session.add(post)
    session.commit()
    post_id = post.id
    session.close()

    return post_id

def get_all_posts():
    # 拿到所有图片
    session = Session()
    posts = session.query(Post).all()
    return posts

def get_post(post_id):
    session = Session()
    post = session.query(Post).filter_by(id=post_id).first()
    return post

