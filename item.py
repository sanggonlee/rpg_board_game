class Item:
    """
    Abstract class for CombatItem and SpecialItem
    Member variables:
    (str) name  - name of the item
    (int) price - price of the item
    """
    def __init__(self, item_name, item_price):
        name = item_name
        price = item_price
        

class CombatItem(Item):
    """
    Concrete class for combat item
    Member variables:
    (str) kind - offence item ('off') or defence item ('def')
    (int) point - attack or defence point
    """