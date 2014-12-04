# -*- coding: utf-8 -*-

import time
import Settings


def get_data_from_xml(item_xml):
    """
    Function return dictionary from item xml tags (without mods)
    :param item_xml: item xml tags
    :return: dictionary where key is a tag and value is value in tag (no mods)
    """
    item_data = {}
    for item_xml_node in item_xml:
        item_tag = item_xml_node.tag
        item_value = item_xml_node.text

        if item_tag != "mods":
            item_data[item_tag] = item_value

    return item_data


def get_poe_trade_main_lowest_timestamp(
        poe_trade_main_handler_classes_list):
    """
    Function gets lowest checked_timestamp in list
    :param poe_trade_main_handler_classes_list: list with instances of PoeTradeMainHandler
    :return: position in list which has lowest checked_timestamp or
            None if no one is ready to work (checked_timestamp is lower than THREAD_SLEEP_DELAY_BETWEEN_CHECKS_SEC)
    """
    position = None

    for index in range(0, len(poe_trade_main_handler_classes_list)):
        # Is class already working?
        if not poe_trade_main_handler_classes_list[index].working:
            if position is None:
                position = index
                continue
            # Class not working at this moment. Lets check timestamp
            current_class_timestamp = poe_trade_main_handler_classes_list[position].checked_timestamp
            index_class_timestamp = poe_trade_main_handler_classes_list[index].checked_timestamp

            if index_class_timestamp < current_class_timestamp:
                position = index

    if position is not None:
        class_timestamp = poe_trade_main_handler_classes_list[position].checked_timestamp
        timestamp_diff = time.time() - class_timestamp

        if timestamp_diff > Settings.thread_sleep_delay_between_checks_sec():
            return position

    return None


def get_free_thread(thread_list):
    for position in range(0, len(thread_list)):
        if thread_list[position] is None or not thread_list[position].isAlive():
            return position

    return None