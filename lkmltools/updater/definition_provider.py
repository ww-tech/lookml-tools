'''
    abstract base / interface for a class that provides definitions (descriptiopns)
    for dimensions, dimension_groups, and measures from some master source

    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)
'''
from abc import ABC, abstractmethod

class DefinitionProvider(ABC):
    '''
        a class that provides definitions for dimensions, dimension_groups, and measures
    '''

    def __init__(self, config):
        '''
        Args:
            config (JSON): the JSON configuration

        '''
        self.config = config

    @abstractmethod
    def get_definitions(self):
        '''get the definitions from the master source

        Returns:
            df (pandas dataframe): dataframe

        '''
        pass # pragma: no cover
