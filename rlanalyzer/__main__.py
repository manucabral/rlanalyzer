'''
    Main module of RLAnalyzer
    This module contains the main class of the library.
'''

import os
import sys

from .utils import Utils
from .player import Player

if sys.platform != 'win32':
    raise NotImplementedError('Only Windows is supported')


class Analyzer:
    '''
    Analyzer class core.
    This class contains all the methods to analyze the log files.

    Attributes:
        log (str): A log file name, if not specified it will get the last log file.
    '''

    def __init__(self, **kwargs):
        '''Initialize the Analyzer class.'''
        self.__path = os.path.expanduser(Utils.LOG_PATH)
        self.__log = kwargs.get('log', 'Launch.log')
        if not os.path.exists(self.__path):
            raise FileNotFoundError("Can't find Rocket League's log files.")

    @property
    def __get_log(self) -> list[str]:
        '''
        Gets a log file.

        Params:
            log_name (str): Log file name.
        Returns:
            list[str]: Log file lines.
        '''
        path = os.path.join(self.__path, self.__log)
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as log:
                return log.read().splitlines()
        except FileNotFoundError as exc:
            raise FileNotFoundError(f"Can't find {self.__log}") from exc

    @property
    def running(self) -> bool:
        '''
        Checks if Rocket League is running.

        Returns:
            bool: True if Rocket League is running, False otherwise.
        '''
        lines = self.__get_log
        if len(lines) == 0:
            return False
        return 'Log file closed' not in lines[-1]

    @property
    def platform(self) -> str:
        '''
        Gets the current platform.

        Returns:
            str: Platform.
        '''
        lines = self.__get_log
        base_directory = [
            line for line in lines if 'Base directory' in line][0]
        if not base_directory:
            raise ValueError('Corrupted log file.')
        return Utils.detect_platform(base_directory)

    @property
    def __get_map(self) -> str:
        '''
        Gets last map with game tags.

        Raises:
            ValueError: If the log file is corrupted.
        Returns:
            str: Map name and game tags.
        '''
        lines = self.__get_log
        map_ = [line for line in lines if 'LoadMap' in line][-1]
        if not map_:
            raise ValueError('Corrupted log file.')
        return map_

    @property
    def game(self) -> str:
        '''
        Gets the current game class.

        Raises:
            ValueError: If the log file is corrupted.
        Returns:
            str: The current game class.
        '''
        mapinfo = self.__get_map
        game = Utils.detect_game(mapinfo)
        return game

    @property
    def map(self) -> str:
        '''
        Gets the current map.

        Returns:
            str: The current map or None if the player is in the menu.
        '''
        lines = self.__get_log
        map_ = [line
                for line in lines if 'LoadMap' in line][-1]
        map_name = map_.split(' ')[3].split('?')[0]
        if '/' in map_name:
            # In online games
            return map_name.split('/')[-1]
        if 'MENU' in map_name:
            return None
        return map_name

    @property
    def freeplay(self) -> bool:
        '''
        Checks if the player is in freeplay.

        Returns:
            bool: True if the player is in freeplay, False otherwise.
        '''
        mapinfo = self.__get_map
        return 'Freeplay' in mapinfo

    @property
    def player(self) -> Player:
        '''
        Gets the current player.

        Returns:
            Player: The current player.
        '''
        lines = self.__get_log
        status = [
            line.split(' ')
            for line in lines if 'HandleLocalPlayerLoginStatusChanged' in line][-1]
        if not status:
            raise ValueError('Corrupted log file.')
        name = status[3].split('=')[1]
        platform_id = status[4].split('=')[1].split('|')[1]
        return Player(platform_id, name, self.platform)
