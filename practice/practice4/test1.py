import tornado.ioloop
import tornado.web
from pycket.session import SessionMixin


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        # return self.get_secure_cookie('tudo_cookie', None)
        return self.session.get('tudo_user', None)

# class IndexHandler(tornado.web.RequestHandler):
#     # 设置用户获取，通过self.current_user获取usename
#     def get_current_user(self):
#         return self.get_secure_cookie('tudo_cookie', None)
#
#     # 设置用户登录保护
#     @tornado.web.authenticated
#     def get(self):
#         # 可以从url输入的username中获取到
#         self.render('index.html', username=self.current_user)

class IndexHandler(BaseHandler):
    # 设置用户登录保护
    @tornado.web.authenticated
    def get(self):
        # 可以从url输入的username中获取到
        self.render('index.html', username=self.current_user)

class TemplatesHandler(BaseHandler):
    def get(self):
        # 登录验证
        username = ''
        # if not self.get_cookie("tudo_cookie"):
        if not self.get_secure_cookie("tudo_cookie"):
            self.write("you cookie was not set yet<br>")
        else:
            username = self.get_secure_cookie("tudo_cookie")
            print(self.get_cookie("tudo_cookie"))
            print(self.get_secure_cookie("tudo_cookie"))
            # username = self.get_cookie("tudo_cookie")
            self.write("your cookie was set<br>")

        next_url = self.get_argument('next', '')
        print(next_url)
        msg = self.get_argument('msg', '')
        self.render('temp.html', username=username, msg=msg, next_url=next_url)

    def post(self):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        next_url = self.get_argument('next', '')
        print('next_url: ' + next_url)
        # self.decode_argument(b'empty', name='name')
        if not username.strip() or not password.strip():
            self.redirect('/temp?msg= empty username or password')
        else:
            print('username:' + username)
            print('password:' + password)
            if username == 'qq' and password == 'qq':
                # self.set_cookie("tudo_cookie", "qq")
                # self.set_secure_cookie("tudo_cookie", "qq")
                self.session.set("tudo_user", "qq")
                if next_url:
                    self.redirect(next_url)
                else:
                    self.redirect('/index')
            else:
                self.redirect('/temp?msg= password error')



def make_app():
    return tornado.web.Application([
        (r'/index', IndexHandler),
        (r'/temp', TemplatesHandler),
    ],
        debug=True,
        template_path='templates',
        static_path='statics',
        # cookie_secret 设置cookie加密
        cookie_secret='hakjsdfhakjsdfhkja',
        # 设置用户登录路径
        login_url='/temp',
        pycket={
            'engine': 'redis',
            'storage': {
                'host': 'localhost',
                'port': 6379,
            #     'password': '',
                'db_sessions': 5, # redis db index
                'db_notifications':11,
                'max_connections': 2**30,
            },
            'cookies': {
                'expires_days': 30,
            },
        },
        )


if __name__ == '__main__':
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()