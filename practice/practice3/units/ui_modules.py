from tornado.web import UIModule


class Hello(UIModule):
    def render(self, *args, **keargs):
        return "I'm ui_module"
