#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:gjduan time:2018/4/21

from lxml import etree
import requests
import urllib
import os


# 获取url的html等内容
def getHtml(url):
    try:
        kv = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
        r = requests.get(url, headers=kv, timeout=30)
        r.encoding = 'utf-8'
        return r.text


    except requests.URLError as e:
        print('get html urlerror:{}'.format(e))
        return ''

    except requests.HTTPError as e:
        # code / reason / headers 异常
        print('get html httperror:{}'.format(e))
        return ''


# 获取视频当前页视频url列表
def getVideoList(html):
    try:
        data = etree.HTML(html)
        video_urls = data.xpath('//div[@class="j-video-c"]/div[@data-mp4]')
        # print(type(video_urls[0]))
        # print(dir(video_urls[0]))
        # <a href="2" class="pagenxt">下一页</a>
        next_page = data.xpath('//a[@class="pagenxt"]')
        if next_page:
            next_page = next_page[0].get('href')
       
        # videos[0].get('data-mp4')
        return video_urls, next_page
        # t(video_urls[0].get('data-mp4'))
    except Exception:
        print('lxml parse failed')
        return None, None


# urlretrieve()的回调函数，显示当前的下载进度
# a为已经下载的数据块
# b为数据块大小
# c为远程文件的大小
global myper


def jindu(a, b, c):
    if not a:
        print("连接打开")
    if c < 0:
        print("要下载的文件大小为0")
    else:
        global myper
        per = 100 * a * b / c

        if per > 100:
            per = 100
        myper = per
        print("\r当前下载进度为：" + '%.2f%%' % per, end='')
    if per == 100:
        return True


def getRemoteFileSize(url, proxy=None):
    """ 通过content-length头获取远程文件大小
        url - 目标文件URL
        proxy - 代理  """
    opener = urllib.request.build_opener()
    if proxy:
        if url.lower().startswith('https://'):
            opener.add_handler(urllib.ProxyHandler({'https': proxy}))
        else:
            opener.add_handler(urllib.ProxyHandler({'http': proxy}))
    try:
        request = urllib.Request(url)
        request.get_method = lambda: 'HEAD'
        response = opener.open(request)
        response.read()
    except Exception:  # 远程文件不存在
        return 0
    else:
        fileSize = dict(response.headers).get('content-length', 0)
        return int(fileSize)


if __name__ == '__main__':

    path = os.path.join(os.path.abspath(os.path.curdir), 'videos')
    if not os.path.exists(path):
        os.mkdir(path)
    url = "http://www.budejie.com/video"
    next_url = url
    n = 0
    while True:
        html = getHtml(next_url)
        # print(html)

        videos, nextpage = getVideoList(html)
        print('\n下载第{}页视频数据:{}'.format(n + 1, next_url))
        # print(videos[0].get('data-mp4'))
        if not videos:
            break
        for v in videos:
            # if v:
            video_url = v.get('data-mp4')
            print('下载：{}'.format(video_url))
            p = os.path.join(path, v.get('data-mp4').split('/')[-1])

            if not os.path.exists(p):
                try:  #
                    # 使用request.build_opener 添加head可解决用urllib提示403错误                                                                                                                  #
                    # myheaders = [('User - Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebK# it/525.17'\
                    #                               '#  (KHTML, like Gecko) Version/3.1 Safari/525.17'),]
                    # opener = urllib.request.build_opener# ()
                    # opener.addheaders = myheaders #
                    # urllib.request.install_opener(opener)
                    urllib.request.urlretrieve(video_url, p, jindu)
                except Exception:
                    print("\n下载文件：{}失败".format(video_url))
            # else:
            #     remote_size = getRemoteFileSize(video_url)
            #     local_size = os.path.getsize(p)
            #     print('remote_size:{}'.format(remote_size))
            #     print('local_size:{}'.format(local_size))

        # 检测是否有下一页
        if nextpage:
            if nextpage == '1':
                break
            next_url = url + '/' + nextpage
        else:
            break
        n = n + 1

    print('所有数据抓取完毕！')
