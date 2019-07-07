'''
    a count name rule

    Authors:
        Carl Anderson (carl.anderson@weightwatchers.com)
'''
from lkmltools.linter.field_rule import FieldRule
from lkmltools.lookml_field import LookMLField

class CountNameRule(FieldRule):
    '''
        if this is a measure of type count, does name end with ``_count``
    '''

    def run(self, lookml_field):
        '''if this is a measure of type count, does name end with ``_count``

        Args:
            lookml_field (LookMLField): instance of LookMLField

        Returns:
            (tuple): tuple containing:

                relevant (bool): is this rule relevant for this JSON chunk?

                passed (bool): did the rule pass?

        '''
        if lookml_field.is_measure() and lookml_field.type == 'count':
            return True, lookml_field.name.endswith("_count")
        return False, None
