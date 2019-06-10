'''
    a drill down rule

    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)
'''
from lkmltools.linter.rule import Rule

class DrillDownRule(Rule):
    '''
        does this have drilldowns?
    '''

    def run(self, json_data):
        '''does this have drilldowns?

        Args:
            json_data (JSON): json_data of the lookml-parser dictionary for this measure only

        Returns:
            (tuple): tuple containing:

                relevant (bool): is this rule relevant for this JSON chunk?

                passed (bool): did the rule pass?

        '''
        # relevant for measures only
        if json_data['_type'] != 'measure':
            return False, None

        if not 'drill_fields' in json_data or json_data['drill_fields'] == []:
            return True, False
        return True, True
