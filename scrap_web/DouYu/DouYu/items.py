# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DouyuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 房间id
    room_id = scrapy.Field()
    # 图片地址
    img_url = scrapy.Field()
    # 分类
    cat = scrapy.Field()
    room_name = scrapy.Field()
    nick_name = scrapy.Field()
    city = scrapy.Field()
    # 房主id
    owner = scrapy.Field()
    # 保存路径
    path = scrapy.Field()
    pass
