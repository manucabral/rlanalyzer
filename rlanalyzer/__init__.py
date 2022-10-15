'''
RLAnalyzer - Rocket League Analyzer

This library extracts and analyses data from Rocket League's log files.
It can be used to get information about the current match, map, groups, etc.

Note: This library is not affiliated with Psyonix, Inc.
'''

__title__ = 'rlanalyzer'
__author__ = 'Manuel Cabral'
__version__ = '0.0.1'
__license__ = 'GPLv3'

from .__main__ import Analyzer

__all__ = ['Analyzer']
