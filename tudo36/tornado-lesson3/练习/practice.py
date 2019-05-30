import time
from datetime import datetime
import tornado.ioloop
import tornado.web


# 主页
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello World!")


# 返回主页
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect(r'/')


class PictureHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<img class="s-news-img" src="https://ss0.baidu.com/6ONWsjip0QIZ8tyhnq/it/u=70421826,2783094321&amp;fm=173&amp;app=49&amp;f=JPEG?w=218&amp;h=146&amp;s=B2404DA182CF3951CCED80A2030060C3" height="119" width="179">')


class TemplatesHandler(tornado.web.RequestHandler):
    def get(self):
        atga = '<a href="https://www.baidu.com" target="_blank">__百度__</a><br>'
        self.render('01.html', name='in and out', time=time, namelist=['a', 'b', 'c'], atga=atga)

    def post(self, *args, **kwargs):
        name = self.get_argument('name', 'no')
        self.render('02.html', username=name)



def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/index", IndexHandler),
        (r"/pic", PictureHandler),
        (r'/temp', TemplatesHandler),
    ],
    debug=True,
    template_path='templates',
    static_path='statics')


if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
