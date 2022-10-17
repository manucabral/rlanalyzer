'''
    This module implements a Rocket League player.
    Only stores the player's useful information.
'''


class Player:
    '''Player class core.'''

    def __init__(self, **kwargs):
        '''Initialize the Player class.'''
        self.name = kwargs.get('PlayerName', 'Unknown')
        self.platform_id = kwargs.get('PlatformID', 'Unknown')
        self.login_status = kwargs.get('LoginStatus', 'Unknown')
        self.in_party = kwargs.get('IsInParty', 'Unknown') == 'True'
        self.platform = kwargs.get('Platform', 'Unknown')
        # TODO: Implement scraping for the player's stats.
        self.stats = {}
        self.rank = {}

    def __repr__(self):
        '''Returns the representation of the Player class.'''
        return f'<Player {self.platform_id}>'

    def __str__(self):
        '''Returns the string representation of the Player class.'''
        return self.__repr__()
