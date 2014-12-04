# -*- coding: utf-8 -*-

import re
import time
import threading
import requests
import Settings


class Currency():

    currency_standard_dict = None
    currency_hardcore_dict = None

    STANDARD_CURRENCY_URL = "http://exilebro.com/currency/rates/standard/"
    HARDCORE_CURRENCY_URL = "http://exilebro.com/currency/rates/hardcore/"

    CURRENCY_PATTERN_CHAOS_LEFT_SIDE = r'class="btn bg-grey-cascade btn-sm">(.{1,50})</span>' \
                                       r'.{1,40}<span.{1,50}>(.{1,5})</span>.{1,5}<span.{1,50}>1</span>' \
                                       r'.{1,50}<span.{1,50}>Chaos orb</span>'
    CURRENCY_PATTERN_CHAOS_RIGHT_SIDE = r'class="btn bg-grey-cascade btn-sm">Chaos Orb' \
                                        r'</span>.{1,50}<span.*?>(.*?)<.{5,50}">1' \
                                        r'</span>.{10,50}<span.*?>(.*?)</span>'

    def get_league_currencies_dictionary(self, currency_url):
        """
        Parses web page and gets all currencies to chaos orb
        :param currency_url: url to web page with currency exchanges (exilebro only)
        :return: currencies as dictionary
        """
        currency_dictionary = {}
        #page_download_timestamp = time.time() # DEBUG
        page = requests.get(currency_url)
        if page.status_code is not 200:
            return False
        # DEBUG
        #print("Page downloaded in: {download_time:.4f}s".format(download_time=(time.time() - page_download_timestamp)))
        #regex_timestamp = time.time() # DEBUG

        matched_left_side = re.findall(self.CURRENCY_PATTERN_CHAOS_LEFT_SIDE, str(page), re.I | re.S)
        matched_right_side = re.findall(self.CURRENCY_PATTERN_CHAOS_RIGHT_SIDE, str(page), re.I | re.S)

        for match in matched_left_side:
            currency_name = match[0]
            currency_rate = match[1]
            currency_dictionary[currency_name] = currency_rate

        for match in matched_right_side:
            currency_name = match[1]
            currency_rate = match[0]
            currency_dictionary[currency_name] = currency_rate
        # DEBUG
        #print("Regex parsed in: {download_time:.4f}s\n".format(download_time=(time.time() - regex_timestamp)))
        return currency_dictionary

    def get_standard_currencies_dictionary(self, result_array, index):
        result_array[index] = self.get_league_currencies_dictionary(self.STANDARD_CURRENCY_URL)

    def get_hardcore_currencies_dictionary(self, result_array, index):
        result_array[index] = self.get_league_currencies_dictionary(self.HARDCORE_CURRENCY_URL)

    def get_all_currencies_multithreading(self):
        """
        Function parses all currency pages in multiple threads and returns results
        :return: list with dictionaries
        """
        thread_results = [None] * 2
        threads = [None] * 2

        threads[0] = threading.Thread(target=self.get_standard_currencies_dictionary,
                                      args=(thread_results, 0))
        threads[1] = threading.Thread(target=self.get_hardcore_currencies_dictionary,
                                      args=(thread_results, 1))
        # Start threads
        for i in range(len(threads)):
            threads[i].start()

        # Wait for threads to finish
        for i in range(len(threads)):
            threads[i].join()

        return thread_results

    def set_currencies(self):
        """
        Function sets currencies to this class dictionaries
        :return: returs nothing
        """
        currency_thread_result = self.get_all_currencies_multithreading()
        self.currency_standard_dict = currency_thread_result[0]
        self.currency_hardcore_dict = currency_thread_result[1]
        print("set_currencies finished")

    def set_reset_currency_thread(self, delay_in_seconds):
        """
        Function resets currencies to this class dictionaries and waits for a delay in seconds
        :param delay_in_seconds: delay to wait between next reset
        :return: returns nothing
        """
        while Settings.get_reset_currency_working():
            time.sleep(delay_in_seconds)
            self.set_currencies()
