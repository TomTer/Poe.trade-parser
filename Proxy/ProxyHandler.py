# -*- coding: utf-8 -*-


import requests


proxies = {
    "http": "183.224.1.55:80"
}

page = requests.get("http://poe.trade/", timeout=4, proxies=proxies)

print(page.status_code)
