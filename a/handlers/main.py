from PIL import Image
import tornado.web
from pycket.session import SessionMixin
from a.utils.account import add_post, get_all_posts, get_post


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get('tudo_user', None)


class IndexHandler(tornado.web.RequestHandler):
    """
    首页，用户上传图片展示，所关注的用户图片流
    """
    def get(self):
        # self.render('index.html')
        posts = get_all_posts()
        self.render('index.html', posts=posts)


class ExploreHandler(tornado.web.RequestHandler):
    """
    发现和最近上传的图片页面
    """
    def get(self):
        self.render('explore.html')


class PostHandler(tornado.web.RequestHandler):
    """
    单个页面图片详情
    """
    # def get(self, post_id):
    #     self.render('post.html', post_id=post_id)
    def get(self, post_id):
        post = get_post(post_id)
        if not post:
            self.write('wrong id {}'.format(post_id))
        else:
            self.render('post.html', post=post)


class UploadHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('upload.html')


    @tornado.web.authenticated
    def post(self):
        pics = self.request.files.get('picture', [])
        post_id = 1
        for p in pics:
            save_path = 'statics/upload/{}'.format('picture', [])
            # print(save_path)
            with open(save_path, 'wb') as fh:
                fh.write(p['body'])

            post_id = add_post('upload/{}'.format(p['filename']), self.current_user)
            im = Image.open(save_path)
            im.thumbnail((200,200))
            im.save('statics/upload/thumb_{}.jpg'.format(p['filename']), 'JPEG')

        self.redirect('/post/{}'.format(post_id))