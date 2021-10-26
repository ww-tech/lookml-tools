from lkmltools.linter.field_rule import FieldRule

class GroupLabelRule(FieldRule):
    '''
        Does `dimension`, `dimension_group`, or `measure` have a description?
    '''

    def run(self, lookml_field):
        '''Run the rule: check whether `dimension`, `dimension_group`, or `measure` has a group_label

        Args:
            lookml_field (LookMLField): instance of LookMLField

        Returns:
            (tuple): tuple containing:

                relevant (bool): is this rule relevant for this JSON chunk?

                passed (bool): did the rule pass?

        '''
        if not (lookml_field.is_dimension() or lookml_field.is_dimension_group() or lookml_field.is_measure()):
            return False, None
        has_group_label = lookml_field.has_key('group_label') and lookml_field.group_label != ""
        return True, has_group_label
