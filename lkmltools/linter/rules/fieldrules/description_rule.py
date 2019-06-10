'''
    A description rule: does `dimension`, `dimension_group`, or `measure` have a description?

    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)
'''
from lkmltools.linter.rule import Rule

class DescriptionRule(Rule):
    '''
        Does `dimension`, `dimension_group`, or `measure` have a description?
    '''

    def run(self, json_data):
        '''Run the rule: check whether `dimension`, `dimension_group`, or `measure` has a description

        Args:
            json_data (JSON): json_data of the lookml-parser dictionary for this dimension, dimension_group, or measure only

        Returns:
            (tuple): tuple containing:

                relevant (bool): is this rule relevant for this JSON chunk?

                passed (bool): did the rule pass?

        '''
        if not '_type' in json_data or not json_data['_type'] in ['dimension', 'measure', 'dimension_group']:
            return False, None
        return True, 'description' in json_data and json_data['description'] != ''
