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



def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/index", IndexHandler),
        (r"/pic", PictureHandler),
    ],
    debug=True)


if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
