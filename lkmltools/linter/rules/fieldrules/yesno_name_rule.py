'''
    a yesno name rule

    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)
'''
from lkmltools.linter.rule import Rule

class YesNoNameRule(Rule):
    '''
        if this is a yesno dimension, does name start with ``is_``
    '''

    def run(self, json_data):
        '''if this is a yesno dimension, does name start with ``is_``

        Args:
            json_data (JSON): json_data of the lookml-parser dictionary for this dimension only

        Returns:
            (tuple): tuple containing:

                relevant (bool): is this rule relevant for this JSON chunk?

                passed (bool): did the rule pass?

        '''
        if json_data['_type'] == 'dimension' and 'type' in json_data and  json_data['type'] == 'yesno':
            return True, json_data['_dimension'].startswith("is_")
        return False, None
