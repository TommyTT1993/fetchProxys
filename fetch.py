# coding=utf-8
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
import re
import sys
import redis
import time
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
rec = None

urls = [
    "http://www.xicidaili.com/nn/{}",
    "http://www.xicidaili.com/nt/{}",
    "http://www.xicidaili.com/wn/{}",
    "http://www.xicidaili.com/wt/{}"
]

headers={"User-Agent": "User-Agent:Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11"}


def fetch(url, opt):
    try:
        r = requests.get(url, **opt)
        return r
    except Exception as e:
        pass
    return None


def go():
    ip_partten = re.compile(r'\d+\.\d+.\d+.\d+')
    for page in range(0, 10):
        for url in urls:
            r = fetch(url.format(1), {"headers": headers})
            for m in ip_partten.finditer(r.text):
                match = re.search(r'\d+', r.text[m.end():m.end() + 20])
                if match:
                    ip, port = m.group(), match.group()
                    latency = check_proxy("http", ip, port)
                    if latency:
                        record("http", ip, port, latency)
                    latency = check_proxy("https", ip, port)
                    if latency:
                        record("https", ip, port, latency)


def check_proxy(proto, ip, port):
    opt = {"timeout": 5, "verify": False, "headers": headers, "proxies": {}}
    opt["proxies"][proto] = ip + ":" + port
    r = fetch('https://www.baidu.com', opt)
    if r and r.status_code == 200:
        return r.elapsed.microseconds / 1000


def record(proto, ip, port, latency):
    print(proto, ip, port)
    if isinstance(rec, redis.Redis):
        rec.zadd("proxy", "{}://{}:{}#{}".format(proto, ip, port, latency), int(time.time()))
    else:
        rec.write("{}://{}:{}\n".format(proto, ip, port, latency))


if __name__ == '__main__':
    if sys.argv[-1] == "redis":
        rec = redis.Redis(host='127.0.0.1', db=1)
    else:
        rec = open("record.txt", "w")
    go()
