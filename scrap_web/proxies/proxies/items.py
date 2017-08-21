# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProxiesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ip = scrapy.Field()
    port = scrapy.Field()

    address = scrapy.Field()
    # 类型
    cat = scrapy.Field()
    # 协议
    h = scrapy.Field()
    # 存活时间
    life = scrapy.Field()
    # 验证时间
    verify_time = scrapy.Field()
    pass
