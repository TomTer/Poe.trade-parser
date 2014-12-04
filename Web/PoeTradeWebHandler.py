# -*- coding: utf-8 -*-

import urllib.parse
import requests
from datetime import datetime, timedelta
import xml.etree.ElementTree as ElementTree
import Web.PoeTradeValidPostValues as PoeTradeValidPostValues
import Settings
import Libs


poe_trade_post_data_send_url = r"http://poe.trade/search"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded'
}


class PoeTradeWebHandler():

    def send_post_request_poe_trade(self, complete_post_data):
        """
        Function sends POST requests and returns its content or None if status_code isnt 200
        :param complete_post_data: full POST data
        :return: None is status_code isn't 200 or
                full html page
        """
        page = requests.post(poe_trade_post_data_send_url, data=complete_post_data, headers=headers)
        if page.status_code is 200:
            return page.content
        else:
            print("Status code in 'send_post_request_poe_trade' isn't 200")
            return None

    def get_data_from_xml(self, item_xml):
        """
        Function gets a dictionary from xml tags and checks if they are valid
        :param item_xml: item xml file
        :return: dictionary where key is tag and value is information in tag
        """
        item_dict = Libs.get_data_from_xml(item_xml)

        for item_tag in item_dict:
            if not PoeTradeValidPostValues.check_valid_tag(item_tag):
                print("Invalid item xml tag. Exiting")
                exit(1)

        return item_dict

    def populate_post_data(self, item_data_dict, item_xml):
        """
        Function populates full POST data for poe.trade without mods
        :param item_data_dict: parsed item xml as dictionary
        :return: POST data without mods as a string
        """
        poe_post_data = "league={league}&type={type}&base={base}&name={name}&dmg_min={dmg_min}" \
                        "&dmg_max={dmg_max}&aps_min={aps_min}&aps_max={aps_max}&crit_min={crit_min}" \
                        "&crit_max={crit_max}&dps_min={dps_min}&dps_max={dps_max}&edps_min={edps_min}" \
                        "&edps_max={edps_max}&pdps_min={pdps_min}&pdps_max={pdps_max}" \
                        "&armour_min={armour_min}&armour_max={armour_max}&evasion_min={evasion_min}" \
                        "&evasion_max={evasion_max}&shield_min={shield_min}&shield_max={shield_max}" \
                        "&block_min={block_min}&block_max={block_max}&sockets_min={sockets_min}" \
                        "&sockets_max={sockets_max}&link_min={link_min}&link_max={link_max}" \
                        "&sockets_r={sockets_r}&sockets_g={sockets_g}&sockets_b={sockets_b}" \
                        "&sockets_w={sockets_w}&linked_r={linked_r}&linked_g={linked_g}&linked_b={linked_b}" \
                        "&linked_w={linked_w}&rlevel_min={rlevel_min}&rlevel_max={rlevel_max}&rstr_min={rstr_min}" \
                        "&rstr_max={rstr_max}&rdex_min={rdex_min}&rdex_max={rdex_max}&rint_min={rint_min}" \
                        "&rint_max={rint_max}&impl={impl}&impl_min={impl_min}&impl_max={impl_max}" \
                        "&mods=&modexclude=&modmin=&modmax={other_mods}&q_min={q_min}&q_max={q_max}&level_min={level_min}" \
                        "&level_max={level_max}&mapq_min={mapq_min}&mapq_max={mapq_max}&rarity={rarity}&seller={seller}" \
                        "&thread={thread}&time={time}&corrupted={corrupted}&online={online}&buyout={buyout}" \
                        "&altart={altart}&capquality={capquality}&buyout_min={buyout_min}&buyout_max={buyout_max}" \
                        "&buyout_currency={buyout_currency}&crafted={crafted}" \
            .format(
                league=item_data_dict["league"] if ("league" in item_data_dict) else "",
                type=item_data_dict["type"] if ("type" in item_data_dict) else "",  # TODO: CHECK THIS
                base=item_data_dict["base"] if ("base" in item_data_dict) else "",
                name=urllib.parse.quote_plus(item_data_dict["name"]) if ("name" in item_data_dict) else "",
                dmg_min=item_data_dict["dmg_min"] if ("dmg_min" in item_data_dict) else "",
                dmg_max=item_data_dict["dmg_max"] if ("dmg_max" in item_data_dict) else "",
                aps_min=item_data_dict["aps_min"] if ("aps_min" in item_data_dict) else "",
                aps_max=item_data_dict["aps_max"] if ("aps_max" in item_data_dict) else "",
                crit_min=item_data_dict["crit_min"] if ("crit_min" in item_data_dict) else "",
                crit_max=item_data_dict["crit_max"] if ("crit_max" in item_data_dict) else "",
                dps_min=item_data_dict["dps_min"] if ("dps_min" in item_data_dict) else "",
                dps_max=item_data_dict["dps_max"] if ("dps_max" in item_data_dict) else "",
                edps_min=item_data_dict["edps_min"] if ("edps_min" in item_data_dict) else "",
                edps_max=item_data_dict["edps_max"] if ("edps_max" in item_data_dict) else "",
                pdps_min=item_data_dict["pdps_min"] if ("pdps_min" in item_data_dict) else "",
                pdps_max=item_data_dict["pdps_max"] if ("pdps_max" in item_data_dict) else "",
                armour_min=item_data_dict["armour_min"] if ("armour_min" in item_data_dict) else "",
                armour_max=item_data_dict["armour_max"] if ("armour_max" in item_data_dict) else "",
                evasion_min=item_data_dict["evasion_min"] if ("evasion_min" in item_data_dict) else "",
                evasion_max=item_data_dict["evasion_max"] if ("evasion_max" in item_data_dict) else "",
                shield_min=item_data_dict["shield_min"] if ("shield_min" in item_data_dict) else "",
                shield_max=item_data_dict["shield_max"] if ("shield_max" in item_data_dict) else "",
                block_min=item_data_dict["block_min"] if ("block_min" in item_data_dict) else "",
                block_max=item_data_dict["block_max"] if ("block_max" in item_data_dict) else "",
                sockets_min=item_data_dict["sockets_min"] if ("sockets_min" in item_data_dict) else "",
                sockets_max=item_data_dict["sockets_max"] if ("sockets_max" in item_data_dict) else "",
                link_min=item_data_dict["link_min"] if ("link_min" in item_data_dict) else "",
                link_max=item_data_dict["link_max"] if ("link_max" in item_data_dict) else "",
                sockets_r=item_data_dict["sockets_r"] if ("sockets_r" in item_data_dict) else "",
                sockets_g=item_data_dict["sockets_g"] if ("sockets_g" in item_data_dict) else "",
                sockets_b=item_data_dict["sockets_b"] if ("sockets_b" in item_data_dict) else "",
                sockets_w=item_data_dict["sockets_w"] if ("sockets_w" in item_data_dict) else "",
                linked_r=item_data_dict["linked_r"] if ("linked_r" in item_data_dict) else "",
                linked_g=item_data_dict["linked_g"] if ("linked_g" in item_data_dict) else "",
                linked_b=item_data_dict["linked_b"] if ("linked_b" in item_data_dict) else "",
                linked_w=item_data_dict["linked_w"] if ("linked_w" in item_data_dict) else "",
                rlevel_min=item_data_dict["rlevel_min"] if ("rlevel_min" in item_data_dict) else "",
                rlevel_max=item_data_dict["rlevel_max"] if ("rlevel_max" in item_data_dict) else "",
                rstr_min=item_data_dict["rstr_min"] if ("rstr_min" in item_data_dict) else "",
                rstr_max=item_data_dict["rstr_max"] if ("rstr_max" in item_data_dict) else "",
                rdex_min=item_data_dict["rdex_min"] if ("rdex_min" in item_data_dict) else "",
                rdex_max=item_data_dict["rdex_max"] if ("rdex_max" in item_data_dict) else "",
                rint_min=item_data_dict["rint_min"] if ("rint_min" in item_data_dict) else "",
                rint_max=item_data_dict["rint_max"] if ("rint_max" in item_data_dict) else "",
                impl=item_data_dict["impl"] if ("impl" in item_data_dict) else "",
                impl_min=item_data_dict["impl_min"] if ("impl_min" in item_data_dict) else "",
                impl_max=item_data_dict["impl_max"] if ("impl_max" in item_data_dict) else "",
                q_min=item_data_dict["q_min"] if ("q_min" in item_data_dict) else "",
                q_max=item_data_dict["q_max"] if ("q_max" in item_data_dict) else "",
                level_min=item_data_dict["level_min"] if ("level_min" in item_data_dict) else "",
                level_max=item_data_dict["level_max"] if ("level_max" in item_data_dict) else "",
                mapq_min=item_data_dict["mapq_min"] if ("mapq_min" in item_data_dict) else "",
                mapq_max=item_data_dict["mapq_max"] if ("mapq_max" in item_data_dict) else "",
                rarity=item_data_dict["rarity"] if ("rarity" in item_data_dict) else "",
                seller=item_data_dict["seller"] if ("seller" in item_data_dict) else "",
                thread=item_data_dict["thread"] if ("thread" in item_data_dict) else "",
                time=item_data_dict["time"] if ("time" in item_data_dict)
                                            else (datetime.now()-timedelta(7)).strftime("%Y-%m-%d"),
                corrupted=item_data_dict["corrupted"] if ("corrupted" in item_data_dict) else "",
                online=item_data_dict["online"] if ("online" in item_data_dict) else "",
                buyout=item_data_dict["buyout"] if ("buyout" in item_data_dict) else "",
                altart=item_data_dict["altart"] if ("altart" in item_data_dict) else "",
                capquality=item_data_dict["capquality"] if ("capquality" in item_data_dict) else "",
                buyout_min=item_data_dict["buyout_min"] if ("buyout_min" in item_data_dict) else "",
                buyout_max=item_data_dict["buyout_max"] if ("buyout_max" in item_data_dict) else "",
                buyout_currency=item_data_dict["buyout_currency"] if ("buyout_currency" in item_data_dict) else "",
                crafted=item_data_dict["crafted"] if ("crafted" in item_data_dict) else "",
                other_mods=self.populate_post_data_mods(item_xml),
            )

        return poe_post_data

    def populate_post_data_mods(self, item_xml):
        """
        Function only adds mods to string and returns the string
        :param item_xml: item xml tags
        :return: proper mods string for post data
        """
        mods_post_string = ""
        mods = item_xml.find("mods")
        if mods:
            for mod in mods:
                modname = mod.find("modname")
                modexclude = mod.find("modexclude")
                modmin = mod.find("modmin")
                modmax = mod.find("modmax")

                mods_post_string += "&mods={modname}&modexclude={modexclude}&modmin={modmin}&modmax={modmax}"\
                    .format(
                        modname=urllib.parse.quote_plus(modname.text) if (modname is not None) else "",
                        modexclude=modexclude.text if (modexclude is not None) else "",
                        modmin=modmin.text if (modmin is not None) else "",
                        modmax=modmax.text if (modmax is not None) else "",
                    )

        return mods_post_string

    def populate_full_post_data(self, item_xml):
        """
        Function populates full POST data from item xml tags
        :param item_xml: item xml
        :return: full ready to use POST data for poe.trade as a string
        """
        item_data_dict = self.get_data_from_xml(item_xml)
        return self.populate_post_data(item_data_dict, item_xml)
