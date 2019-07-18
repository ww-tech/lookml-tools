'''
    an all caps rule

    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)
'''
from lkmltools.linter.field_rule import FieldRule
from lkmltools.lookml_field import LookMLField

class AllCapsRule(FieldRule):
    '''is the name non all caps?
    '''

    def run(self, lookml_field):
        '''is the name non all caps?

        Args:
            lookml_field (LookMLField): instance of LookMLField

        Returns:
            (tuple): tuple containing:

                relevant (bool): is this rule relevant for this JSON chunk?

                passed (bool): did the rule pass?

        '''
        if not (lookml_field.is_dimension() or lookml_field.is_dimension_group() or lookml_field.is_measure()):
            return False, None
        return True, lookml_field.name != lookml_field.name.upper()
