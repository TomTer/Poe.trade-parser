# -*- coding: utf-8 -*-

poe_trade_valid_tags_list = [
    "league",
    "type",
    "base",
    "name",
    "dmg_min",
    "dmg_max",
    "aps_min",
    "aps_max",
    "crit_min",
    "crit_max",
    "dps_min",
    "dps_max",
    "edps_min",
    "edps_max",
    "pdps_min",
    "pdps_max",
    "armour_min",
    "armour_max",
    "evasion_min",
    "evasion_max",
    "shield_min",
    "shield_max",
    "block_min",
    "block_max",
    "sockets_min",
    "sockets_max",
    "link_min",
    "link_max",
    "sockets_r",
    "sockets_g",
    "sockets_b",
    "sockets_w",
    "linked_r",
    "linked_g",
    "linked_b",
    "linked_w",
    "rlevel_min",
    "rlevel_max",
    "rstr_min",
    "rstr_max",
    "rdex_min",
    "rdex_max",
    "rint_min",
    "rint_max",
    "impl",
    "impl_min",
    "impl_max",
    "mods",
    "modexclude",
    "modmin",
    "modmax",
    "q_min",
    "q_max",
    "level_min",
    "level_max",
    "mapq_min",
    "mapq_max",
    "rarity",
    "seller",
    "thread",
    "time",
    "corrupted",
    "online",
    "buyout",
    "altart",
    "capquality",
    "buyout_min",
    "buyout_max",
    "buyout_currency",
    "crafted"
]

own_valid_tags_list = [  # TODO: Fill later
    ""
]


def check_valid_tag(xml_tag_name):
    """
    Function checks if xml tags are valid
    :param xml_tag_name: xml tag
    :return: True if valid
            False if invalid
    """
    return xml_tag_name in poe_trade_valid_tags_list \
           or xml_tag_name in own_valid_tags_list