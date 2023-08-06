from queue import Queue

from .proxy_pool_class import ProxyPool


class FQProxyMiddleWare(object):
    """docstring for ProxyMiddleWare"""

    proxy = 'http://127.0.0.1:8008'

    @classmethod
    def from_crawler(cls, crawler):
        pass

    def process_request(self, request, spider):
        """对request对象加上proxy"""

        request.meta['proxy'] = self.proxy
        request.meta['download_timeout'] = 20


class TorProxyMiddleware(object):
    proxy = 'http://127.0.0.1:8123/'

    @classmethod
    def from_crawler(cls, crawler):
        pass

    def process_request(self, request, spider):
        """对request对象加上proxy"""

        request.meta['proxy'] = self.proxy
        request.meta['download_timeout'] = 20


# percent = 1
class ProxyPoolMiddleWare(object):
    """docstring for ProxyMiddleWare"""

    proxy_queue = Queue()
    proxy = None
    limit = 100

    # proxy_count = -1

    def __init__(self, settings):
        self.proxy_pool = ProxyPool()
        self.max_retry_times = settings.getint('MAX_PROXY_RETRY_TIMES') or 2
        self.max_retry_proxy_times = settings.getint('MAX_PROXY_PER_REQUEST') or 3

    @classmethod
    def from_crawler(cls, crawler):

        return cls(crawler.settings)
    #     # This method is used by Scrapy to create your spiders.
    #     s = cls()
    #     # print('666')
    #     # print(crawler.settings.getint('PROXY_COUNT'))
    #     conn = MongoClient(host=Setting.get_from_json('mongo_host'), port=Setting.get_from_json('mongo_port'))
    #     s.mongo = conn
    #     s.db = conn.get_database('ssti')
    #     s.mongo.db = s.db
    #     s.proxy = ProxyInfo(s)
    #     s.proxy_count = crawler.settings.getint('PROXY_COUNT')
    #     s.limit = 100
    #     crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
    #     return s

    def spider_opened(self):
        pass

    def get_proxy_list(self, limit=100):

        for proxy in self.proxy_pool.get_proxies_random(limit):
            self.proxy_queue.put_nowait(proxy['_id'])

    def process_request(self, request, spider):

        if request.meta.get('proxy'):
            return

        proxy = self.get_one_proxy()

        if not proxy:
            return

        # if request.meta.get('proxy_id'):
        #     proxy_id = request.meta['proxy_id']
        #
        #     self.proxy.collection.update(
        #         {'_id': proxy_id},
        #         {
        #             '$inc': {
        #                 'fail_count': 1,
        #                 'score': -1
        #             }
        #         })

        # if not request.meta.get('retry_times'):
        #     request.meta['retry_times'] = 1

        # request.meta['proxy_id'] = proxy['_id']
        request.meta['proxy'] = proxy
        request.meta['download_timeout'] = 30
        # print('proxy: %s://%s:%s' % (proxy['type'].lower(), proxy['ip'], proxy['port']))
        # return request
        # print(request.meta.get('retry_times', 0))

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.
        # print(exception)
        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        request.meta['exception'] = exception
        if 'proxy' not in request.meta:
            return

        retry_times = request.meta.get('proxy_retry_times') or 0

        retry_proxy_count = request.meta.get('retry_proxy_count') or 0

        if retry_proxy_count < self.max_retry_proxy_times:

            if retry_times >= self.max_retry_times:
                request.meta['proxy_retry_times'] = 0
                retry_proxy_count += 1
                request.meta['retry_proxy_count'] = retry_proxy_count
                request.meta['proxy'] = self.get_one_proxy()
                return request
            else:
                retry_times += 1
                request.meta['proxy_retry_times'] = retry_times
                return request
        #
        # proxy = self.get_one_proxy()
        #
        # request.meta['proxy_id'] = proxy['_id']
        # request.meta['proxy'] = '%s://%s:%s' % (proxy['type'].lower(), proxy['ip'], proxy['port'])
        # print('proxy: %s://%s:%s' % (proxy['type'].lower(), proxy['ip'], proxy['port']))
        # return request

    def process_response(self, request, response, spider):
        '''对返回的response处理'''
        # 如果返回的response状态不是200，重新生成当前request对象
        # if not request.meta.get('proxy_id'):
        #     return response
        # if response.status != 200:
        #
        #     if (request.meta.get('retry_times') or 0) > 10:
        #         spider.logger.info('ignore request %s' % request.url)
        #         raise IgnoreRequest
        #
        #     proxy_id = request.meta['proxy_id']
        #
        #     self.proxy.collection.update(
        #         {'_id': proxy_id},
        #         {
        #             '$inc': {
        #                 'fail_count': 1,
        #                 'score': -6
        #             }
        #         })
        #
        #     proxy = self.get_one_proxy()
        #
        #     request.meta['proxy_id'] = proxy['_id']
        #     request.meta['proxy'] = '%s://%s:%s' % (proxy['type'].lower(), proxy['ip'], proxy['port'])
        #
        #     print('proxy: %s://%s:%s' % (proxy['type'].lower(), proxy['ip'], proxy['port']))
        #     return request
        # if response.status == 200:
        #     proxy_id = request.meta['proxy_id']
        #     if proxy_id:
        #         self.proxy.collection.update(
        #             {'_id': proxy_id},
        #             {
        #                 '$inc': {
        #                     'score': 1
        #                 }
        #             })
        return response

    def get_one_proxy(self):
        if self.proxy_queue.empty():
            self.get_proxy_list(self.limit)
        proxy = self.proxy_queue.get_nowait()
        return proxy
