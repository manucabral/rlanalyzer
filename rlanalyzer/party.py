'''
    This module implements a Rocket League simple party.
    Only stores the party's useful information.
'''

from .player import Player
from .utils import Utils


class Party:
    '''Party class core.'''

    def __init__(self, party_data: list[dict], **kwargs):
        '''Initialize the Party class.'''

        self.data = reversed(party_data)
        self.size = self.__last_key('Members')
        self.party_id = self.__last_key('LobbyUID')
        self.party_leader = kwargs.get('party_leader', 'Unknown')

    def __repr__(self) -> str:
        '''Returns the representation of the Party class.'''
        return f'<Party {self.party_id}>'

    def __str__(self) -> str:
        '''Returns the string representation of the Party class.'''
        return self.__repr__()

    @property
    def leader(self) -> Player:
        '''Returns the party leader.'''
        return self.party_leader

    def __last_key(self, key: str) -> str:
        '''Returns the last value of a key.'''
        for entry in self.data:
            if not key in entry:
                continue
            return entry[key]

    def members(self) -> list[Player]:
        '''Returns the party members.'''
        members = []
        for entry in self.data:
            if not 'MemberID' in entry:
                continue
            if entry['LobbyUID'] != self.party_id:
                continue
            if len(entry['MemberID']) == 0:
                continue
            player = Player(**Utils.parse_playerid(entry['MemberID']))
            members.append(player)
        return members
