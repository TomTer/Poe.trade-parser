# -*- coding: utf-8 -*-

import codecs
import os
import threading
import time
import Libs
import Settings
from Web.PoeTradeResponseHandler import PoeTradeResponseHandler
from Web.PoeTradeWebHandler import PoeTradeWebHandler


class PoeTradeMainHandler():
    poe_trade_web_handler = None
    poe_trade_response_handler = None
    item_xml = None
    full_post_data = None

    checked_timestamp = 0
    working = False

    def __init__(self, full_post_data, item_xml,
                 poe_trade_web_handler, poe_trade_response_handler):
        self.full_post_data = full_post_data
        self.item_xml = item_xml
        self.poe_trade_web_handler = poe_trade_web_handler
        self.poe_trade_response_handler = poe_trade_response_handler

    def from_item_xml_data(self):
        if self.item_xml:
            return Libs.get_data_from_xml(self.item_xml)
        else:
            return None

    def get_string_for_file_writing(self):
        """
        Function populates a proper string from xml tags to be written to a file
        :return: a properly populated string
        """
        string_for_file = ">>>> From XML <<<<\n"
        items_dict = self.from_item_xml_data()

        if items_dict:
            for item_tag in sorted(items_dict):
                string_for_file += "{tag}: {value}\n".format(tag=item_tag,
                                                             value=items_dict[item_tag])
            mods = self.item_xml.find("mods")
            if mods:
                for mod in mods:
                    modname = mod.find("modname")
                    if modname.text:
                        string_for_file += "mods: {modname}\n".format(modname=modname.text)

            return string_for_file

    def write_to_file_string(self, string_to_write):
        """
        Function writes a string to a file which name is defined in Settings.py
        :param string_to_write: string to write
        :return: returns nothing
        """
        filename = Settings.items_file_name_if_found()
        with threading.Lock():
            file_ = codecs.open("./" + filename, 'a', "utf-8")
            file_.write(str(string_to_write + "\n"))
            file_.close()

    def write_to_file_item(self, res):
        """
        Function makes proper string from information got from item xml tags
        and poe.trade information and writes it to a file
        :param res: item_container_html
        :return: returns nothing
        """
        parsed_item_container_dict = self.poe_trade_response_handler.item_container_parser(res)
        if parsed_item_container_dict:
            string_for_file_writing = self.get_string_for_file_writing()
            string_for_file_writing += ">>>> From Poe.trade <<<<\n"
            for item_container_tag in sorted(parsed_item_container_dict):
                value = parsed_item_container_dict[item_container_tag]
                string_for_file_writing += "{item_cont}: {value}\n".format(
                    item_cont=item_container_tag, value=value)

            # Check if file exists
            if os.path.isfile(Settings.items_file_name_if_found()):
                # Check if already exists in file
                already_exists = string_for_file_writing in open(Settings.items_file_name_if_found()).read()
                if not already_exists:
                    self.write_to_file_string(string_for_file_writing)
            # File not exists. Can write
            else:
                self.write_to_file_string(string_for_file_writing)

    def start_checking(self):
        """
        Class main working function. Checks for items and does some action when something is found
        :return: returns nothing
        """
        # Get page
        self.working = True
        page = self.poe_trade_web_handler.send_post_request_poe_trade(self.full_post_data)
        if page:
            result = self.poe_trade_response_handler.get_all_item_containers(str(page))
            if result:
                # Found something
                print("Found! Results: " + str(len(result)))
                for res in result:
                    # Action to-do when some item is found
                    self.write_to_file_item(res)

        self.checked_timestamp = time.time()
        self.working = False

