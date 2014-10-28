class Debugger:
    """
    Debugging level 1~3 for now
    3 logs more messages than 1
    """

    DEBUG_MODE = True
    _level = 2
    
    LEVEL1 = 1
    LEVEL2 = 2
    LEVEL3 = 3

    SKIP_GOLD_GET = False  # omit the gold_get event for debugging

    def __init__(self):
        pass

    @classmethod
    def log(cls, message, level):
        if cls.DEBUG_MODE and level <= cls._level:
            print "[DEBUG] {}".format(message)