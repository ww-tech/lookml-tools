'''
    A data source rule

    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)
'''
from lkmltools.linter.rule import Rule

class DataSourceRule(Rule):
    '''
        does source contain a sql_table_name or derived_table?
    '''

    def run(self, json_data):
        '''does source contain a sql_table_name or derived_table?

        Args:
            json_data (JSON): json_data of the whole lookml-parser ouput for a file

        Returns:
            (tuple): tuple containing:

                relevant (bool): is this rule relevant for this JSON chunk?

                passed (bool): did the rule pass?

        '''
        if not 'views' in json_data: #['files'][0]:
            return False, None
#        v = json_data['files'][0]['views'][0]
        v = json_data['views'][0]
        if 'sql_table_name' in v or 'derived_table' in v:
            return True, True
        return True, False
