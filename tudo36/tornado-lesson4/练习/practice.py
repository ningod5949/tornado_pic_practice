import time
from datetime import datetime
import tornado.ioloop
import tornado.web
from utils import ui_methods, ui_modules


# 主页
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello World!")

    def prepare(self):
        print('prepare ' + str(datetime.now()))
        self.write('in prepare<br>')


# 返回主页
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect(r'/')


class PictureHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<img class="s-news-img" src="https://ss0.baidu.com/6ONWsjip0QIZ8tyhnq/it/u=70421826,2783094321&amp;fm=173&amp;app=49&amp;f=JPEG?w=218&amp;h=146&amp;s=B2404DA182CF3951CCED80A2030060C3" height="119" width="179">')


class TemplatesHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('02.html', username='no')
    def post(self, *args, **kwargs):
        username = self.get_argument('username', '')
        age = self.get_argument('age', '')
        print('username: ' + username)
        print('age: ' + age)
        self.render('02.html', username=username, age=age)


class Cal(object):
    # @staticmethod
    # def sum(a, b):
    #     return a + b
    # @classmethod
    # def sum(cls, a, b):
    #     return a + b
    def sum(self, a, b):
        return a + b


class ExtendsHandler(tornado.web.RequestHandler):
    def haha(self):
        return "hahah, I'm coming."
    def get(self):
        self.render('04.html', username='xuning',haha=self.haha, cal=Cal)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/index", IndexHandler),
        (r"/pic", PictureHandler),
        (r'/temp', TemplatesHandler),
        (r"/extend", ExtendsHandler),
    ],
    debug=True,
    template_path='templates',
    static_path='statics',
    ui_methods=ui_methods,
    ui_modules=ui_modules,
    # ui_modules={'UiModule': ui_modules.UiModule}
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
