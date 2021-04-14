#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = EASY
import sys
import os
import time
import requests
import getpass
from config import email,password,Save_Path


class ZoomEye:
    def __init__(self,username=None, password=None):
        self.username = username
        self.password = password
        self.token = ''
        self.result = []
        self.Flag = True
        self.zoomeye_login_api = "https://api.zoomeye.org/user/login"
        self.zoomeye_dork_api = "https://api.zoomeye.org/{}/search"
        self.auto_login()
        print("[*] login success!")
        info = self.resources_info().get('resources')
        if info:
            print('[*] Available ZoomEye search: (search:%s)' % (info.get('search', 'NO FOUND')))
        keyword = input("请输入Zoomeye搜索关键字:")
        start_pages = input("请输入开始页数:")
        end_pages = input("请输入介绍页数:")
        for page_n in range(int(start_pages), int(end_pages)+1):
            data  = self.dork_search(keyword, int(page_n))
            if data:
                for i in data:
                    ip_str = i.get('ip')
                    if 'portinfo' in i.keys():
                        ip_str = ip_str + ':' + str(i.get('portinfo').get('port'))
                    print(ip_str)
                    self.result.append(ip_str)
            else:
                break
        self.save()


    def auto_login(self):
        try:
            self.username = email
            self.password = password
        except:
            pass
        if bool(self.username and self.password):
            if self.get_token():
                return
        print("[*] Automatic authorization failed.")
        self.manual_login()

    def manual_login(self):
        msg = print('[*] Please input your ZoomEye Email and Password below.')
        self.username = input('ZoomEye Username(Email): ').strip()
        self.password = getpass.getpass(prompt='ZoomEye Password: ').strip()
        if not self.get_token():
            msg = 'Invalid ZoomEye username or password.'
            sys.exit(msg)

    def get_token(self):
        # Please access https://www.zoomeye.org/api/doc#login
        data = '{{"username": "{}", "password": "{}"}}'.format(self.username,
                                                               self.password)
        resp = requests.post(self.zoomeye_login_api, data=data)
        if resp and resp.status_code == 200 and 'access_token' in resp.json():
            self.token = resp.json().get('access_token')
            return self.token
        return False

    def setToken(self, token):
        """set Token from exist token string"""
        self.token = token.strip()

    def dork_search(self, dork, page=1, resource='host', facet=['ip']):
        """Search records with ZoomEye dorks.

        param: dork
               ex: country:cn
               access https://www.zoomeye.org/search/dorks for more details.
        param: page
               total page(s) number
        param: resource
               set a search resource type, ex: [web, host]
        param: facet
               ex: [app, device]
               A comma-separated list of properties to get summary information
        """
        result = []
        if isinstance(facet, (tuple, list)):
            facet = ','.join(facet)

        zoomeye_api = self.zoomeye_dork_api.format(resource)
        headers = {'Authorization': 'JWT %s' % self.token}
        params = {'query': dork, 'page': page, 'facet': facet}
        resp = requests.get(zoomeye_api, params=params, headers=headers)
        if resp and resp.status_code == 200 and 'matches' in resp.json():
            matches = resp.json().get('matches')
            if self.Flag:
                total = resp.json().get("total")
                print("[*] 共搜索到{}".format(total))
                self.Flag = False
            # total = resp.json().get('total')  # all matches items num
            result = matches


        return result

    def resources_info(self):
        """Resource info shows us available search times.

        host-search: total number of available host records to search
        web-search: total number of available web records to search
        """
        data = None
        zoomeye_api = "https://api.zoomeye.org/resources-info"
        headers = {'Authorization': 'JWT %s' % self.token}
        resp = requests.get(zoomeye_api, headers=headers)
        if resp and resp.status_code == 200 and 'plan' in resp.json():
            data = resp.json()

        return data


    def save(self):
        path = os.path.join(Save_Path,"Zoomeye_{}.txt".format(time.strftime('%Y%m%d%H%M%S')))
        with open(path,'w',encoding="utf-8") as file:
            for line in self.result:
                file.write(line + '\n')

        print("")
        print("[*] 结果保存在:{}".format(path))
