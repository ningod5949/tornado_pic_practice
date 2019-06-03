import uuid
from datetime import datetime
import logging
from pycket.session import SessionMixin
from tornado.httpclient import AsyncHTTPClient
import tornado.websocket
import tornado.web
import tornado.gen
import tornado.escape
from tornado.ioloop import IOLoop
from .main import Basehandler
from utils.photo import UploadImage


logger = logging.getLogger('tudo.log')


def make_data(handler, msg, username='system', img_url=None, post_id=None):
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
        'img_url': img_url,
        'post_id': post_id,
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

    # @tornado.gen.coroutine
    def on_message(self, message):
        """
        WebSocket 服务端收到消息自动调用
        :param message:
        :return:
        """
        print("got message: {}".format(message))
        parsed = tornado.escape.json_decode(message) # json数据解码
        msg = parsed['body']

        if msg and msg.startswith('http://'):
            # temp_chat = make_data(self, 'url processing {}'.format(msg))
            # self.write_message(temp_chat)
            # client = AsyncHTTPClient()
            # resp = yield client.fetch(msg)
            # up_img = UploadImage('x.jpg', self.settings['static_path'])
            # up_img.save_upload(resp.body)
            # reply_msg = 'upload photo from url {}'.format(msg)
            # chat = make_data(self, reply_msg, username=self.current_user, img_url=up_img.image_url)
            # ChatWSHandler.send_updates(chat)


            client = AsyncHTTPClient()
            save_api_url = 'http://127.0.0.1:8000/save?save_url={}&name={}&is_from=room'.format(msg, self.current_user)
            logger.info(save_api_url)
            IOLoop.current().spawn_callback(client.fetch,
                                            save_api_url,
                                            request_timeout=50)
            reply_msg = "user {}, url {} is processing".format(
                self.current_user,
                msg,
            )
            chat = make_data(self, reply_msg)
            self.write_message(chat)   # 只给当前用户发送


        else:
        # chat = {
        #     'id': str(uuid.uuid4()),
        #     'body': msg,
        #     'username': self.current_user,
        #     'created': str(datetime.now()),
        # }
        #
        # chat['html'] =  tornado.escape.to_basestring(self.render_string('message.html', chat = chat))
            logger.warning(locals())
            chat = make_data(self, msg, self.current_user)
            ChatWSHandler.update_history(chat)
            ChatWSHandler.send_updates(chat)
        # print(chat['html'])

    @classmethod
    def update_history(cls, chat):
        """
        把新消息更新到 history，截取最后20条
        :param chat:
        :return:
        """
        ChatWSHandler.history.append(chat['html'])
        if len(ChatWSHandler.history) > ChatWSHandler.history_size:
            ChatWSHandler.history = ChatWSHandler.history[-ChatWSHandler.history_size:]

    @classmethod
    def send_updates(cls, chat):
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


