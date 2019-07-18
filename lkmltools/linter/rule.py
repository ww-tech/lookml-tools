'''
    abstract base / interface for a rule

    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)
'''
from lkmltools.abstract_rule import AbstractRule
from abc import abstractmethod

class Rule(AbstractRule):
    '''
        concept of a rule that is applied to some LookML
    '''

    def name(self):
        '''name of the the rule

        Returns:
            name of the the rule

        '''
        return self.__class__.__name__

    @abstractmethod
    def run(self, lookml):
        '''run the rule

        Args:
            lookml (LookML): LookML instance

        Returns:
            (tuple): tuple containing:

                relevant (bool): is this rule relevant for this JSON chunk?

                passed (bool): did the rule pass?

        '''
        pass # pragma: no cover
