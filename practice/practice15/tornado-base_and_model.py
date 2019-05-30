from datetime import datetime
import os
import glob
import tornado.ioloop
import tornado.web
from utils import ui_methods, ui_modules
from PIL import Image

from handlers.main import BaseHandler, UploadHandler


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

    def prepare(self):
        print('prepare ' + str(datetime.now()))
        self.write('in prepare <br>')


# class PictureHandler(tornado.web.RequestHandler):
class PictureHandler(BaseHandler):
    # def get_current_user(self):
    #     return 'tudo'
    @tornado.web.authenticated
    def get(self):
        # self.write('''<html><head></head><body> username: {} <br><img class="s-news-img" src="https://ss0.baidu.com/6ONWsjip0QIZ8tyhnq/it/u=70421826,2783094321&amp;fm=173&amp;app=49&amp;f=JPEG?w=218&amp;h=146&amp;s=B2404DA182CF3951CCED80A2030060C3" height="119" width="179"></body></html>'''.format(self.current_user))
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
# class TemplatesHandler(tornado.web.RequestHandler):
    def get(self):
        username = ''
        # 设置cookie ：set_cookie
        # if not self.get_cookie('tudo_cookie'):
        if not self.get_secure_cookie('tudo_cookie'):
            # self.set_cookie('tudo_cookie', 'qq')
            # self.write('Your coolie was not set yet!')
            print('Your cookie was not set yet!')
        else:
            # self.write('Your cookie was set!')
            # print(self.get_cookie('tudo_cookie'))
            username = self.get_secure_cookie('tudo_cookie')
        # self.write('templates')  # 尽量write 和render不要一起使用
        # atga = "<a href='https://www.baidu.com' target='_blank'>___百度___</a><br>"
        # self.render('01in_our.html', name='in and out', time=time, namelist=['a', 'b', 'c'], atga=atga)
        # write直接返回字符串信息
        # render（渲染）利用模版文件进行字符串渲染
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
                # self.set_secure_cookie('tudo_cookie', 'qq')
                if next_url:
                    self.redirect(next_url)
                else:
                    self.redirect('/pic')
                # self.write('login pass')
                # self.redirect('/pic')
            else:
                # self.write('fall')
                self.redirect('/temp?msg=password error')
            # self.render('02template.html', username=username, age=age)

        # name = self.decode_argument(b'empty', name='name')
        # print('post response for %s' % username)
        # self.render('02template.html', username=age, namelist=['a', 'b', 'c'])
        # self.render('02template.html', username=username, age=age)


class Cal(object):
    # @staticmethod
    # def sum(a, b):
    #     return a + b
    # @classmethod
    # def sum(cls, a, b):
    #     return a + b
    def sum(self, a, b):
        return a + b


class ExtendsHandler(BaseHandler):
# class ExtendsHandler(tornado.web.RequestHandler):
    # 返回cookie中的username
    # def get_current_user(self):
    #     return self.get_secure_cookie('tudo_cookie', None)

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
