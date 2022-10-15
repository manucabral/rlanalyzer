'''
    This module implements a Rocket League player.
    Only stores the player's useful information.
'''


class Player:
    '''Player class core.'''

    def __init__(self, id_: str, name: str, platform: str):
        '''Initialize the Player class.'''
        self.platform_id = id_
        self.name = name
        self.platform = platform
        # TODO: Implement scraping for the player's stats.
        self.stats = {}
        self.rank = {}

    def __repr__(self):
        '''Returns the representation of the Player class.'''
        return f'<Player {self.name}>'

    def __str__(self):
        '''Returns the string representation of the Player class.'''
        return self.__repr__()
