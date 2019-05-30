import tornado.web
import tornado.ioloop
import tornado.options
from tornado.options import define, options
from handlers import main, account


define('port', default='8000', help='Listening port', type=int)
define('debug', default='True', help='Debug mode', type=bool)

class Application(tornado.web.Application):
    def __init__(self, debug=False):
        # 路由
        handles= [
            (r'/', main.IndexHandler),
            (r'/explore', main.ExploreHandler),
            (r'/post/(?P<post_id>[0-9]+)', main.PostHandler),
            (r'/signup', account.RegisterHandler),
            (r'/login', account.LoginHandler),
            (r'/upload', main.UploadHandler),
        ]
        settings = dict(
            debug=debug,
            static_path='statics',
            template_path='templates',
            cookie_secret='shkfajkfhakfhk',
            login_url='/login',
            pycket={
                'engine': 'redis',
                'stronge': {
                    'host': 'localhost',
                    'port': '6379',
                    'db_session': 5,
                    'max_connecction': 2**30,
                },
                'cookies':{
                    'expires_days': 30,
                },
            },
        )
        # 加载父类的__init__方法，传入参数
        super().__init__(handles, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    application = Application(debug=options.debug)
    application.listen(options.port)
    print('Server start on port : {}'.format(str(options.port)))
    tornado.ioloop.IOLoop.current().start()