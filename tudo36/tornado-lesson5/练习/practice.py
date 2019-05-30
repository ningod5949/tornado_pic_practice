import time
from datetime import datetime
import tornado.ioloop
import tornado.web
from pycket.session import SessionMixin


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        # return self.get_secure_cookie('tudo_cookie', None)
        return self.session.get('tudo_user', None)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello World!')

    def prepare(self):
        print('prepare ' + str(datetime.now()))
        self.write('in prepare <br>')


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect(r"/")


class PictureHandler(BaseHandler):
    # 设置用户认证，防止随意访问
    # def get_current_user(self):
    #     return 'tudo'
    @tornado.web.authenticated
    def get(self):
        self.write('''<html><head></head><body> username: {} <br><img class="s-news-img" src="https://ss0.baidu.com/6ONWsjip0QIZ8tyhnq/it/u=70421826,2783094321&amp;fm=173&amp;app=49&amp;f=JPEG?w=218&amp;h=146&amp;s=B2404DA182CF3951CCED80A2030060C3" height="119" width="179"></body></html>'''.format(self.current_user))


class TemplatesHandler(BaseHandler):
    def get(self):
        username = ''
        # if not self.get_cookie("tudo_cookie"):
        if not self.get_secure_cookie("tudo_cookie"):
            print("Your cookie is not set yet!")
        else:
            print(self.get_cookie("tudo_cookie"))
            print(self.get_secure_cookie("tudo_cookie"))
            # username = self.get_cookie('tudo_cookie')
            username = self.get_secure_cookie('tudo_cookie')
            # self.write("Your cookie was set!")

        next_url = self.get_argument('next', '')
        print('next_url: [{}]'.format(next_url))
        msg = self.get_argument('msg', '')
        self.render('02template.html', username=username, msg=msg, next_url=next_url)

    def post(self):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        next_url = self.get_argument('next', '')
        if (not username.strip()) or (not password.strip()):
            self.redirect('/temp?msg=empty password or name')
        else:
            print('username: [{}] \npassword: [{}]'.format(username, password))
            print('next_url: [{}]'.format(next_url))
            if (username == 'qq') and (password == 'qq'):
                # self.set_cookie('tudo_cookie', "qq")
                self.session.set('tudo_user', "qq")
                # self.set_secure_cookie('tudo_cookie', "qq")
                if next_url:
                    self.redirect(next_url)
                else:
                    self.redirect('/pic')
            else:
                self.redirect('/temp?msg=password error')


# class ExtendsHandler(BaseHandler):
class ExtendsHandler(BaseHandler):
    # 返回cookie中的username

    # def get_current_user(self):
    #     return self.get_secure_cookie('tudo_cookie', None)
    # @tornado.web.authenticated
    @tornado.web.authenticated
    def get(self):
        self.render('04extends.html', username=self.current_user)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/index", IndexHandler),
        (r"/pic", PictureHandler),
        (r"/temp", TemplatesHandler),
        (r"/extend", ExtendsHandler),
    ],
    debug=True,
    template_path="templates",
    static_path="statics",
    cookie_secret='ajklfjsaiofjsioafjoasif',
    login_url="/temp",
    pycket={
        'engine': 'redis',  # 使用redis这个引擎存储
        'stronge': {
            'host': 'localhost',
            'port': 6379,
            # 'password' : '',
            'db_sessions': 5,  # redis db index
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
    tornado.ioloop.IOLoop().current().start()