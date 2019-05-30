import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    """
    RequestHandler子类
    主入口点：处理HTTP方法
    产生响应
        render或者write等
        错误处理或者重定向等
    可复写的方法
        每个请求的调用序列
        常用的复写方法
    """
    def get(self):
        self.write("Hello, world >")
        # self.write_error(500)
        # 如果一个处理程序抛出一个异常, Tornado会调用 RequestHandler.write_error 来生成一个错误页. tornado.web.HTTPError 可以被用来生成一个指定的状态码; 所有其他的异常 都会返回一个500状态.
        # self.set_status(500)
        # self.set_status: 返回一个(自定义)响应来生成一个错误页面.


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect(r'/')
        # redirect：重定向


class PictureHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<img class="s-news-img" src="https://ss0.baidu.com/6ONWsjip0QIZ8tyhnq/it/u=70421826,2783094321&amp;fm=173&amp;app=49&amp;f=JPEG?w=218&amp;h=146&amp;s=B2404DA182CF3951CCED80A2030060C3" height="119" width="179">')
class MyFormHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><body><form action="/myform" method="POST">'
                   '<input type="text" name="message">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')

    def post(self):
        self.set_header("Content-Type", "text/plain")
        self.write("You wrote " + self.get_body_argument("message"))


def make_app():
    """
    Application对象
        路由表URL映射
        关键词参数settings
    :return:
    """
    return tornado.web.Application([
        (r"/", MainHandler),
        (r'/post', MyFormHandler),
        (r'/index', IndexHandler),
        (r'/pic', PictureHandler)
    ],
    debug=True)

if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
    # current 现在的