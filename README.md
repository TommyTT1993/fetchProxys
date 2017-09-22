## fetchProxys

  爬取www.xicidaili.com的代理服务器列表存入redis，并定时检测代理服务器的可用性
ip存在SortedSet里，score是当前时间戳

### start
  
```python3 fetch.py redis // 抓取proxy-list保存到redis```

```python3 fetch.py // 也可以直接保存到文件```

### result

```python3 do_some_thing.py redis // 从redis里获取proxy-list看看效果```

```python3 do_some_thing.py // 从文件中获取```

    proxy ip is https://122.72.32.82:80
    我的ip地址122.72.32.82
    proxy ip is http://122.72.32.82:80
    您当前的IP：122.72.32.82
    proxy ip is http://219.135.164.245:3128
    您当前的IP：219.135.164.245
    proxy ip is http://175.10.188.111:80
    您当前的IP：175.10.188.111
    proxy ip is http://175.10.188.111:80
    您当前的IP：175.10.188.111
    proxy ip is https://122.72.32.88:80
    我的ip地址122.72.32.88
    proxy ip is https://122.72.32.88:80
    我的ip地址122.72.32.88
    proxy ip is http://122.72.32.88:80
    您当前的IP：122.72.32.88
    proxy ip is http://218.20.54.81:9797
    您当前的IP：218.20.54.81
    proxy ip is http://221.215.121.96:8118
