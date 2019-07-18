'''a lexicon rule: check that field name or description does not mention certain words or phrases provided int the config

Authors:
        Carl Anderson (carl.anderson@weightwatchers.com)

'''
from lkmltools.linter.field_rule import FieldRule
from lkmltools.lookml_field import LookMLField

class LexiconRule(FieldRule):
    '''does dimension, dimension group, or measure follow some lexicon rules, 
       i.e. not mention certain words or phrases in name or description?
    '''

    def run(self, lookml_field):
        '''apply some lexion rules: check that the field name or description does not mention certain words or 
        phrases provided int the config

        Args:
            lookml_field (LookMLField): instance of LookMLField

        Returns:
            (tuple): tuple containing:

                relevant (bool): is this rule relevant for this JSON chunk?

                passed (bool): did the rule pass?

        '''
        if not (lookml_field.is_dimension() or lookml_field.is_dimension_group() or lookml_field.is_measure()):
            return False, None

        if not self.has_key("phrases"):
            raise Exception("Missing required key 'phrases'")

        phrases = self.config_for_key("phrases")
        if not isinstance(phrases, list):
            raise Exception("Error with phrases list. Should be a list")
        phrases = [str(s).lower() for s in phrases]

        passed = True
        for phrase in phrases:
            if phrase in lookml_field.name:
                passed = False
                break

            if  lookml_field.has_key('description') and lookml_field.description != "" and phrase in lookml_field.description:
                passed = False
                break

        return True, passed
