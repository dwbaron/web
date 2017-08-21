import json
import re
from collections import defaultdict
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import os


# 获取cookies,返回字典
def get_cookie(cookie):
    cookies = {}
    for line in cookie.split(';'):
        name, value = line.strip().split('=', 1)  # 1代表只分割一次
        cookies[name] = value
    return cookies


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
# ban = defaultdict(list)
# html = requests.get('http://tieba.baidu.com/home/main?un=%E8%8B%B1%E9%9B%84%E7%99%BE%E6%88%98&ie=utf-8&fr=pb&red_tag=h2276515409').content
# soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
# result1 = soup.find_all('a', class_='n_name')
# result2 = soup.find_all('a', class_='reply_content')
#
#
# for r1, r2 in zip(result1, result2):
#     if '马杜克' in r1.text:
#         url = r2['href']
#         ban['英雄百战'].append(url)
# print(ban['英雄百战'])


# 获取每页的楼层信息
def find_all_levels(url):
    html = requests.get(url, headers=headers).content
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    # 楼主信息
    res1 = soup.find_all('div', class_='d_author')
    # res2 = soup.find_all('div', class_='l_post')
    for r in res1:
        print(type(r))
        r0 = r.find_all('li', class_='d_name')[0]
        name = r0.a.text
        print(name)


# 根据url初始soup对象
def create_soup(url):
    html = requests.get(url, headers=headers).content
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    return soup


# 共有多少页,返回整数
def find_pages(soup):
    pages = soup.find_all('li', class_='l_reply_num')

    print(pages[0].text)
    p = pages[0].text
    p = re.findall(re.compile(r'(?<=共)\d+'), p)[0]
    return int(p)


# 爬取并且保存图片
def scrap_pics(soup, base_path):
    lzl_reply = soup.find_all('img')
    print('----- start -----')
    # 保证图片名字唯一
    for i, l in enumerate(lzl_reply):
        # 去除特殊符号
        string = re.sub(r'_|\?v=tbs|-| ', '', str(l['src']))
        o_path = re.findall(re.compile(r'(?<=/)\w+(?:(?:\.jpg)|(?:\.png)|(?:\.gif))$'), string)
        if o_path:
            o_path = o_path[0]
        else:
            continue
        n_path = str(i) + o_path
        print(n_path)
        # print(str(l['src']))
        try:
            res = requests.get('http://imgsrc.baidu.com/forum/pic/item/' + o_path)

        except Exception as e:
            try:
                res = requests.get(l['src'])
                # print(res)
                with open(base_path + n_path, 'wb') as f:
                    f.write(res.content)
            except Exception as e:
                print('[error pass]')

        else:
            # print(res)
            with open(base_path + n_path, 'wb') as f:
                f.write(res.content)


def recursive_pics(url_list, base_path='./tieba_pics/hzw02/'):
    if not os.path.exists('./tieba_pics/hzw02/'):
        os.mkdir('./tieba_pics/hzw02/')

    for url in url_list:
        soup = create_soup(url)

        num_pages = find_pages(soup)

        for p in range(1, num_pages + 1):

            if p >= 2:
                p_url = url + '?pn=' + str(p)

                soup = create_soup(p_url)

            scrap_pics(soup, base_path)

            print('***----- page', p, ' ------***')


# recursive_pics(['https://tieba.baidu.com/p/4337601672'])


# find_all_levels('https://tieba.baidu.com/p/5270574374')

# 楼中楼回复的页面
"https://tieba.baidu.com/p/comment?tid=5250619642&pid=110035730730&pn=1"


def get_all(tid):

    soup = create_soup('https://tieba.baidu.com/p/{}'.format(tid))
    num_pages = find_pages(soup)
    url = 'https://tieba.baidu.com/p/{}'.format(tid)
    for p in range(1, num_pages + 1):

        if p >= 2:
            p_url = url + '?pn=' + str(p)
            soup = create_soup(p_url)
        res = soup.find_all('cc')

        for p in res:
            print(p.find_all('div', class_='d_post_content'))
            pid = re.findall(re.compile(r'\d+'), p.div['id'])[0]
            # lzl回复的地址
            lzl_url = 'https://tieba.baidu.com/p/comment?tid=' + tid + '&pid=' + pid + '&pn=1'
            lzl_soup = create_soup(lzl_url)
            pages = lzl_soup.find_all('li', class_='lzl_li_pager')[0]
            js = json.loads(pages['data-field'])
            if not js['total_num']:
                continue
            num_pages = js['total_page']
            for lzl_p in range(1, int(num_pages) + 1):
                cur_url = 'https://tieba.baidu.com/p/comment?tid=' + tid + '&pid=' + pid + '&pn={}'.format(lzl_p)
                cur_soup = create_soup(cur_url)
                for l_reply in cur_soup.find_all('div', class_='lzl_cnt'):
                    print(' ' * 4, l_reply.a.text, ': ', l_reply.span.text.strip())


get_all('5177695506')
