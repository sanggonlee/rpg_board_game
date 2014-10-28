__author__ = 'San Lee'

from constants import *

#################################################################
#   Monster data
#################################################################

MONSTER_TYPE = 0
MONSTER_LEVEL = 1
MONSTER_HEALTH = 2
MONSTER_ATTACK = 3
MONSTER_DEFENCE = 4

monster_data = {
    # monster's data representation is
    # name: (type, level, health, attack, defence)

    'bandit': (MONSTER_TYPE_MINION, 1, 30, 4, 0),
    'boar': (MONSTER_TYPE_MINION, 1, 40, 3, 0),
    'orc': (MONSTER_TYPE_MINION, 2, 60, 6, 0),
    'skeleton': (MONSTER_TYPE_MINION, 2, 40, 7, 1),
    'fallen knight': (MONSTER_TYPE_MINION, 2, 50, 6, 1),
    'ogre': (MONSTER_TYPE_MINION, 3, 100, 6, 0),
    'demon scout': (MONSTER_TYPE_DEMON, 3, 70, 8, 0),
    'gargoyle': (MONSTER_TYPE_MINION, 3, 60, 6, 2),
    'demon bull': (MONSTER_TYPE_DEMON, 4, 125, 7, 0),
    'phantom swordsman': (MONSTER_TYPE_MINION, 4, 80, 10, 0),
    'demon vanguard': (MONSTER_TYPE_DEMON, 4, 90, 8, 2),

    'evil mage': (MONSTER_TYPE_BOSS, 2, 60, 9, 0),
    'demon king gaias': (MONSTER_TYPE_BOSS, 4, 120, 15, 1),
}

##################################################################
#   Weapon data
##################################################################

WEAPON_FILENAME = 0
WEAPON_ATTACK = 1
WEAPON_PRICE = 2

weapon_data = {
    # weapon's data format is
    # name: (image_file, attack, price)

    'dagger': ('dagger.png', 10, 40),
    'spear': ('spear.png', 14, 80),
    'long sword': ('long_sword.png', 18, 140),
    'shining morning star': ('shining_morning_star.png', 23, 200),
}

##################################################################
#   Armor data
##################################################################

ARMOR_FILENAME = 0
ARMOR_ATTACK = 1
ARMOR_PRICE = 2

armor_data = {
    # armor's data format is
    # name: (image_file, defence, price)

    'quilt shirts': ('quilt_shirts.png', 1, 50),
    'leather jacket': ('leather_jacket.png', 2, 120),
    'ring mail': ('ring_mail.png', 3, 210),
    'plate armor': ('plate_armor.png', 4, 300),
}

##################################################################
#   Tile data
##################################################################

TILE_TYPE = 0
TILE_GOLD_MULTIPLIER = 1
TILE_HEAL_AMOUNT = 1
TILE_DATA = 1

tile_data = [
    (TILE_RESPAWN,),
    (TILE_GOLD, 10),
    (TILE_GOLD, 5),
    (TILE_SHOP, [weapon_data['dagger'], weapon_data['spear']]),
    (TILE_GOLD, 5),
    (TILE_MONSTER, monster_data['bandit']),
    (TILE_MONSTER, monster_data['boar']),
    (TILE_GOLD, 10),
    (TILE_HEAL, 100),
    (TILE_RESPAWN,),
    (TILE_SHOP, [armor_data['quilt shirts'], armor_data['leather jacket']]),
    (TILE_GOLD, 5),
    (TILE_MONSTER, monster_data['bandit']),
    (TILE_HEAL, 100),
    (TILE_RESPAWN,),
    (TILE_GOLD, 10),
    (TILE_MONSTER, monster_data['boar']),
    (TILE_SHOP, [weapon_data['dagger'], weapon_data['spear'], weapon_data['long sword']]),
    (TILE_MONSTER, monster_data['orc']),
    (TILE_HEAL, 100),
    (TILE_MONSTER, monster_data['skeleton']),
    (TILE_SHOP, [armor_data['quilt shirts'], armor_data['leather jacket'], armor_data['ring mail']]),
    (TILE_GOLD, 10),
    (TILE_RESPAWN,),
    (TILE_MONSTER, monster_data['fallen knight']),
    (TILE_HEAL, 100),
    (TILE_MONSTER, monster_data['orc']),
    (TILE_MONSTER, monster_data['evil mage']),
]