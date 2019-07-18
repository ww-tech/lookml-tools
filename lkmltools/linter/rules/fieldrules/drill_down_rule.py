'''
    a drill down rule

    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)
'''
from lkmltools.linter.field_rule import FieldRule
from lkmltools.lookml_field import LookMLField

class DrillDownRule(FieldRule):
    '''
        does this have drilldowns?
    '''

    def run(self, lookml_field):
        '''does this have drilldowns?

        Args:
            lookml_field (LookMLField): instance of LookMLField

        Returns:
            (tuple): tuple containing:

                relevant (bool): is this rule relevant for this JSON chunk?

                passed (bool): did the rule pass?

        '''
        if not lookml_field.is_measure():
            return False, None

        if not lookml_field.has_key('drill_fields') or lookml_field.drill_fields == []:
            return True, False
        return True, True
