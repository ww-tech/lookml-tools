'''
    A description rule: does `dimension`, `dimension_group`, or `measure` have a description?

    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)
'''
from lkmltools.linter.field_rule import FieldRule

class DescriptionRule(FieldRule):
    '''
        Does `dimension`, `dimension_group`, or `measure` have a description?
    '''

    def run(self, lookml_field):
        '''Run the rule: check whether `dimension`, `dimension_group`, or `measure` has a description

        Args:
            lookml_field (LookMLField): instance of LookMLField

        Returns:
            (tuple): tuple containing:

                relevant (bool): is this rule relevant for this JSON chunk?

                passed (bool): did the rule pass?

        '''
        if not (lookml_field.is_dimension() or lookml_field.is_dimension_group() or lookml_field.is_measure()):
            return False, None
        has_description = lookml_field.has_key('description') and lookml_field.description != ""
        return True, has_description

