# -*- coding: utf-8 -*-
import scrapy

from tencent.items import TencentItem


class TencentJobSpider(scrapy.Spider):
    name = 'tencent_job'
    allowed_domains = ['tencent.com']
    start_urls = ['http://hr.tencent.com/position.php']

    # 爬取详情页
    def parse_detail(self, response):
        print('====================')
        item = response.meta['item']

        nodes_work = response.xpath('//tr[@class="c"][1]/td/ul/li')
        nodes_require = response.xpath('//tr[@class="c"][2]/td/ul/li')
        work_list = []
        require_list = []

        for work, require in zip(nodes_work, nodes_require):
            print(work.xpath('/text()').extract_first())
            work_list.append(work.xpath('text()').extract_first())
            require_list.append(require.xpath('text()').extract_first())

        item['work'], item['require'] = work_list, require_list

        return item

    def parse(self, response):
        nodes = response.xpath('//tr[@class="even"]|//tr[@class="odd"]')
        print('-----------> ', len(nodes))
        base_url = 'http://hr.tencent.com/'

        for node in nodes:
            item = TencentItem()
            cur_url = node.xpath('./td[1]/a/@href').extract_first()

            item['job'] = node.xpath('./td[1]/a/text()').extract_first()
            item['cat'] = node.xpath('./td[2]/text()').extract_first()
            item['num'] = node.xpath('./td[3]/text()').extract_first()
            item['address'] = node.xpath('./td[4]/text()').extract_first()
            item['pub_time'] = node.xpath('./td[5]/text()').extract_first()

            # 详情页
            detail_url = base_url + cur_url
            yield scrapy.Request(detail_url, meta={'item': item}, callback=self.parse_detail)

<<<<<<< HEAD
        # # 获取下一页url
        # next_url = base_url + response.xpath('//a[@id="next"]/@href').extract_first()
        # # 创建新请求，并返回且引擎
        # yield scrapy.Request(next_url, callback=self.parse)
=======
        # 获取下一页url
        next_url = base_url + response.xpath('//a[@id="next"]/@href').extract_first()
        # 创建新请求，并返回且引擎
        yield scrapy.Request(next_url, callback=self.parse)
>>>>>>> 2c1067c4c308529d19cd5b6c073eb20a5a2c04ff
