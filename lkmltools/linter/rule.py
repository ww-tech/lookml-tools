'''
    abstract base / interface for a rule

    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)
'''
from abc import ABC, abstractmethod

class Rule(ABC):
    '''
        concept of a rule that is applied to some JSON version of LookML
    '''

    def name(self):
        '''name of the the rule

        Returns:
            name of the the rule

        '''
        return self.__class__.__name__

    @abstractmethod
    def run(self, json_data):
        '''run the rule

        Args:
            json_data (JSON): some JSON chunk from LookML

        Returns:
            (tuple): tuple containing:

                relevant (bool): is this rule relevant for this JSON chunk?

                passed (bool): did the rule pass?

        '''
        pass # pragma: no cover
