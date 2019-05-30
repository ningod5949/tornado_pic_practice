from datetime import datetime
import os
# glob简单的目录检索来展示
import glob
import tornado.ioloop
import tornado.web
from pycket.session import SessionMixin
from utils import ui_methods, ui_modules
from PIL import Image


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
       return self.session.get('tudo_user', None)


class MainHandler(BaseHandler):
    def get(self):
        self.write("Hello, world")

    def prepare(self):
        print('prepare ' + str(datetime.now()))
        self.write('in prepare <br>')


class PictureHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        os.chdir('statics/upload')
        names = glob.glob('*.jpg')
        print(names)
        new_names = []
        for i in names:
            a = i.split('.jpg')
            b = a[0] + '.jpeg'
            im = Image.open(i)
            im.thumbnail((200,200))
            im.save('{}.jpeg'.format(a[0]))
            new_names.append(b)
        print(new_names)
        os.chdir('..')
        os.chdir('..')
        print(os.getcwd())
        self.render('08picture.html', new_names=new_names)


class TemplatesHandler(BaseHandler):
    def get(self):
        username = ''
        if not self.get_secure_cookie('tudo_cookie'):
            print('Your cookie was not set yet!')
        else:
            username = self.get_secure_cookie('tudo_cookie')
        next_url = self.get_argument('next', '')
        msg = self.get_argument('msg', '')
        self.render('02template.html', username=username, msg=msg, next_url=next_url)
    def post(self):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        next_url = self.get_argument('next', '')
        print('username [{}] password [{}]'.format(username, password))
        print('next_url [{}]'.format(next_url))
        if not username.strip() or not password.strip():
            self.redirect('/temp?msg=empty password or username ')
        else:
            if (username == 'qq') and (password == 'qq'):
                self.session.set('tudo_user', 'qq')
                if next_url:
                    self.redirect(next_url)
                else:
                    self.redirect('/pic')
            else:
                self.redirect('/temp?msg=password error')



class UploadHandler(BaseHandler):
    def get(self):
        self.render('07upload.html')

    def post(self):
        # self.request.files.get(name,[])获取文件内容，
        pics = self.request.files.get('picture', [])
        print(pics[0]['filename'])
        # pics = [{"filename":..., "content_type":..., "body":...}, ]
        for p in pics:
            save_path = 'statics/upload/{}'.format(p['filename'])
            # print(p['filename'])
            print(save_path)
            print(p['content_type'])
            # print(p['body'])
            with open(save_path, 'wb') as fh:
                fh.write(p['body'])

        self.write('upload done')


class Cal(object):
    def sum(self, a, b):
        return a + b


class ExtendsHandler(BaseHandler):
    def haha(self):
        return "hahah, I'm coming."

    @tornado.web.authenticated
    def get(self):
        self.render('04extends.html', username=self.current_user, haha=self.haha, cal=Cal)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r'/pic', PictureHandler),
        (r'/temp', TemplatesHandler),
        (r'/extend', ExtendsHandler),
        (r'/upload', UploadHandler),
    ],
        debug=True,
        template_path='templates',
        # autoescape=None, # 整个模版去转义
        static_path='statics',
        # static_url_prefix='/image/', # 改变路径名
        ui_methods=ui_methods,
        ui_modules=ui_modules,
        # ui_modules={'UiModule': ui_modules.UiModule}
        cookie_secret="ashfhuiafhewuifhuhaiufhiauhf",
        # xsrf保护
        # xsrf_cookies=True,
        login_url='/temp',
        pycket={
            'engine': 'redis', # 使用redis这个引擎存储
            'stronge': {
                'host': 'localhost',
                'port': 6379,
                # 'password' : '',
                'db_sessions': 5, # redis db index
                # 'db_notifications': 11,
                'max_connection': 2 ** 30,
            },
            'cookies': {
                'expires_days': 30,
            },
        },
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
