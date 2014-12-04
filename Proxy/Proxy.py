# -*- coding: utf-8 -*-

import requests


class Proxy():
    test = ""

    def check_proxies(self, proxy_dictionary, proxy_threads, proxy_timeout):
        ### TODO: Implements checks
        checked_proxy_dict = {}
        thread_results = [None] * 4
        threads = [None] * proxy_threads
        """while len(proxy_dictionary) is not 0:
            key, value = proxy_dictionary.popitem()
            print(key + ": " + str(value))
        """

        return proxy_dictionary