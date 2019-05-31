import tornado.web
from test1.utils.account import register

class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('register.html')


    def post(self):
        username = self.get_argument('username', '')
        password1 = self.get_argument('password1', '')
        password2 = self.get_argument('password2', '')

        if username and (password1 == password2):
            register(username, password1)
            self.write('signup ok')
        else:
            self.write('bad username/password')
