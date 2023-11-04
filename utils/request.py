import requests
import random
import time
import numpy as np 
import io 
import sys
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root_path)

import utils.config as cfg
from utils.logger import Logger

log = Logger('search')


class Request:
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
    ]

    def __init__(self):
        # self.proxies = {
        #     'http': 'socks5h://127.0.0.1:9050',
        #     'https': 'socks5h://127.0.0.1:9050'
        # }
        self.session = requests.session()
        # self.session.proxies = {
        #     'http': 'socks5h://127.0.0.1:9050',
        #     'https': 'socks5h://127.0.0.1:9050'
        # }
        # self.user_agent = self.random_user_agent()


    def get_kukala_product_image(src):
        # url = "http://192.168.110.45:5200/product/images/GetImage/2023-11-04/3228019768045198323_1.jpg"
        url = f"http://192.168.110.45:5200/product/images/GetImage/{src}"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 200:
            image_data = response.content
        else:
            log.error('image not found! ')
            image_data = None
        return image_data
    
    

    def tor_get_request(self, url, params=None, headers=None):
        if headers is None:
            headers = {}
        headers['User-Agent'] = self.random_user_agent()
        if params is None:
            params = {}
        counter = 0
        while True:
            try:
                res = self.session.get(url, params=params,
                                       headers=headers, timeout=10)
                # res = requests.get(url, params=params,
                #                    headers=headers, proxies=self.proxies)
                return res.text
            except Exception as e:
                try:
                    time.sleep(3)
                    counter += 1
                    self.change_session()
                except:
                    pass

    def tor_post_request(self, url, params=None, headers=None):
        if headers is None:
            headers = {}
        headers['User-Agent'] = self.random_user_agent()
        if params is None:
            params = {}
        res = self.session.post(url, params=params,
                                headers=headers)
        # res = requests.post(url, params=params,
        #                     headers=headers, proxies=self.proxies)
        return res.text

    def random_user_agent(self, wa=None):
        return random.choice(self.user_agent_list)

    def change_session(self):
        self.session = requests.session()
        self.session.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
