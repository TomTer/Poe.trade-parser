# -*- coding: utf-8 -*-
from asyncio.tasks import sleep

import time
import threading
import xml.etree.ElementTree as ElementTree
import Settings
import Libs
from Web.Currency import Currency
from Web.PoeTradeMainHandler import PoeTradeMainHandler
from Web.PoeTradeResponseHandler import PoeTradeResponseHandler
from Web.PoeTradeWebHandler import PoeTradeWebHandler
from Proxy.Proxy import Proxy


# DEBUG
start_time = time.time()

# Proxy section #
proxy = Proxy()
use_proxy = Settings.use_proxies()
proxy_file_name = Settings.proxy_file_name()
check_proxies = Settings.check_proxies()
proxy_threads = Settings.proxy_threads()
proxy_timeout = Settings.proxy_timeout_msec()
overwrite_file_with_working_proxies = Settings.overwrite_file_with_working_proxies()

""" NO PROXY AT THIS MOMENT """
if use_proxy:
    # Get proxies to dictionary
    proxy_dict = {}
    checked_proxies_dict = {}
    proxy_file = open(proxy_file_name, 'r')
    for line in proxy_file:
        line = line.strip()
        proxy_dict[line] = 0
    proxy_file.close()

    # Check proxies
    if check_proxies:
        checked_proxies_dict = proxy.check_proxies(proxy_dict, proxy_threads, proxy_timeout)
        if len(checked_proxies_dict) == 0:
            print("\nNot a single working proxy. Exiting\n")
            exit(-1)
    # Overwrite with working proxies
    proxy_dict = checked_proxies_dict

    # Should program save working proxies to file?
    if overwrite_file_with_working_proxies:
        proxy_file = open(proxy_file_name, 'w')
        for proxy_key in proxy_dict:
            proxy_file.write(proxy_key + "\n")
        proxy_file.close()

""" NOT NEED FOR CURRENCY CHECK AT THIS MOMENT
### Currency section ###
currency = Currency()
currency_reset_delay = Settings.CURRENCY_RESET_DELAY_SEC
threading.Thread(
    target=currency.set_reset_currency_thread,
    args=(currency_reset_delay,)).start()
"""

# Poe.trade #
poe_trade_web_handler = PoeTradeWebHandler()
poe_trade_response_handler = PoeTradeResponseHandler()

# Main program section #
poe_trade_main_handler_classes_list = []
items_tree = ElementTree.parse(Settings.items_file_name())
item_xml_file_root = items_tree.getroot()

for item_xml in item_xml_file_root:
    full_post_data = poe_trade_web_handler.populate_full_post_data(item_xml)
    poe_trade_main_handler_classes_list.append(
        PoeTradeMainHandler(full_post_data, item_xml,
                            poe_trade_web_handler, poe_trade_response_handler))

print("Starting to parse")

working = True
iteration = 0
if not Settings.use_multithreading():
    # No multithreading
    print("No multithreading")
    while working:
        position = \
            Libs.get_poe_trade_main_lowest_timestamp(poe_trade_main_handler_classes_list)
        print("Iteration: {iteration}, class position: {position}".format(
            iteration=iteration, position=position))
        if position is not None:
            poe_trade_main_handler_classes_list[position].start_checking()
        iteration += 1
        time.sleep(Settings.main_thread_sleep_time())
else:
    # Using multithreading
    pass

# DEBUG
print("\nMain thread ends. Total time: {time:0.6f}".format(time=(time.time() - start_time)))

