import requests
import redis
import sys
import random
import re

headers = {
    "User-Agent": "User-Agent:Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11"}
TOTAL_PROXY = 100

def do_some_thing(iplist):
    for ip in iplist:
        proxy = {}
        proxy[ip.split('://')[0]] = ip.split('://')[1]
        if ip.split('://')[0] == "https":
            print("proxy ip is " + ip.split('://')[1])
            try:
                r = requests.get("https://www.baidu.com/s?wd=ip", proxies=proxy, headers=headers)
                print(re.search(r'我的ip地址\d+\.\d+\.\d+\.\d+', r.text).group())
            except:
                pass


if __name__ == '__main__':
    iplist = []
    if sys.argv[-1] == "redis":
        rec = redis.Redis(host='127.0.0.1', db=1, decode_responses=True)
        # order by latency
        iplist = map(lambda e:e.split('#'), rec.zrevrange("proxy", 0, TOTAL_PROXY))
        iplist = list(map(lambda e:e[0], sorted(iplist, key=lambda e: e[1])))
    else:
        iplist = open("record.txt", "r").read().split('\n')
    do_some_thing(iplist)