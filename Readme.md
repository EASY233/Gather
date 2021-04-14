## 前言

Gather是一个数据采集工具，使用python3编写，使用的时候请确保运行环境为python3.6以上。Gather支持Fofa，钟馗之眼(Zoomeye),Shodan的数据采集。

## 使用说明

Gather极力避免各种繁杂的参数，使用-aF or aZ or -aS 指定特定采集方式即可。

```
git clone
pip install -r requirements.txt
python3 Gather.py -h
  -aF         Using fofa to collect data
  -aZ         Using Zoomeye to collect data
  -aS         Using Shodan to collect data

```

## 配置文件

在根目录下的``config.py``进行api等配置,注意fofa不是使用api进行调用而是使用爬虫的方式，需要填入fofa_token(没有钱开通会员，没有办法使用api进行测试所以没有写api调用版本~)。

```txt
fofa_token = ""
# 一轮抓取结束后，休眠时间，防止被fofa拉黑
time_sleep = 5
time_out = (10, 10)
page_host_limit = 10

# Zoomeye配置文件
email = ""
password = ""

# Shodan配置文件
api_key = ""
```

## 运行效果

通过fofa进行数据采集，该脚本修改自开源项目:[[fofa_spider-1.0.3](https://github.com/FightingForWhat/fofa_spider-1.0.3)

![](https://picbed.easy233.top//imgimage-20210414210322955.png)

通过Zoomeye进行数据采集:

![](https://picbed.easy233.top//imgimage-20210414210427953.png)

通过Shodan进行数据采集:

![](https://picbed.easy233.top//imgimage-20210414210538305.png)

