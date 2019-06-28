'''
    a count name rule

    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)
'''
from lkmltools.linter.rule import Rule

class CountNameRule(Rule):
    '''
        if this is a measure of type count, does name end with ``_count``
    '''

    def run(self, json_data):
        '''if this is a measure of type count, does name end with ``_count``

        Args:
            json_data (JSON): json_data of the lookml-parser dictionary for this count measure only

        Returns:
            (tuple): tuple containing:

                relevant (bool): is this rule relevant for this JSON chunk?

                passed (bool): did the rule pass?

        '''
        if json_data['_type'] == 'measure' and 'type' in json_data and json_data['type'] == 'count':
#            return True, json_data['_measure'].endswith("_count")
            return True, json_data['name'].endswith("_count")
        return False, None
