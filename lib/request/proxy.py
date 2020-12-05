#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 用于获取代理

from bs4 import BeautifulSoup
import requests
import random
import json


class ProxyIp():

    proxys = []


    @staticmethod
    def get_proxy_ip():
        if len(ProxyIp.proxys) == 0:
            ProxyIp.gen_or_refresh_proxys()
        return random.choice(ProxyIp.proxys)


    @staticmethod
    def remove_proxy_ip(proxy):
        ProxyIp.proxys.remove(proxy)


    @staticmethod
    def gen_or_refresh_proxys():
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
            'Host': 'www.kuaidaili.com'
        }

        url = 'https://www.kuaidaili.com/free/inha/1/'
        response = requests.get(url, headers=headers)
        page = BeautifulSoup(response.text, 'lxml')

        ips = [tag.text for tag in page.find_all("table", "table table-bordered table-striped")[0].tbody.find_all("td") if tag["data-title"] == "IP"]
        ports = [tag.text for tag in page.find_all("table", "table table-bordered table-striped")[0].tbody.find_all("td") if tag["data-title"] == "PORT"]
        types = [tag.text for tag in page.find_all("table", "table table-bordered table-striped")[0].tbody.find_all("td") if tag["data-title"] == "类型"]

        temp_proxies = []
        for i in range(len(ips)):
            proxy = {"https": ips[i] + ":" + ports[i]}
            print(proxy)
            if ProxyIp.check_if_effect(proxy):
                temp_proxies.append(proxy)

        ProxyIp.proxys = temp_proxies


    @staticmethod
    def check_if_effect(proxy):
        try:
            local_ip = ProxyIp.get_bin_ip()
            proxy_ip = ProxyIp.get_bin_ip(proxy)
            if proxy_ip != local_ip:
                return True
            else:
                return False
        except Exception as e:
            print(proxy, e)
            return False


    @staticmethod
    def get_bin_ip(proxy=None):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15'
        }
        url = 'http://httpbin.org/ip'
        response = requests.get(url, headers=headers, proxies=proxy)
        return json.loads(response.text)["origin"]


if __name__ == '__main__':
    ProxyIp.gen_or_refresh_proxys()
    ProxyIp.get_proxy_ip()
