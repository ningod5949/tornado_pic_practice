import logging
import tornado.web
from pycket.session import SessionMixin
from test1.utils.account import HandlerORM
from test1.utils.photo import UploadImage
from models.db import Session


logger = logging.getLogger('tudo.log')


class Basehandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get('tudo_user', None)

    def prepare(self):
        self.db_session = Session()
        logger.info('db_session instance %s' % self)
        self.orm = HandlerORM(self.db_session)

    def on_finish(self):
        self.db_session.close()
        logger.info('db_session close')


class IndexHandler(Basehandler):
    @tornado.web.authenticated
    def get(self):
        posts = self.orm.get_posts_for(self.current_user)

        self.render('index.html', posts=posts)


class ExploreHandler(Basehandler):
    @tornado.web.authenticated
    def get(self):
        posts = self.orm.get_all_posts()
        self.render('explore.html', posts=posts)


class PostHandler(Basehandler):
    def get(self, post_id):
        post = self.orm.get_post(post_id)
        count = self.orm.count_like_for(post_id)
        # user = post.user
        print('post return')
        if not post:
            self.write('wrong id {}'.format(post_id))
        else:
            count = self.orm.count_like_for(post_id)
            self.render('post.html', post=post, count=count)


class UploadHandler(Basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render('upload.html')


    @tornado.web.authenticated
    def post(self):
        pics = self.request.files.get('picture', [])
        post_id = 1
        for p in pics:
            up_img = UploadImage(p['filename'], self.settings['static_path'])
            up_img.save_upload(p['body'])
            up_img.make_thumb()
            post_id = self.orm.add_post(up_img.image_url,
                                        up_img.thumb_url,
                                        self.current_user)
        self.redirect('/post/{}'.format(post_id))


class ProfileHander(Basehandler):
    """
    用户的档案页面
    """
    @tornado.web.authenticated
    def get(self):
        name = self.get_argument('name', None)
        if not name:
            name = self.current_user
        user = self.orm.get_user(name)
        if user:
            like_posts = self.orm.like_posts_for(name)
            self.render('profile.html', user=user, like_posts=like_posts)
        else:
            self.write('user error')


class LikeH(Basehandler):
    def post(self):
        post_id = self.get_argument('post_id', '')
        name = self.get_argument('username', '')
        print(post_id, name)
        self.write({'status': 'ok',
                    'count': 33})