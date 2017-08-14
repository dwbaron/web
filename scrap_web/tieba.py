import re
from collections import defaultdict
from threading import Thread
import sys
import requests


class Tieba:
    def __init__(self, kw, url='http://tieba.baidu.com/f?'):
        self.kw = kw
        self.url = url
        self.res = {}
        self.content = defaultdict(list)
        # 查找符合的标签a
        self.pattern = re.compile(r'(?<=<a href=").+(?=class="j_th_tit\s{1}">)')  # 此处有空格
        # 匹配帖子地址
        self.pattern_url = re.compile(r'/p/\d+')
        # 匹配帖子标题
        self.pattern_title = re.compile(r'(?<=title=").+?(?=")')

    def get_html(self, pn):

        response = requests.get(self.url + 'kw=' + self.kw + '&ie=utf-8' + '&pn=' + pn,
                                headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                                                       "Chrome/58.0.3029.110 Safari/537.36"})
        # 字符串
        cur = response.content.decode()

        self.res[pn] = cur

    # 获取主题和url地址
    def get_tags(self):

        for k, h in self.res.items():
            pair_list = []
            contents = re.findall(self.pattern, h)

            for c in contents:

                url = re.findall(self.pattern_url, c)[0]
                title = re.findall(self.pattern_title, c)[0]
                pair_list.append((url, title))

            self.content[k] = pair_list


if __name__ == '__main__':

    # 可以接受命令行参数
    query = ''
    if len(sys.argv) >= 2:
        query = sys.argv[1]
    if query:
        t = Tieba(query)

    # 默认海贼王贴吧
    else:
        t = Tieba('海贼王')

    # 多线程爬取前10页帖子页面
    for p in range(0, 500, 50):
        thread_html = Thread(target=t.get_html, args=(str(p), ))
        thread_html.start()
        # 必须等待页面爬取结束
        thread_html.join()

    t.get_tags()

    # 显示第一页的帖子内容
    for i in t.content['0']:
        print(i)
