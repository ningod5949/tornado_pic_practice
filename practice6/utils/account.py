import hashlib
from models.auth import User, Post, Like
from models.db import Session

db_session = Session()
def hashed(text):
    return hashlib.md5(text.encode('utf8')).hexdigest()

def authenticate(username, password):
    # session = Session()
    # user = session.query(User).filter_by(name=username).first()
    # 登录密码用hash md5加密
    return User.get_password(username) == hashed(password)


# def register(username, password):
#     session = Session()
#     session.add(User(name=username, password=hashed(password)))
#     session.commit()
#     session.close()
#
#
# def add_post(image_url, thumb_url, username):
#     session = Session()
#     user = session.query(User).filter_by(name=username).first()
#     post = Post(image_url=image_url, thumb_url=thumb_url, user=user)
#     # session.add(Post(image_url=image_url, user_id=user.id))
#     session.add(post)
#     session.commit()
#     post_id = post.id
#     session.close()
#
#     return post_id
#
# def get_all_posts():
#     # 拿到所有图片
#     # session = Session()
#     posts = db_session.query(Post).all()
#     return posts
#
# def get_posts_for(username):
#     user = db_session.query(User).filter_by(name=username).first()
#     posts = db_session.query(Post).filter_by(user=user).all()
#     return posts
#
# def get_post(post_id, db_session):
#     # session = Session()
#     post = db_session.query(Post).filter_by(id=post_id).first()
#     # session.close()
#     return post

# ps -ef|grep python
# kill id
class HandlerORM:
    """
    辅助操作数据库的工具类，结合 RequestHandler 使用
    """
    def __init__(self, db_session):
        """

        :param db_session: 由handler 进行实例化和close
        """
        self.db = db_session

    def get_user(self, username):
        user = self.db.query(User).filter_by(name=username).first()
        return user

    def register(self, username, password):

        self.db.add(User(name=username, password=hashed(password)))
        self.db.commit()

    def add_post(self, image_url, thumb_url, username):
        user = self.get_user(username)
        post = Post(image_url=image_url, thumb_url=thumb_url, user=user)
        # session.add(Post(image_url=image_url, user_id=user.id))
        self.db.add(post)
        self.db.commit()
        post_id = post.id

        return post_id

    def get_all_posts(self):
        # 拿到所有图片
        # session = Session()
        posts = self.db.query(Post).all()
        return posts

    def get_posts_for(self, username):
        # user = self.db.query(User).filter_by(name=username).first()
        user = self.get_user(username)
        posts = self.db.query(Post).filter_by(user=user).all()
        return posts

    def get_post(self, post_id):
        """
        返回特定id 的post实例
        :param post_id:
        :return:
        """
        # session = Session()
        post = self.db.query(Post).filter_by(id=post_id).first()
        # session.close()
        return post

# django channel

    def like_posts_for(self, username):
        """
        查询用户喜欢的posts
        :param username:
        :return:
        """
        user = self.get_user(username)
        posts = self.db.query(Post).filter(Post.id == Like.post_id,
                                           Like.user_id == user.id,
                                           Post.user_id != user.id)
        return posts

    def count_like_for(self, post_id):
        count = self.db.query(Like).filter_by(post_id=post_id).count()
        return count