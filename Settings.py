# -*- coding: utf-8 -*-
import configparser

# I love when program reacts to settings changes in real time
def get_config():
    config = configparser.ConfigParser()
    config.read("settings.ini")

    return config

# CURRENCY
def get_reset_currency_working():
    return get_config()["CURRENCY"]["RESET_CURRENCY_WORKING"]
def currency_reset_delay_sec():
    return get_config().getint("CURRENCY", "CURRENCY_RESET_DELAY_SEC")

# ITEMS
def items_file_name():
    return get_config()["ITEMS"]["ITEMS_FILE_NAME"]
def items_file_name_if_found():
    return get_config()["ITEMS"]["ITEMS_FILE_NAME_IF_FOUND"]
def use_multithreading():
    return get_config().getboolean("ITEMS", "USE_MULTITHREADING")
def items_check_threads():
    return get_config().getint("ITEMS", "ITEMS_CHECK_THREADS")
def thread_sleep_delay_between_checks_sec():
    return get_config().getint("ITEMS", "THREAD_SLEEP_DELAY_BETWEEN_CHECKS_SEC")
def main_thread_sleep_time():
    return get_config().getint("ITEMS", "MAIN_THREAD_SLEEP_TIME")

# PROXY
def use_proxies():
    return get_config().getboolean("PROXY", "USE_PROXIES")
def proxy_file_name():
    return get_config()["PROXY"]["PROXY_FILE_NAME"]
def check_proxies():
    return get_config().getboolean("PROXY", "CHECK_PROXIES")
def proxy_threads():
    return get_config().getint("PROXY", "PROXY_THREADS")
def proxy_timeout_msec():
    return get_config().getint("PROXY", "PROXY_TIMEOUT_MSEC")
def overwrite_file_with_working_proxies():
    return get_config().getboolean("PROXY", "OVERWRITE_FILE_WITH_WORKING_PROXIES")
