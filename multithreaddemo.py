from multiprocessing.dummy import Pool as ThreadPool
import requests
import time


def getsource(url):
    try:
        html = requests.get(url)
        return html.text
    except :
        return None


def single_thread(urls):
    t1=time.time()
    for i in urls:
        print(i)
        getsource(i)
    t2=time.time()
    print('单线程耗时：{}'.format(str(t2-t1)))



def multi_thread(urls):
    pool = ThreadPool(4)
    t1=time.time()
    results=pool.map(getsource,urls)
    # print(type(results))
    pool.close()
    pool.join()
    t2=time.time()
    print('多线程耗时：{}'.format(str(t2-t1)))

if __name__ == '__main__':
    # 生成待爬网页url
    url = []
    for i in range(1, 21):
        newpage = 'http://tiebao.baidu.com/p/3522395718?pn=' + str(i)
        url.append(newpage)
    # 单线程爬取数据
    single_thread(url)
    # 多线程爬取数据
    multi_thread(url)