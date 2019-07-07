'''
    a yesno name field rule

    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)
'''
from lkmltools.linter.field_rule import FieldRule
#from lkmltools.lookml_dimension import LookMLDimension

class YesNoNameRule(FieldRule):
    '''
        if this is a yesno dimension, does name start with ``is_``
    '''

    def run(self, lookml_field):
        '''if this is a yesno dimension, does name start with ``is_``

        Args:
            lookml_field (LookMLField): instance of LookMLField

        Returns:
            (tuple): tuple containing:

                relevant (bool): is this rule relevant for this field?

                passed (bool): did the rule pass?

        '''
        if lookml_field.is_dimension() and lookml_field.type == 'yesno':
            return True,lookml_field.name.startswith("is_")
        return False, None
