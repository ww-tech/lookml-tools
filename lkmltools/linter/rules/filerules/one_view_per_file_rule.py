'''
    a one view per file rule

    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)
'''
from lkmltools.linter.rule import Rule

class OneViewPerFileRule(Rule):
    '''
        is there one view only in this file?
    '''

    def run(self, lookml):
        '''is there one view only in this LookML file?

        Args:
            lookml (LookML): instance of LookML

        Returns:
            (tuple): tuple containing:

                relevant (bool): is this rule relevant for this JSON chunk?

                passed (bool): did the rule pass?

        '''
        if not lookml.has_views():
            return False, None
        if len(lookml.views()) > 1:
            return True, False
        return True, True
