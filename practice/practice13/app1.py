import tornado.ioloop
import tornado.web
# 可以添加一些额外的参数
import tornado.options
from tornado.options import define, options


# from practice.practice6.handlers.main import IndexHandler, ExploreHandler
# from practice.practice6.handlers import main
from handlers import main, account


define('port', default='8000', help='Listening port', type=int)
define('debug', default='True', help='Debug mode', type=bool)
# python app.py --port=8000


class Application(tornado.web.Application):
    def __init__(self, debug=False):
        handles = [
            (r'/', main.IndexHandler),
            (r'/explore', main.ExploreHandler),
            # 命名捕获
            (r'/post/(?P<post_id>[0-9]+)', main.PostHandler),
            (r'/upload', main.UploadHandler),
            (r'/profile', main.ProfileHandler),
            (r'/like', main.LikeH),
            (r'/signup', account.RegisterHandler),
            (r'/login', account.LoginHandler),
            (r'/logout', account.LogoutHandler),
        ]
        settings = dict(
            debug=debug,
            template_path='templates',
            static_path='statics',
            cookie_secret="ashfhuiafhewuisdfsdff",
            # xsrf_cookies=True,
            login_url='/login',
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
        # 加载父类的__init__方法，传入对应的参数,来实现tornado.web.Application的功能
        super().__init__(handles, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    application = Application(debug=options.debug)
    application.listen(options.port)
    print("Server start on port {}".format(str(options.port)))
    tornado.ioloop.IOLoop.current().start()
