import logging

import tornado.ioloop
import tornado.web
import tornado.options
from tornado.options import define, options
from handlers import main, account, chat, service


logging.basicConfig(level=logging.DEBUG,  format='%(levelname)s -- %(funcName)s: %(message)s')
define('port', default='8000', help='Listening port', type=int)
define('debug', default='True', help='Debug mode', type=bool)


class Application(tornado.web.Application):
    def __init__(self, debug=False):
        handles = [
            (r'/', main.IndexHandler),
            (r'/explore', main.ExploreHandler),
            (r'/post/(?P<post_id>[0-9]+)', main.PostHandler),
            (r'/upload', main.UploadHandler),
            (r'/profile', main.ProfileHander),
            (r'/like', main.LikeH),
            (r'/signup', account.RegisterHandler),
            (r'/login', account.LoginupHandler),
            (r'/logout', account.LogoutHandler),
            (r'/ws/echo', chat.EchoWebSocket),
            (r'/ws', chat.ChatWSHandler),
            (r'/room', chat.RoomHandler),
            (r'/sync', service.SyncSaveHandler),
            (r'/save', service.AsycSaveHandler),
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
        super().__init__(handles, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    # if options.debug:
    #     from my_config import HOST
    # else:
    #     from prod_config import HOST
    # application = Application(debug=options.debug, host=HOST)

    application = Application(debug=options.debug)
    application.listen(options.port)
    print("Server start on port {}".format(str(options.port)))
    tornado.ioloop.IOLoop.current().start()







#