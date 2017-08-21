# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class TencentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    job = scrapy.Field()
    url = scrapy.Field()
    cat = scrapy.Field()
    num = scrapy.Field()
    address = scrapy.Field()
    pub_time = scrapy.Field()

    # 职责
    work = scrapy.Field()
    # 要求
    require = scrapy.Field()
