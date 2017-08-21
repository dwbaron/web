# -*- coding: utf-8 -*-
import re
import scrapy
from proxies.items import ProxiesItem


class XiciProxySpider(scrapy.Spider):
    name = 'xici_proxy'
    allowed_domains = ['xicidaili.com']
    start_urls = ['http://www.xicidaili.com']

    def parse(self, response):

        odd_items = response.xpath('//tr[@class="odd"]')
        even_items = response.xpath('//tr[@class=""]')

        print('---- start ----')
        # 扩充列表
        odd_items.extend(even_items)

        for items in odd_items:
            proxy = ProxiesItem()
            proxy['ip'] = items.xpath('./td[2]/text()').extract_first()
            # print(proxy['ip'])
            proxy['port'] = items.xpath('./td[3]/text()').extract_first()
            proxy['h'] = items.xpath('./td[6]/text()').extract_first()
            proxy['address'] = items.xpath('./td[4]/text()').extract_first()
            proxy['cat'] = items.xpath('./td[5]/text()').extract_first()
            proxy['life'] = items.xpath('./td[7]/text()').extract_first()
            proxy['verify_time'] = items.xpath('./td[8]/text()').extract_first()

            yield proxy

        pass




