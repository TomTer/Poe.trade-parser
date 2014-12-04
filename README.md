Hello!

Idea of this program came to my mind when i bought Spell Echo under a chaos. So I created this automatic parser for [Poe.trade][1].

It will parse [Poe.trade][1] for items in items.xml (configurable) and wait a delay (configrable). If the item is found it will write all items information to found_items.txt (configrable)

#Usage

Configure **settings.ini**, make your item list in **items.xml** file and:

```
python Main.py
```

or

Start **Main.exe** in **dist** folder

#XML

Xml file has a structure


    <?xml version="1.0"?>

    <items>

        <item>
            ITEM1
        </item>

        <item>
            ITEM2
        </item>

        <item>
            ITEM3
        </item>

        etc...

    </items>
    

Every *item* tag takes some information to check.

**Only mandatory tag is *league*. You don't need to write empty tags!**

Next tags are valid:

    <league></league> (Standard, Hardcore or any other)
    <type>
        empty = any
        1h = Gen. 1h
        2h = Gen. 2h
        Bow = bows
        Claw = claws
        Dagger = daggers
        One Hand Axe = 1h axe
        One Hand Mace = 1h mace
        One Hand Sword = 1h sword
        Sceprte = sceptres
        Staff = staffs
        Two Hand Axe = 2h axes
        Two Hand Mace = 2h maces
        Two Hand Sword = 2h sword
        Wand = wands
        Body Armour = body armours
        Boots = boots
        Gloves = gloves
        Helmet = helmet
        Shield = shield
        Amulet = amulet
        Belt = belt
        Currency = currency
        Fishing Rods = fishing rods
        Flask = flasks
        Gem = gems
        Map = map
        Quiver = quivers
        Ring = rings
        Vaal Fragments = vaal fragments
    </type>
    <base></base> (name)
    <name></name> (ex. Cast on Critical Strike)
    <dmg_min></dmg_min>
    <dmg_max></dmg_max>
    <aps_min></aps_min>
    <aps_max></aps_max>
    <crit_min></crit_min>
    <crit_max></crit_max>
    <dps_min></dps_min>
    <dps_max></dps_max>
    <edps_min></edps_min>
    <edps_max></edps_max>
    <pdps_min></pdps_min>
    <pdps_max></pdps_max>
    <armour_min></armour_min>
    <armour_max></armour_max>
    <evasion_min></evasion_min>
    <evasion_max></evasion_max>
    <shield_min></shield_min>
    <shield_max></shield_max>
    <block_min></block_min>
    <block_max></block_max>
    <sockets_min></sockets_min>
    <sockets_max></sockets_max>
    <link_min></link_min>
    <link_max></link_max>
    <sockets_r></sockets_r>
    <sockets_g></sockets_g>
    <sockets_b></sockets_b>
    <sockets_w></sockets_w>
    <linked_r></linked_r>
    <linked_g></linked_g>
    <linked_b></linked_b>
    <linked_w></linked_w>
    <rlevel_min></rlevel_min> (req minimum level)
    <rlevel_max></rlevel_max> (req maximum level)
    <rstr_min></rstr_min> (req minimum strength)
    <rstr_max></rstr_max> (req maximum strength)
    <rdex_min></rdex_min> (req minimum dexterity)
    <rdex_max></rdex_max> (req maximum dexterity)
    <rint_min></rint_min> (req minimum intelligence)
    <rint_max></rint_max> (req maximum intelligence)
    <impl></impl> (Implicit mod)
    <impl_min></impl_min>
    <impl_max></impl_max>
    <q_min></q_min>
    <q_max></q_max>
    <level_min></level_min>
    <level_max></level_max>
    <mapq_min></mapq_min>
    <mapq_max></mapq_max>
    <rarity></rarity>
    <seller></seller>
    <thread></thread>
    <time></time> (Last time seen. Empty for week ago or date in YYYY-MM-DD format)
    <corrupted></corrupted>
    <online></online> (empty or x)
    <altart></altart>
    <capquality></capquality>
    <buyout></buyout> (empty or x)
    <buyout_min></buyout_min>
    <buyout_max></buyout_max>
    <buyout_currency></buyout_currency> (chaos, blessed, chisel, chromatic, 
                                        divine, exalted, gcp, jewellers, alchemy, alteration, 
                                        chance, fusing, regret, scouring, regal)
    <crafted></crafted>


Mods go to their own tags
Example:

    <mods>

        <mod>
            <modname>NAME1</modname>
            <modexclude>x</modexclude>
        </mod>

        <mod>
            <modname>NAME2</modname>
            <modmin>10</modmin>
            <modmax>20</modmax>
        </mod>

        <mod>
            <modname>NAME3</modname>
        </mod>

    </mods>


Following is an example of valid xml:

    <?xml version="1.0"?>

    <items>

        <item>
            <league>Standard</league>
            <name>Cast on Critical Strike</name>
        </item>

        <item>
            <league>Standard</league>
            <name>Multistrike</name>
            <q_min>10</q_min>
            <q_max>16</q_max>
            <buyout>x</buyout>
        </item>

        <item>
            <league>Standard</league>
            <link_min>6</link_min>
            <mods>
                <mod>
                    <modname>+1 maximum Power Charge</modname>
                </mod>
                <mod>
                    <modname>#% increased Critical Strike Chance</modname>
                    <modmin>30</modmin>
                </mod>
            </mods>
        </item>

    </items>



[1]: http://poe.trade/
