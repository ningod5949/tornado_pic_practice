# import tornado.ioloop
# import tornado.web
# from tornado.web import RequestHandler
# from tornado.web import Application
# from tornado.web import url
#
# class MainHandler(RequestHandler):
#     def get(self):
#         self.write('<a href="%s">link to story 1</a>' %
#                    self.reverse_url("story", "1"))
#
# class StoryHandler(RequestHandler):
#     def initialize(self, db):
#         self.db = db
#
#     def get(self, story_id):
#         self.write("this is story %s" % story_id)
#
# def make_app():
#     return tornado.web.Application([
#         url(r"/", MainHandler),
#         url(r"/story/([0-9]+)", StoryHandler, dict(db='a'), name="story")
#     ])
#
#
# if __name__ == "__main__":
#     app = make_app()
#     app.listen(8000)
#     tornado.ioloop.IOLoop.current().start()
#
from tornado import template
t = template.Template("<html>{{ myvalue }}</html>")
print (t.generate(myvalue="XXX"))