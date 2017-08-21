# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json
import random

import requests
from scrapy import signals
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware  # 代理ip，这是固定的导入
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from multiprocessing import Process, Queue


class ProxiesSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# 响应头
class MyAgent(UserAgentMiddleware):

    def __init__(self,user_agent=''):
        self.user_agent = user_agent

    def process_request(self,request,spider):
        request.headers.setdefault('User-Agent', 'Mozilla/5.0 '
                                                 '(X11; Linux x86_64) '
                                                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                 'Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36')


class IPPOOLS(HttpProxyMiddleware):

    def __init__(self, ip=''):
        self.ip = ip
        self.ippools = self.get_ippool()
        self.proxies = ["{0}://{1}:{2}".format(ip['h'], ip['ip'], ip['port'])
                        for ip in self.ippools]

    def process_request(self, request, spider):
        """使用代理ip，随机选用"""
        # 先验证
        self.verify_proxies()
        # 验证更新代理列表后所有的ip可用
        ip = random.choice(self.proxies)  # 随机选择一个ip
        print('当前使用的IP是' + ip)
        try:
            request.meta["proxy"] = ip
        except Exception as e:
            print(e)
        pass

    # 获代理ip程池, 默认30条
    def get_ippool(self, n=30):
        res = []
        with open(r'D:\workspace\web_scrap\proxies\proxies\proxies.json', 'r', encoding='gbk') as f:
            for i in range(n):
                res.append(json.loads(f.readline().strip()))
        return res

    def verify_proxies(self):
        # 没验证的代理
        old_queue = Queue()
        # 验证后的代理
        new_queue = Queue()
        print('verify proxy........')
        works = []
        for _ in range(len(self.ippools)):
            works.append(Process(target=self.verify_one_proxy, args=(old_queue, new_queue)))
        for work in works:
            work.start()
        for proxy in self.proxies:
            old_queue.put(proxy)
        for _ in works:
            old_queue.put(0)
        for work in works:
            work.join()

        # 更新代理列表
        self.proxies = []
        while True:
            try:
                self.proxies.append(new_queue.get(timeout=1))
            except:
                break
        print('verify_proxies done!')
        print('---------------------')
        for i in self.proxies:
            print(i)

    def verify_one_proxy(self, old_queue, new_queue):
        while True:
            proxy = old_queue.get()
            if proxy == 0:
                break
            try:
                if requests.get('http://www.baidu.com', proxies=proxy, timeout=2).status_code == 200:
                    print('success %s' % proxy)
                    new_queue.put(proxy)
            except:
                print('fail %s' % proxy)


class UAPOOLS(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        """使用代理UA，随机选用"""
        ua = random.choice(self.user_agent_pools)
        print('当前使用的user-agent是' + ua)
        try:
            request.headers.setdefault('User-Agent', ua)
        except Exception as e:
            print(e)
            pass

    user_agent_pools = [
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    ]
