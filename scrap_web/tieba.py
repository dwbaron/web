from datetime import datetime
import re
from collections import defaultdict
from threading import Thread
import sys
import requests
from bs4 import BeautifulSoup


class Tieba:
    def __init__(self, kw, url='http://tieba.baidu.com/f?'):
        self.kw = kw
        self.url = url
        self.response = {}
        self.time = defaultdict(list)
        self.content = defaultdict(list)
        # 查找符合的标签a
        self.pattern = re.compile(r'(?<=<a href=").+(?=class="j_th_tit\s{1}">)')  # 此处有空格
        # 匹配帖子地址
        self.pattern_url = re.compile(r'/p/\d+')
        # 匹配帖子标题
        self.pattern_title = re.compile(r'(?<=title=").+?(?=")')

        # 时间匹配
        self.pattern_time = re.compile(r'(?<=<span class="threadlist_reply_date pull_right j_reply_data" title="最后回复时间">).+?(?=</span>)',
                                       re.DOTALL)

    def get_html(self, pn):

        response = requests.get(self.url + 'kw=' + self.kw + '&pn=' + pn,
                                headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                                                       "Chrome/58.0.3029.110 Safari/537.36"})
        self.response[pn] = response.content

    # 获取主题和url地址
    def get_tags(self, k):

        h = self.response[k]

        # 字符串
        cur = h.decode()
        contents = re.findall(self.pattern, cur)
        # 帖子最后时间

        year = datetime.now().year
        month = datetime.now().month
        day = datetime.now().day

        for time in re.findall(self.pattern_time, cur):

            time = time.strip()
            if ':' in time:
                h = time.split(':')[0]
                m = time.split(':')[1]

                date = datetime(int(year), int(month), int(day), int(h), int(m))
            else:
                month = time.split('-')[0]
                day = time.split('-')[1]
                date = datetime(int(year), int(month), int(day), int(h), int(m))
            self.time[k].append(date)

        # 帖子地址和标题
        for c in contents:

            url = re.findall(self.pattern_url, c)[0]
            title = re.findall(self.pattern_title, c)[0]

            self.content[k].append((url, title))


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

    time_list = []
    # 多线程爬取前10页帖子页面
    for p in range(0, 50, 50):
        thread_html = Thread(target=t.get_html, args=(str(p), ))
        thread_html.start()
        # 必须等待页面爬取结束

        print('----------------------->  ', p)
        thread_html.join()
        t.get_tags(str(p))

    #
    #
    for p, t in zip(t.content['0'], t.time['0']):
        print(p, t)




# from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# driver = webdriver.PhantomJS(executable_path=r"/home/python/phantomjs-2.1.1-linux-x86_64/bin/phantomjs")
# # browser = webdriver.Chrome()
# # browser.get('https://tieba.baidu.com/f?kw=%E9%A9%AC%E6%9D%9C%E5%85%8B&fr=home')
# # browser.find_element_by_class_name('editor_textfield')
#
# browser.find_element_by_class_name('editor_textfield').send_keys(title)
# browser.find_element_by_class_name('edui-body-container').send_keys(con)
# browser.find_element_by_class_name('btn_default').click()
