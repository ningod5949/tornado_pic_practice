import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write('hello world')
        # self.write_error(400)
        self.set_status(400)
        # self.redirect('https://www.baidu.com')
def make_app():
    return tornado.web.Application([
        (r'/', MainHandler),
    ],
    debug=True,)

if __name__ == '__main__':
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()