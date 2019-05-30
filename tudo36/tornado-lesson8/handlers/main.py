import tornado.web
from PIL import Image
from pycket.session import SessionMixin

from utils.account import add_post, get_all_posts, get_post

class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        # return self.get_secure_cookie('tudo_cookie', None)
        # return self.get_secure_cookie('tudo_cookie', None)
        return self.session.get('tudo_user', None)


class IndexHandler(tornado.web.RequestHandler):
    """
    首页， 用户上传图片的展示
    """
    def get(self):
        posts = get_all_posts()
        self.render('index.html', posts=posts)


class ExploreHandler(tornado.web.RequestHandler):
    """
    最近上传的缩略图图片页面
    """
    def get(self):
        self.render('explore.html', a=100)


class PostHandler(tornado.web.RequestHandler):
    """
    单个图片详情页面
    """
    def get(self, post_id):
        post = get_post(post_id)
        if not post:
            self.write('wrong id {}'.format(post_id))
        else:
            self.render('post.html', post=post)
    # def get(self, *args, **kwargs):
    #     self.render('post.html', post_id=kwargs['post_id'])


class UploadHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('upload.html')

    @tornado.web.authenticated
    def post(self):
        pics = self.request.files.get('picture', [])
        post_id = 1
        print(pics[0]['filename'])
        # pics = [{"filename":..., "content_type":..., "body":...}, ]
        for p in pics:
            save_path = 'statics/upload/{}'.format(p['filename'])
            print(save_path)
            print(p['content_type'])
            with open(save_path, 'wb') as fh:
                fh.write(p['body'])

            post_id = add_post('upload/{}'.format(p['filename']), self.current_user)

            im = Image.open(save_path)
            im.thumbnail((200,200))
            im.save('statics/upload/thumb_{}.jpg'.format(p['filename']), 'JPEG')

        self.redirect('/post/{}'.format(post_id))