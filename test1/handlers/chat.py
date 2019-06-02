import uuid
from datetime import datetime
from pycket.session import SessionMixin
import tornado.websocket
import tornado.web
import tornado.escape
from .main import Basehandler


def make_data(handler, msg, username):
    """
    生成用来发送消息的字典数据
    :param handler:
    :param msg:
    :param username:
    :return:
    """
    chat = {
        'id': str(uuid.uuid4()),
        'body': msg,
        'username': username,
        'created': str(datetime.now()),
    }

    chat['html'] = tornado.escape.to_basestring(handler.render_string('message.html', chat=chat))
    return chat

class RoomHandler(Basehandler):
    """
    聊天室
    """
    @tornado.web.authenticated
    def get(self):
        # m = {
        #     'id': 41342,
        #     'username': self.current_user,
        #     'body': 'hello 36 class',
        # }
        #
        # msgs = [
        #     {
        #         'html': self.render_string('message.html', chat=m)
        #     }
        # ]
        self.render('room.html', messages=ChatWSHandler.history)


class ChatWSHandler(tornado.websocket.WebSocketHandler, SessionMixin):
    """
    处理和响应 WebSocket连接
    """
    waiters = set()   # 等待接受信息的用户
    history = [ ]       # 存放历史消息
    history_size = 20    # 最后20条

    def get_current_user(self):
        return self.session.get('tudo_user', None)

    def open(self, *args, **kwargs):
        """
        新的 WebSocket 连接打开 自动调用
        :param args:
        :param kwargs:
        :return:
        """
        print('new ws connection: {}'.format(self))
        ChatWSHandler.waiters.add(self)

    def on_close(self):
        """
        WebSocket 连接断开， 自动调用
        :return:
        """
        print("close ws connection: {}".format(self))
        ChatWSHandler.waiters.remove(self)

    def on_message(self, message):
        """
        WebSocket 服务端收到消息自动调用
        :param message:
        :return:
        """
        print("got message: {}".format(message))
        parsed = tornado.escape.json_decode(message) # json数据解码
        msg = parsed['body']
        # chat = {
        #     'id': str(uuid.uuid4()),
        #     'body': msg,
        #     'username': self.current_user,
        #     'created': str(datetime.now()),
        # }
        #
        # chat['html'] =  tornado.escape.to_basestring(self.render_string('message.html', chat = chat))
        chat = make_data(self, msg, self.current_user)
        self.update_history(chat)
        self.send_updates(chat)
        # print(chat['html'])

    def update_history(self, chat):
        """
        把新消息更新到 history，截取最后20条
        :param chat:
        :return:
        """
        ChatWSHandler.history.append(chat['html'])
        if len(ChatWSHandler.history) > ChatWSHandler.history_size:
            ChatWSHandler.history = ChatWSHandler.history[-ChatWSHandler.history_size:]

    def send_updates(self, chat):
        """
        给每个等待接收的用户发新的消息
        :param chat:
        :return:
        """
        for w in ChatWSHandler.waiters:
            w.write_message(chat)

        # print(set(ChatWSHandler.waiters))


class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print('WebSocket opened')

    def on_message(self, message):
        self.write_message(u'You said: ' + message)
        print('message')

    def on_close(self):
        print('WebSocket closed')


