'''
    This module contains all utilities used by the library.
    Note: This module is not intended to be used by the user.
'''


class Utils:
    '''Utils class core.'''

    LOG_PATH = '~/Documents/My Games/Rocket League/TAGame/Logs'
    LAST_LOG_FILE = 'Launch.log'
    PLATFORMS = r'Steam|Epic|PS4|XboxOne'

    # No include news game modes, only classic modes.
    GAME_CLASS = {
        'TAGame.GameInfo_Soccar_TA': 'Soccar',
        'TAGame.GameInfo_Items_TA': 'Rumble',
        'TAGame.GameInfo_Basketball_TA': 'Hoops',
        'TAGame.GameInfo_Breakout_TA': 'Dropshot',
        'TAGame.GameInfo_Hockey_TA': 'Snowday',
    }

    @staticmethod
    def last_line(lines: list[str], token: str = None) -> str:
        '''
        Get the last line that contains the token.

        Args:
            lines (list[str]): A list of lines.
            token (str): A token to search for.
        Returns:
            str: The last line that contains the token or None.
        '''
        if token is None:
            return lines[-1]
        for line in reversed(lines):
            if token in line:
                return line
        return None

    @staticmethod
    def find_lines(lines: list[str], token: str) -> list[str]:
        '''
        Find all lines that contains the token.

        Args:
            lines (list[str]): A list of lines.
            token (str): A token to search for.
        Returns:
            list[str]: A list of lines that contains the token.
        '''
        return [line for line in lines if token in line]

    @staticmethod
    def get_game_class(class_name: str) -> str:
        '''
        Get the game class name.

        Args:
            class_name (str): The game class name.
        Returns:
            str: The game name.
        '''
        return Utils.GAME_CLASS[class_name]

    @staticmethod
    def parse_playerid(player_id: str) -> dict:
        '''
        Parse the player ID.

        Args:
            player_id (str): The player ID.
        Returns:
            dict: A dictionary with the player ID.
        '''
        player_id = player_id.split('|')
        return {
            'Platform': player_id[0],
            'PlatformID': player_id[1],
        }
