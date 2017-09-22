# coding=utf-8
import requests
import redis
import sys
import random
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

headers = {
    "User-Agent": "User-Agent:Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11"}
TOTAL_PROXY = 100

def do_some_thing(iplist):
    for p_ip in iplist:
        proxy = {}
        proto = p_ip.split('://')[0]
        ip = p_ip.split('://')[1]
        proxy[proto] = ip
        if proto == "https":
            url = "https://www.baidu.com/s?wd=ip"
        else:
            url = "http://www.ipip.net"
        try:
            print("proxy ip is " + p_ip)
            r = requests.get(url, proxies=proxy, headers=headers, timeout=10, verify=False)
            if url.find('baidu') > -1:
                print(re.search(r'我的ip地址\d+\.\d+\.\d+\.\d+', r.text).group())
            else:
                print(re.search(r'您当前的IP\S+(\d+\.\d+\.\d+\.\d+)', r.text).group())
        except Exception as e:
            print(e)


if __name__ == '__main__':
    rec = redis.Redis(host='127.0.0.1', db=1, decode_responses=True)
    iplist = rec.zrevrange("proxy_https", 0, TOTAL_PROXY)
    do_some_thing(iplist)