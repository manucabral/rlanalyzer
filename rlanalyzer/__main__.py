'''
    This module contains the main class of the library.
    It is used to analyze simple Rocket League log files.
    TODO:
    Use a variable to store the log data and use it to get the information.
    Reading many times the same file is not efficient.
'''

import os
import re
import sys

from .utils import Utils
from .player import Player
from .party import Party

if sys.version_info < (3, 6):
    raise RuntimeError('Python 3.6 or higher is required.')

if sys.platform != 'win32':
    raise RuntimeError('Windows is required to run this library.')


class Analyzer:
    '''
    Analyzer class core.

    Attributes:
        log (str): A specific log file to be analyze.
    Raises:
        FileNotFoundError: If the log file does not exist.
    '''

    def __init__(self, **kwargs):
        self.__log = kwargs.get('log', Utils.LAST_LOG_FILE)
        self.__path = os.path.expanduser(Utils.LOG_PATH)
        if not self.__exists:
            raise FileNotFoundError(f'Log file "{self.__log}" not found.')

    def __str__(self) -> str:
        '''Return the string representation of the object.'''
        return f'Analyzer(current_log="{self.__log}")'

    def __repr__(self) -> str:
        '''Return the representation of the object.'''
        return self.__str__()

    @property
    def __exists(self) -> bool:
        '''
        Check if the log file exists.

        Returns:
            bool: True if the log file exists, False otherwise.
        '''
        return os.path.exists(os.path.join(self.__path, self.__log))

    @property
    def log(self) -> str:
        '''
        Get the log filename.

        Returns:
            str: The log filename.
        '''
        return self.__log

    @log.setter
    def log(self, value: str) -> None:
        '''
        Set the log filename.

        Args:
            value (str): The new log filename.
        Raises:
            FileNotFoundError: If the log file does not exist.
        '''
        self.__log = value
        if not self.__exists:
            raise FileNotFoundError(f'Log file "{self.__log}" not found.')

    @property
    def path(self) -> str:
        '''
        Get the full path of the log file.

        Returns:
            str: The log full path.
        '''
        return os.path.normpath(os.path.join(self.__path, self.__log))

    def __read(self) -> list[str]:
        '''
        Read the log file.

        Raises:
            RuntimeError: If the log file is empty or an error occurred.
        Returns:
            list[str]: A list of lines.
        '''
        try:
            with open(self.path, 'r', encoding='utf-8', errors='ignore') as file:
                return file.read().splitlines()
        except Exception as exc:
            raise RuntimeError(f'Unable to read the log file: {exc}') from exc

    def __load_map(self) -> str:
        '''
        Get the last map status loaded.

        Returns:
            str: The map name.
        '''
        lines = self.__read()
        map_ = Utils.last_line(lines, 'LoadMap')
        return map_

    @property
    def __player_status(self) -> dict:
        '''
        Get the last player status

        Returns:
            dict: The last player status.
        '''
        log = self.__read()
        line = Utils.last_line(log, 'HandleLocalPlayerLoginStatusChanged')
        status = dict(re.findall(r'(\w*)=(\".*?\"|\S*)', line))
        parsed_playerid = Utils.parse_playerid(status['PlayerID'])
        del status['PlayerID']
        return {**status, **parsed_playerid}

    @property
    def __lobby_member_status(self) -> list[dict]:
        '''
        Get all lobby members status.

        Returns:
            list[dict]: The lobby members status.
        '''
        log = self.__read()
        statuses = Utils.find_lines(log, 'HandleLobbyMemberStatusUpdate')
        parsed_statuses = re.findall(
            r'(\w*)=(\".*?\"|\S*)', '\n'.join(statuses))
        return [dict(parsed_statuses[i:i + 4]) for i in range(0, len(parsed_statuses), 4)]

    @property
    def in_party(self) -> bool:
        '''
        Check if the player is in a party.

        Returns:
            bool: True if the player is in a party, False otherwise.
        '''
        statuses = self.__lobby_member_status
        if not self.game_running:
            return False
        if len(statuses) == 0:
            # Maybe Rocket League is starting or not lobby is created.
            return False
        last_member_status = statuses[-1]
        print(last_member_status)
        index = last_member_status['MemberIndex']
        # if the member index is -1, the player is not in a party
        return index != '-1'

    @ property
    def party_leader(self) -> Player:
        '''
        Get the party player leader.
        Separate function because that info is not in HandleLobbyMemberStatusUpdate.

        Returns:
            str: The party leader name.
        '''
        if not self.game_running:
            return None
        lines = self.__read()
        if not self.in_party:
            return None
        line = Utils.last_line(lines, 'OnPartyLeaderChanged')
        if not line:
            # Maybe the player is the party leader
            return self.player
        leader = dict(re.findall(r'(\w*)=(\".*?\"|\S*)', line))
        parsed = Utils.parse_playerid(leader['NewLeader'])
        return Player(**parsed, IsInParty='True')

    @property
    def party(self) -> Party:
        '''
        Get the party where the player is in.

        Raises:
            RuntimeError: If the player is not in a party.
        Returns:
            Party: The party object.
        '''
        if not self.game_running:
            raise RuntimeError(
                "Can't get the party if the game is not running.")
        if not self.in_party:
            return None
        return Party(party_data=self.__lobby_member_status, party_leader=self.party_leader)

    @property
    def player(self) -> Player:
        '''
        Get the player object.

        Returns:
            Player: The player.
        '''
        return Player(**self.__player_status)

    @ property
    def game_running(self) -> bool:
        '''
        Check if Rocket League is running.

        Returns:
            bool: True if Rocket League is running, False otherwise.
        '''
        log = self.__read()
        last_line = Utils.last_line(log)
        return 'Log file closed' not in last_line

    @ property
    def platform(self) -> str:
        '''
        Get the platform used to play Rocket League.

        Returns:
            str: The platform used to play.
        '''
        log = self.__read()
        line = Utils.last_line(log, 'Base directory')
        return re.findall(Utils.PLATFORMS, line)[0]

    @ property
    def map(self) -> str:
        '''
        Get the last map loaded.

        Returns:
            str: The map name.
        '''
        last_map = self.__load_map()
        param = re.findall('LoadMap: ([^?]*)', last_map)[0]
        if '/' in param:
            return param.split('/')[-1]
        return param

    @ property
    def gameclass(self) -> str:
        '''
        Get the last game class loaded (e.g. 'Soccer', 'Hoops', etc.)

        Returns:
            str: The game class name.
        '''
        last_map = self.__load_map()
        if 'MENU' in last_map:
            return None
        game = re.findall(r'(Game|game)=([^?]*)', last_map)[0]
        return Utils.get_game_class(game[1])

    @ property
    def freeplay(self) -> bool:
        '''
        Check if the last map loaded is in Freeplay.

        Returns:
            bool: True if the last map loaded is in Freeplay, False otherwise.
        '''
        last_map = self.__load_map()
        return 'Freeplay' in last_map

    @ property
    def version(self) -> str:
        '''
        Get the Rocket League build version.

        Returns:
            str: The Rocket League version.
        '''
        log = self.__read()
        line = Utils.last_line(log, 'Version:')
        return re.findall('Version: (.*)', line)[0]
