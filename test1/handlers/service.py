import time
import logging
import requests
from tornado.httpclient import AsyncHTTPClient
from tornado.gen import coroutine,sleep
# from tornado.concurrent import Future
from .main import Basehandler
from utils.photo import UploadImage


logger = logging.getLogger('tudo.log')
class SyncSaveHandler(Basehandler):
    def get(self):
        save_url = self.get_argument('save_url', '')
        logger.info(save_url)

        resp = requests.get(save_url)
        time.sleep(10)
        logger.info(resp.status_code )
        # up_img = UploadImage('x.jpg', self.settings['static_path'])
        # up_img.save_upload(resp.content)
        # up_img.make_thumb()
        #
        # post_id = self.orm.add_post(up_img.image_url,
        #                             up_img.thumb_url,
        #                             self.current_user)

        # self.redirect('/post/{}'.format(post_id))


# def async_fetch_future(url):
#     http_client = AsyncHTTPClient()
#     my_future = Future()
#     fetch_future = http_client.fetch(url)
#     fetch_future.add_done_callback(
#         lambda f: my_future.set_result(f.result())
#     )
#     return my_future

class AsycSaveHandler(Basehandler):
    @coroutine
    def get(self):
        save_url = self.get_argument('save_url', '')
        logger.info(save_url)

        client = AsyncHTTPClient()
        resp = yield client.fetch(save_url)
        logger.info(resp.code)
        yield sleep(15)
        logger.info('sleep end')
        self.write('get end')
        # up_img = UploadImage('x.jpg', self.settings['static_path'])
        # up_img.save_upload(resp.body)
        # up_img.make_thumb()
        #
        # post_id = self.orm.add_post(up_img.image_url,
        #                             up_img.thumb_url,
        #                             self.current_user)
        #
        # self.redirect('/post/{}'.format(post_id))