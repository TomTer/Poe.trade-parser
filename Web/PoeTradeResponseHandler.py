# -*- coding: utf-8 -*-

import re

item_level_req_pattern = r'class="requirements">.{1,100}Level.*?;(\d+).*?<'
item_dex_req_pattern = r'requirements.{1,200}>.*?Dexteri.*?(\d+).*?<'
item_str_req_pattern = r'requirements.{1,200}>.*?Stren.*?(\d+).*?<'
item_int_req_pattern = r'requirements.{1,200}>.*?Intell.*?(\d+).*?<'
item_first_characteristics_pattern = r'cell-first">\s{1,20}<td.*?data-value="(.*?)"' \
                                     r'.*?data-value="(.*?)".*?data-value="(.*?)"' \
                                     r'.*?data-value="(.*?)".*?data-value="(.*?)"' \
                                     r'.*?data-value="(.*?)".*?data-value="(.*?)"'
item_seconds_characteristics_pattern = r'cell-second">\s{1,20}<td.*?data-value="(.*?)"' \
                                       r'.*?data-value="(.*?)".*?data-value="(.*?)"' \
                                       r'.*?data-value="(.*?)".*?data-value="(.*?)"' \
                                       r'.*?data-value="(.*?)"'
item_name_pattern = r'class="title itemframe.*?>(.*?)</a'
item_sockets_raw_pattern = r'class="sockets-raw">(.*?)</span'
item_bo_pattern = r'data-name="price_in_chaos".*?<.*?title="(.*?)"'
ign_pattern = r'IGN:\s.*?(\w*?)\s'

full_page_regex_pattern = r'(<tbody id="item-container.*?</tbody>)'


class PoeTradeResponseHandler:
    def item_container_parser(self, item_container_html):
        """
        Function takes a chunk html code from poe.trade (item_container)
        and parses it to get all item information
        :param item_container_html: html code from poe.trade (item_container)
        :return: dictionary with parsed information
                or None if players IGN is not found
        """

        item_information_dict = {}

        # Sockets
        sockets_raw_result = re.search(item_sockets_raw_pattern, item_container_html, re.I | re.S)
        if sockets_raw_result and sockets_raw_result.group(1):
            item_information_dict["Sockets_raw"] = sockets_raw_result.group(1)

        # Requirements
        req_string = ""
        item_level_req = re.search(item_level_req_pattern, item_container_html, re.I | re.S)
        item_str_req = re.search(item_str_req_pattern, item_container_html, re.I | re.S)
        item_dex_req = re.search(item_dex_req_pattern, item_container_html, re.I | re.S)
        item_int_req = re.search(item_int_req_pattern, item_container_html, re.I | re.S)
        if item_level_req and item_level_req.group(1):
            req_string += "Lvl: {lvl}, ".format(lvl=item_level_req.group(1))
        if item_str_req and item_str_req.group(1):
            req_string += "Str: {str}, ".format(str=item_str_req.group(1))
        if item_dex_req and item_dex_req.group(1):
            req_string += "Dex: {dex}, ".format(dex=item_dex_req.group(1))
        if item_int_req and item_int_req.group(1):
            req_string += "Int: {int}".format(int=item_int_req.group(1))

        item_information_dict["Req"] = req_string

        # Item first characteristics
        item_first_chars = re.search(item_first_characteristics_pattern, item_container_html, re.I | re.S)
        item_first_chars_list = item_first_chars.groups()
        quality = item_first_chars_list[0]
        psych_dmg = item_first_chars_list[1]
        elem_dmg = item_first_chars_list[2]
        aps = item_first_chars_list[3]
        dps = item_first_chars_list[4]
        pdps = item_first_chars_list[5]
        edps = item_first_chars_list[6]

        if quality != "0" and quality != "0.0":
            item_information_dict["quality"] = quality
        if psych_dmg != "0" and psych_dmg != "0.0":
            item_information_dict["psych_dmg"] = psych_dmg
        if elem_dmg != "0" and elem_dmg != "0.0":
            item_information_dict["elem_dmg"] = elem_dmg
        if aps != "0" and aps != "0.0":
            item_information_dict["aps"] = aps
        if dps != "0" and dps != "0.0":
            item_information_dict["dps"] = dps
        if pdps != "0" and pdps != "0.0":
            item_information_dict["pdps"] = pdps
        if edps != "0" and edps != "0.0":
            item_information_dict["edps"] = edps

        # Item second characteristics
        item_second_chars = re.search(item_seconds_characteristics_pattern, item_container_html, re.I | re.S)
        item_second_chars_list = item_second_chars.groups()
        armour = item_second_chars_list[0]
        evasion = item_second_chars_list[1]
        shield = item_second_chars_list[2]
        block = item_second_chars_list[3]
        crit = item_second_chars_list[4]
        level = item_second_chars_list[5]

        if armour != "0" and armour != "0.0":
            item_information_dict["armour"] = armour
        if evasion != "0" and evasion != "0.0":
            item_information_dict["evasion"] = evasion
        if shield != "0" and shield != "0.0":
            item_information_dict["shield"] = shield
        if block != "0" and block != "0.0":
            item_information_dict["block"] = block
        if crit != "0" and crit != "0.0":
            item_information_dict["crit"] = crit
        if level != "0" and level != "0.0":
            item_information_dict["level"] = level

        # Item name
        item_name = re.search(item_name_pattern, item_container_html, re.I | re.S)
        if item_name and item_name.group(1):
            item_name_full = str(item_name.group(1)).strip()
            if "corrupted</span>" in item_name_full:
                item_name_full = re.search("corrupted</span>(.*)",
                                           item_name_full, re.I).group(1)
                item_name_full = "Corrupted" + item_name_full
            item_information_dict["name"] = item_name_full

        # Buyout
        item_bo = re.search(item_bo_pattern, item_container_html, re.I | re.S)
        if item_bo and item_bo.group(1):
            item_information_dict["BO"] = str(item_bo.group(1)).strip()

        # IGN
        ign_results = ign_regex_results = re.search(ign_pattern, item_container_html, re.I | re.S)
        if ign_regex_results:
            item_information_dict["IGN"] = ign_results.group(1)
        else:
            return None

        return item_information_dict

    def get_all_item_containers(self, page_content):
        """
        Function checks for item_containers in html code.
        :param page_content: full html page from poe.trade
        :return: item_containers in list on None if none found
        """
        regex_results = re.findall(full_page_regex_pattern, page_content, re.I)

        if len(regex_results) == 0:
            return None
        else:
            return regex_results