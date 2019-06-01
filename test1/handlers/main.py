import tornado.web
from pycket.session import SessionMixin
from test1.utils.account import add_post, get_post, get_all_posts
from test1.utils.photo import UploadImage


class Basehandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get('tudo_user', None)


class IndexHandler(Basehandler):
    @tornado.web.authenticated
    def get(self):
        posts = get_all_posts()
        self.render('index.html', posts=posts)


class ExploreHandler(Basehandler):
    def get(self):
        posts = get_all_posts()
        self.render('explore.html', posts=posts)


class PostHandler(Basehandler):
    def get(self, post_id):
        post = get_post(post_id)
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
            post_id = add_post(up_img.image_url,
                               up_img.thumb_url,
                               self.current_user)
        self.redirect('/post/{}'.format(post_id))
