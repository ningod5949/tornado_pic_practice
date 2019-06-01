import tornado.web
from pycket.session import SessionMixin
from test1.utils.account import HandlerORM
from test1.utils.photo import UploadImage
from models.db import Session


class Basehandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get('tudo_user', None)

    def prepare(self):
        self.db_session = Session()
        print('db_session instance')
        self.orm = HandlerORM(self.db_session)
    def on_finish(self):
        self.db_session.close()
        print('db_session close')


class IndexHandler(Basehandler):
    @tornado.web.authenticated
    def get(self):
        posts = self.orm.get_posts_for(self.current_user)

        self.render('index.html', posts=posts)


class ExploreHandler(Basehandler):
    def get(self):
        posts = self.orm.get_all_posts()
        self.render('explore.html', posts=posts)


class PostHandler(Basehandler):
    def get(self, post_id):
        post = self.orm.get_post(post_id)
        user = post.user
        print('post return')
        if not post:
            self.write('wrong id {}'.format(post_id))
        else:
            self.render('post.html', post=post)


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
