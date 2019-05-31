import tornado.web
from PIL import Image
from pycket.session import SessionMixin
from test1.utils.account import add_post

class Basehandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get('tudo_user', None)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class ExploreHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('explore.html')


class PostHandler(tornado.web.RequestHandler):
    def get(self, post_id):
        self.render('post.html', post_id=post_id)


class UploadHandler(Basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render('upload.html')


    @tornado.web.authenticated
    def post(self):
        pics = self.request.files.get('picture', [])
        post_id = 1
        for p in pics:
            save_path = 'statics/upload/{}'.format(p['filename'])
            with open(save_path, 'wb') as fh:
                fh.write(p['body'])

            post_id = add_post('upload/{}'.format(p['filename']), self.current_user)
            im = Image.open(save_path)
            im.thumbnail((200,200))
            im.save('statics/upload/thumb_{}.jpg'.format(p['filename']), 'JPEG')

        self.redirect('/post/{}'.format(post_id))
