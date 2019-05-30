# import time
import tornado.ioloop
import tornado.web
from units import ui_modules, ui_methods


class IndexHandler(tornado.web.RequestHandler):
    def haha(self):
        return "I'm coming"

    def get(self):
        self.render('index.html', username='xuning', cal=Cal, haha=self.haha)


class Cal(object):
    def sum(self, a, b):
        return a + b



class TemplatesHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('temp.html', username='no')

    def post(self):
        username = self.get_argument('username', ' ')
        password = self.get_argument('password', ' ')
        # self.decode_argument(b'empty', name='name')
        print(username)
        print(password)
        self.render('temp.html', username=username, password=password)


def make_app():
    return tornado.web.Application([
        (r'/', IndexHandler),
        (r'/temp', TemplatesHandler),
    ],
        debug=True,
        template_path='templates',
        static_path='statics',
        ui_methods=ui_methods,
        ui_modules=ui_modules,
        # ui_modules={'A': ui_modules.Hello}
        )


if __name__ == '__main__':
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()