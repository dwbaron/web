# -*- coding: utf-8 -*-
import json

import scrapy
from DouYu.items import DouyuItem


class DouyuSpider(scrapy.Spider):
    name = 'douyu'
    # 修改允许的域名
    allowed_domains = ['capi.douyucdn.cn']
    # 偏移量,加载更多数据使用
    offset = 0
    base = 'http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=100&offset='
    # 修改起始的url列表
    start_urls = [base]

    def parse(self, response):
        # api 返回的是json格式
        res = json.loads(response.body.decode('utf-8'))
        # 数据列表
        data = res['data']
        for item in data:
            douyu = DouyuItem()
            douyu['room_id'] = item['room_id']
            douyu['room_name'] = item['room_name']
            douyu['img_url'] = item['vertical_src']
            douyu['cat'] = item['cate_id']
            douyu['owner'] = item['owner_uid']
            douyu['nick_name'] = item['nickname']
            douyu['city'] = item['anchor_city']

            yield douyu

        # 偏移量判断
        if len(data) != 0:
            # 拼接下一个url
            self.offset += 100
            next_url = self.base + str(self.offset)
            # 请求后续数据
            yield scrapy.Request(next_url, callback=self.parse)




