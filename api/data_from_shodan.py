#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = EASY
import sys
import shodan
import os
import time
from config import api_key,Save_Path

class Shodan:
    def __init__(self):
        self.result = []
        self.login()
        api = shodan.Shodan(self.api_key)
        self.query = input("[*] 请输入Shodan搜索关键词:").strip()
        total = api.search(self.query)['total']
        print("[*] 共搜索到结果:{}".format(total))
        if total == 0:
            sys.exit("没有搜索到结果，请检查关键词！！")
        self.limit = int(input("[*] 请输入你需要的数量:").strip())
        try:
            context = api.search(query=self.query,offset=0,limit=self.limit)
        except Exception as e:
            pass
        if 'matches' in context:
            for match in context.get('matches'):
                ip_port = match.get('ip_str') + ':' + str(match.get('port'))
                self.result.append(ip_port)
                print(ip_port)
        else:
            self.result = []
        self.save()

    def login(self):
        self.api_key = api_key
        if not self.api_key:
            print("[*] Automatic authorization failed.Please input your Shodan API Key (https://account.shodan.io/)")
            self.api_key = input('API_KEY >').strip()
        try:
            api = shodan.Shodan(self.api_key)
            account_info = api.info()
            print("[*] login success！")
            print("[*] Available Shodan query credits: %d" % account_info.get('query_credits'))

        except Exception as e:
            exit(0)

    def save(self):
        path = os.path.join(Save_Path,"Shodan_{}.txt".format(time.strftime('%Y%m%d%H%M%S')))
        with open(path,'w',encoding="utf-8") as file:
            for line in self.result:
                file.write(line + '\n')
        print("")
        print("[*] 结果保存在:{}".format(path))
