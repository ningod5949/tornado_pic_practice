import time
import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.write('prepare先被调用')

    def get(self):
        taga = '<a href="https://www.baidu.com">去百度</a>'
        self.render('01.html', username='xuning', time=time, taga=taga)


def make_app():
    return tornado.web.Application([
        (r'/', MainHandler),
        ],
        debug=True,
        template_path='templates',
        static_path='statics',
        static_url_prefix='/image/'
        )


if __name__ == '__main__':
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()

