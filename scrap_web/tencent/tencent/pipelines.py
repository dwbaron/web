# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
<<<<<<< HEAD


class TencentPipeline(object):
    # 创建存储数据的文件
    def open_spider(self, spider):
        self.file = open('tencent.json', 'w')

    # 处理数据
    def process_item(self, item, spider):
        # 先将item串转化成字典，再将字典转化成字符串
        data = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        # 写入文件
        self.file.write(data)

=======
from collections import defaultdict


class TencentPipeline(object):
    # def __init__(self):
        # self.data = defaultdict(list)

    # 创建存储数据的文件
    def open_spider(self, spider):
        self.file = open('data.json', 'w', encoding='utf-8')

    # 处理数据
    def process_item(self, item, spider):

        # 将item、
        # 先将item串转化成字典，再将字典转化成字符串
        # 写入文件
        data = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(data)
>>>>>>> 2c1067c4c308529d19cd5b6c073eb20a5a2c04ff
        return item

    # 关闭保存数据的文件
    def close_spider(self, spider):
        self.file.close()
