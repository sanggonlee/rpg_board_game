import inspect


SKIP_GOLD_GET = True
SKIP_HEAL = True
SKIP_RESPAWN = False
SKIP_MONSTER_FIGHT = False
SKIP_OLD_MONSTER_FIGHT = True
SKIP_SHOP = False
SKIP_DICE_GRAPHICS = True


class Debugger:
    """
    Debugging level 1~3 for now
    3 logs more messages than 1
    """

    DEBUG_MODE = True
    _level = 2

    def __init__(self):
        pass

    @classmethod
    def log(cls, message, level=3):
        if cls.DEBUG_MODE and level <= cls._level:
            print "[DEBUG][{}.{}] {}".format(
                inspect.getmodulename(inspect.stack()[1][1]),
                inspect.stack()[1][3], message
            )