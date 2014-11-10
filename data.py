__author__ = 'San Lee'

from constants import *

#################################################################
#   Monster data
#################################################################

MONSTER_TYPE = 0
MONSTER_NAME = 1
MONSTER_IMG_FILE = 2
MONSTER_LEVEL = 3
MONSTER_HEALTH = 4
MONSTER_ATTACK = 5
MONSTER_DEFENCE = 6

monster_data = {
    # monster's data representation is
    # name: (type, name, image file, level, health, attack, defence)

    'bandit': (MONSTER_TYPE_MINION, 'Bandit', 'bandit.png', 1, 30, 4, 0),
    'boar': (MONSTER_TYPE_MINION, 'Boar', 'boar.png', 1, 40, 3, 0),
    'orc': (MONSTER_TYPE_MINION, 'Orc', 'orc.png', 2, 60, 6, 0),
    'skeleton': (MONSTER_TYPE_MINION, 'Skeleton', 'skeleton.png', 2, 40, 7, 1),
    'fallen knight': (MONSTER_TYPE_MINION, 'Fallen knight', 'fallen_knight.png', 2, 50, 6, 1),
    'ogre': (MONSTER_TYPE_MINION, 'Ogre', 'ogre.png', 3, 100, 6, 0),
    'demon scout': (MONSTER_TYPE_DEMON, 'Demon Scout', 'demon_scout.png', 3, 70, 8, 0),
    'gargoyle': (MONSTER_TYPE_MINION, 'Gargoyle', 'gargoyle.png', 3, 60, 6, 2),
    'demon bull': (MONSTER_TYPE_DEMON, 'Demon Bull', 'demon_bull.png', 4, 125, 7, 0),
    'phantom swordsman': (MONSTER_TYPE_MINION, 'Phantom Swordsman', 'phantom_swordsman.png', 4, 80, 10, 0),
    'demon vanguard': (MONSTER_TYPE_DEMON, 'Demon Vanguard', 'demon_vanguard.png', 4, 90, 8, 2),

    'evil mage': (MONSTER_TYPE_BOSS, 'Evil Mage', 'evil_mage.png', 2, 60, 9, 0),
    'demon king gaias': (MONSTER_TYPE_BOSS, 'Demon King Gaias', 'demon_king_gaias.png', 4, 120, 15, 1),
}

##################################################################
#   Weapon data
##################################################################

ITEM_NAME = 0
ITEM_FILENAME = 1
ITEM_POINT = 2
ITEM_PRICE = 3

weapon_data = {
    # weapon's data format is
    # name: (image_file, attack, price)

    'dagger': ('Dagger', 'dagger.png', 10, 40),
    'spear': ('Spear', 'spear.png', 14, 80),
    'long sword': ('Long Sword', 'long_sword.png', 18, 140),
    'shining morning star': ('Shining Morning Star', 'shining_morning_star.png', 23, 200),
}

##################################################################
#   Armor data
##################################################################

armor_data = {
    # armor's data format is
    # name: (image_file, defence, price)

    'quilt shirts': ('Quilt Shirts', 'quilt_shirts.png', 1, 50),
    'leather jacket': ('Leather Jacket', 'leather_jacket.png', 2, 120),
    'ring mail': ('Ring Mail', 'ring_mail.png', 3, 210),
    'plate armor': ('Plate Armor', 'plate_armor.png', 4, 300),
}

##################################################################
#   Tile data
##################################################################

TILE_TYPE = 0
TILE_GOLD_MULTIPLIER = 1
TILE_HEAL_AMOUNT = 1
TILE_MONSTER_DATA = 1
TILE_ITEM_TYPE = 0
TILE_ITEM_DATA = 1

tile_data = [
    (TILE_RESPAWN,),
    (TILE_GOLD, 10),
    (TILE_GOLD, 5),
    (TILE_WEAPON_SHOP, [weapon_data['dagger'], weapon_data['spear']], ),
    (TILE_GOLD, 5),
    (TILE_MONSTER, monster_data['bandit']),
    (TILE_MONSTER, monster_data['boar']),
    (TILE_GOLD, 10),
    (TILE_HEAL, 100),
    (TILE_RESPAWN,),
    (TILE_ARMOR_SHOP, [armor_data['quilt shirts'], armor_data['leather jacket']]),
    (TILE_GOLD, 5),
    (TILE_MONSTER, monster_data['bandit']),
    (TILE_HEAL, 100),
    (TILE_RESPAWN,),
    (TILE_GOLD, 10),
    (TILE_MONSTER, monster_data['boar']),
    (TILE_WEAPON_SHOP, [weapon_data['dagger'], weapon_data['spear'], weapon_data['long sword']]),
    (TILE_MONSTER, monster_data['orc']),
    (TILE_HEAL, 100),
    (TILE_MONSTER, monster_data['skeleton']),
    (TILE_ARMOR_SHOP, [armor_data['quilt shirts'], armor_data['leather jacket'], armor_data['ring mail']]),
    (TILE_GOLD, 10),
    (TILE_RESPAWN,),
    (TILE_MONSTER, monster_data['fallen knight']),
    (TILE_HEAL, 100),
    (TILE_MONSTER, monster_data['orc']),
    (TILE_MONSTER, monster_data['evil mage']),
]