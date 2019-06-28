'''
    an all caps rule

    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)
'''
from lkmltools.linter.rule import Rule

class AllCapsRule(Rule):
    '''is the name non all caps?
    '''

    def run(self, json_data):
        '''is the name non all caps?

        Args:
            json_data (JSON): json_data of the lookml-parser dictionary for this dimension, dimension group, or measure only

        Returns:
            (tuple): tuple containing:

                relevant (bool): is this rule relevant for this JSON chunk?

                passed (bool): did the rule pass?

        '''
        if not '_type' in json_data or not json_data['_type'] in ['dimension', 'dimension_group', 'measure']:
            return False, None
        name = json_data['name'] #['_' + json_data['_type']]
        return True, name != name.upper()
