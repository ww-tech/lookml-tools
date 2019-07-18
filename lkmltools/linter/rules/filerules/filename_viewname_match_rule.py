'''
    a filename viewname rule

    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)
'''
from lkmltools.linter.rule import Rule

class FilenameViewnameMatchRule(Rule):
    '''
        does filename match the view name?
    '''

    def run(self, lookml):
        '''does filename match the view name?

        Args:
            lookml (LookML): instance of LookML

        Returns:
            (tuple): tuple containing:

                relevant (bool): is this rule relevant for this JSON chunk?

                passed (bool): did the rule pass?

        '''
        if not lookml.has_views():
            return False, None
        return True, lookml.views()[0]['name'] == lookml.base_name
