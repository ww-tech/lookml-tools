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

    def run(self, json_data):
        '''is there one view only in this file?

        Args:
            json_data (JSON): json_data of the whole lookml-parser ouput for a file

        Returns:
            (tuple): tuple containing:

                relevant (bool): is this rule relevant for this JSON chunk?

                passed (bool): did the rule pass?

        '''
        if not 'views' in json_data:
            return False, None
        n = len(json_data['views'])
        if n > 1:
            return True, False
        return True, True
