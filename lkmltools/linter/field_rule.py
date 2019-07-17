'''abstract base / interface for a field rule

Authors:
    Carl Anderson (carl.anderson@weightwatchers.com)

'''
from lkmltools.abstract_rule import AbstractRule
from abc import abstractmethod

class FieldRule(AbstractRule):
    '''concept of a rule that is applied to some view field: dimension, dimension_group, or measure
    '''

    def name(self):
        '''name of the the rule

        Returns:
            name of the the rule

        '''
        return self.__class__.__name__

    @abstractmethod
    def run(self, lookml_field):
        '''run the rule

        Args:
            lookml (LookMLField): LookMLField instance

        Returns:
            (tuple): tuple containing:

                relevant (bool): is this rule relevant for this JSON chunk?

                passed (bool): did the rule pass?

        '''
        pass # pragma: no cover
