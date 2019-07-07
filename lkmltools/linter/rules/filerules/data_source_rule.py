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

    def run(self, lookml):
        '''does source contain a sql_table_name or derived_table?

        Args:
            lookml (LookML): instance of LookML

        Returns:
            (tuple): tuple containing:

                relevant (bool): is this rule relevant for this JSON chunk?

                passed (bool): did the rule pass?

        '''
        if not lookml.has_views():
            return False, None
        v = lookml.views()[0]
        if 'sql_table_name' in v or 'derived_table' in v:
            return True, True
        return True, False
