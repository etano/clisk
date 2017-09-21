class Player(object):
    """Player class

       Attributes:
           name (str): Player name
           territories (dict(str, int)): Dictionary of territories and troops
    """

    def __init__(self, name):
        """Initialize player

           Args:
               name (str): Player name
        """
        self.name = name
        self.territories = {}
