# coding:utf-8
# !/usr/bin/env python
import requests
import re
import os
from bs4 import BeautifulSoup

# import time


# 通过url获取html内容
def getHtml(url):
    try:
        kv = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=kv, timeout=30)
        r.raise_for_status()
        r.encoding = 'gbk'  # r.apparent_encoding
        return r.text
    except:
        print('get html:{} failed'.format(url))
        return ""


# 获取全书分类目录
def getArticleTypeList(typelist):
    for title_name, title_url in typelist:
        # print(name,url)
        p = os.path.join(path, title_name)
        if not os.path.exists(p):
            os.mkdir(p)
        print(title_url)
        getOneTypeArticleUrl(title_name, title_url)
        # break


# 取得全书指定类型所有书
def getOneTypeArticleUrl(title_name, title_url):
    # todo :优化
    html = getHtml(title_url)
    if not html == "":
        # 取得全书指定类型书的当前页url
        bs = BeautifulSoup(html, 'html.parser')

        cfs = bs.find('ul', class_="seeWell cf")
        lis = cfs.find_all('li')

        for li in lis:
            # get title
            a = li.find('a', class_='clearfix stitle')
            if a:
                text = a.text
                print(a.text)
                ul = a.get('href')
                print(ul)

                # 创建书目录
                p = os.path.join(path, title_name)
                p = os.path.join(p, str(text).replace('/', '-'))
                if not os.path.exists(p):
                    os.mkdir(p)
                getChapterContent(p, ul)
                # debug 获取特定类型书的第一本书的内容
                # break
        # 递归调用全书指定类型书的下一页url
        # 测试获取当前页内容即第一页的内容
        next_page = bs.find_all('div', class_=r'pagelink')
        if next_page:
            next_url = next_page[0].find_all('a', class_=r'next')
            # print(next_url)
            if next_url:
                print(next_url[0])
                np_url = next_url[0].get('href')
                if np_url:
                    getOneTypeArticleUrl(title_name, np_url)


# 获得全书指定类型指定书章节url,title
def getChapterContent(path, url):
    # todo ：优化
    # 取得书指定类型书的具体某本书的阅读地址
    html = getHtml(url)
    bs = BeautifulSoup(html, 'html.parser')
    u = bs.find_all('a', class_='reader')
    if u:
        # print(t_url)
        book_url = u[0].get('href')
        print("阅读地址：" + book_url)
    else:
        print("not find the book url:{}".format(url))
        return
    # 打开阅读书的阅读章节url
    html = getHtml(book_url)

    bs = BeautifulSoup(html, 'html.parser')
    ulist = bs.find_all('div', class_='clearfix dirconone')
    if ulist:
        urls = ulist[0].find_all('a')
        if urls:
            # print(urls)
            for a in urls:
                ch_url = a.get('href')
                name = a.text
                if name == "":
                    title = a.get('title')
                    if title and title != '':
                        name = title
                    else:
                        name = re.split(r'/', book_url)[-1:]
                name = re.sub(r'/', r'-', name)
                p1 = os.path.join(path, name + '.txt')
                if os.path.exists(p1) and os.path.getsize(p1) > 0:
                    print('file:{} is existed!!!'.format(p1))
                    # continue
                    break  # 测试发现如果曾经获取过数据，就暂时不获取
                print(p1)
                # 获取书的章节内容
                with open(p1, 'w') as fp:
                    fp.close()
                getBookContent(p1, ch_url)
                # debug 测试仅获取第1章内容
                break


# 获取书的章节内容
def getBookContent(path, url):
    html = getHtml(url)
    bs = BeautifulSoup(html, 'html.parser')
    if bs:
        content = bs.find_all('div', class_='mainContenr')
        if content and len(content) > 0:
            text = content[0].text
            text = re.sub(r'style\d?\(\);', '', text)
            print(text)
            print(url)
            with open(path, 'a') as fp:
                fp.write(text)
            fp.close()


# 主函数入口
def main():
    enter_url = "http://www.quanshuwang.com/list/1_1.html"
    book_html = getHtml(enter_url)

    bs = BeautifulSoup(book_html, 'html.parser')
    title = bs.find_all('ul', class_="channel-nav-list")
    if not title:
        return

    tag = title[0]

    aa = tag.find_all('a')
    book_type_list = []
    for a in aa:
        u = a.get('href')
        t = a.text
        book_type_list.append((t, u))

    global path
    path = os.path.join(os.path.abspath(os.path.curdir), 'books')
    if not os.path.exists(path):
        os.mkdir(path)

    getArticleTypeList(book_type_list)

    print("恭喜网站所有数据采集完毕！")


if __name__ == '__main__':
    main()
