# coding=utf-8
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
import re
import sys
import redis
import time
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import gevent
import random
from gevent import pool
from gevent import monkey; monkey.patch_socket()

red = redis.Redis(host='127.0.0.1', db=1, decode_responses=True)

urls = [
    "http://www.xicidaili.com/nn/{}",
    "http://www.xicidaili.com/nt/{}",
    "http://www.xicidaili.com/wn/{}",
    "http://www.xicidaili.com/wt/{}"
]

headers={"User-Agent": "User-Agent:Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11"}
ip_partten = re.compile(r'\d+\.\d+.\d+.\d+')
TOTALPAGE = 100

def fetch(url, opt):
    try:
        r = requests.get(url, **opt)
        return r
    except Exception as e:
        pass
    return None


def go():
    while True:
        for page in range(1, TOTALPAGE):
            g = []
            for url in urls:
                g.append(gevent.spawn(save_proxy_from_url, url.format(page)))
            gevent.joinall(g)


def save_proxy_from_url(url):
    print(url)
    g = pool.Pool(5)
    opt = {"headers": headers}
    proxy = get_random_ip("http")
    if proxy:
        opt["proxies"] = proxy
    r = fetch(url, opt)
    for m in ip_partten.finditer(r.text):
        match = re.search(r'\d+', r.text[m.end():m.end() + 20])
        if match:
            ip, port = m.group(), match.group()
            print('try to save proxy ', ip, port)
            g.spawn(save_proxy, "http", ip, port)
            g.spawn(save_proxy, "https", ip, port)
    g.join()


def save_proxy(proto, ip, port):
    opt = {"timeout": 10, "verify": False, "headers": headers, "proxies": {}}
    opt["proxies"][proto] = ip + ":" + port
    if proto == "https":
        r = fetch('https://www.baidu.com', opt)
    else:
        r = fetch('http://www.ipip.net', opt)
    if r and r.status_code == 200:
        red.zadd("proxy_" + proto, "{}://{}:{}".format(proto, ip, port), int(time.time()))
    else:
        red.zrem("proxy_" + proto, "{}://{}:{}".format(proto, ip, port))


def check_alive():
    g = pool.Pool(3)
    while True:
        list = red.zrange("proxy_http", 0, -1)
        list.extend(red.zrange("proxy_https", 0, -1))
        print('total proxy ips = ' + str(len(list)))
        for l in list:
            proto = l.split('://')[0]
            ip = l.split('://')[1].split(':')[0]
            port = l.split('://')[1].split(':')[1]
            print("check alive", proto, ip, port)
            g.spawn(save_proxy, proto, ip, port)
        g.join()
        gevent.sleep(60)


def get_random_ip(proto):
    l = red.zcard("proxy_" + proto)
    if l > 0:
        p = random.randint(0, l - 1)
        host = red.zrange("proxy_" + proto, p, p)
        host = host[0]
        o = {}
        o[host.split('://')[0]] = host.split('://')[1]
        return o


if __name__ == '__main__':
    gevent.spawn(check_alive)
    go()