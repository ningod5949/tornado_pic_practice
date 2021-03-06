import uuid
import tornado.websocket
import tornado.web
import tornado.escape
from .main import BaseHandler


class Roomhandler(BaseHandler):
    """
    聊天页面
    """
    @tornado.web.authenticated
    def get(self):
        m = {
            'id': 41342,
            'username': self.current_user,
            'body': 'hello world aa',
        }
        msgs = [
            {
                'html':self.render_string('message.html', chat=m)
            }
        ]
        self.render('room.html', messages=msgs)


class ChatWSHandler(tornado.websocket.WebSocketHandler, BaseHandler):
    """
    处理和响应 Websocket 连接
    """
    waiters = set()   # 等待接收信息的用户
    # def open(self, *args: str, **kwargs: str):
    def open(self, *args, **kwargs):
        """
        新的 Websocket 连接打开， 自动调用
        :param args:
        :param kwargs:
        :return:
        """
        print('new ws connection: {}'.format(self))
        ChatWSHandler.waiters.add(self)

    def on_close(self):
        """
        Websocket 连接断开，自动调用
        :return:
        """
        print('close ws connection: {}'.format(self))
        ChatWSHandler.waiters.remove(self)

    def on_message(self, message):
        """
        Websocket 服务端接收到消息自动调用
        :param message:
        :return:
        """
        print("got message: {}".format(message))
        parsed = tornado.escape.json_decode(message)
        msg = parsed['body']
        chat = {
            'id': str(uuid.uuid4()),
            'body': msg,
            'username': self.current_user,
        }
        chat['html'] =tornado.escape.to_basestring(self.render_string('message.html', chat=chat))

        for w in ChatWSHandler.waiters:
            w.write_message(chat)



class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(u'You said:' + message)

    def on_close(self):
        print('WebSocket closed')



