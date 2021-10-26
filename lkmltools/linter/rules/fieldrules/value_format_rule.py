'''
    a count name rule

    Authors:
        Carl Anderson (carl.anderson@weightwatchers.com)
'''
from lkmltools.linter.field_rule import FieldRule
from lkmltools.lookml_field import LookMLField

class ValueFormatRule(FieldRule):
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
        if lookml_field.is_measure() and lookml_field.has_key('value_format_name'):
            return True, lookml_field.value_format_name
        elif lookml_field.is_measure() and lookml_field.has_key('value_format'):
            return False, lookml_field.value_format
        else:
            return False, None
