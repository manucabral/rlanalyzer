'''This module contains all utility functions for RLAnalyzer.'''


class Utils:
    '''Utilities class core.'''
    LOG_PATH = '~/Documents/My Games/Rocket League/TAGame/Logs'
    PLATFORM = ['Epic Games', 'Steam']
    GAME_CLASS = {
        'TAGame.GameInfo_Soccar_TA': 'Soccar',
        'TAGame.GameInfo_Items_TA': 'Rumble',
        'TAGame.GameInfo_Basketball_TA': 'Hoops',
        'TAGame.GameInfo_Breakout_TA': 'Dropshot',
        'TAGame.GameInfo_Hockey_TA': 'Snowday',
    }

    @staticmethod
    def detect_platform(data: str) -> str:
        '''
        Detects the platform from a string.

        Params:
            data (str): String to detect the platform from.
        Returns:
            str: The detected platform. If the platform is not detected returns 'Unknown'.
        '''
        for platform in Utils.PLATFORM:
            if platform in data:
                return platform
        return 'Unknown'

    @staticmethod
    def detect_game(data: str) -> str:
        '''
        Detects the game class from a string.

        Params:
            data (str): String to detect the game class from.
        Returns:
            str: The detected game class. If the game class is not detected returns 'Menu'.
        '''
        data = data.split('?')
        for param in data:
            if 'game' in param:
                game = param.split('=')[1]
                return Utils.GAME_CLASS.get(game, 'Unknown')
        return 'Menu'
