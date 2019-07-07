'''
    a lexicon rule

    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)
'''
from lkmltools.linter.field_rule import FieldRule
from lkmltools.lookml_field import LookMLField

class LexiconRule(FieldRule):
    '''
        does dimension, dimension group, or measure follow some lexicon rules?
    '''

    def run(self, lookml_field):
        '''apply some lexion rules:

        we want:
            member not "Subscriber"
            membership not "Subscription"
            workshop not "studio"

        so this is a has subscriber, has suscription, or has studio rule in name or description.

        Args:
            lookml_field (LookMLField): instance of LookMLField

        Returns:
            (tuple): tuple containing:

                relevant (bool): is this rule relevant for this JSON chunk?

                passed (bool): did the rule pass?

        '''
        if not (lookml_field.is_dimension() or lookml_field.is_dimension_group() or lookml_field.is_measure()):
            return False, None

        # check name
        name = lookml_field.name
        passed = not ('subscriber' in name or 'subscription' in name or 'studio' in name)

        # check description
        if lookml_field.has_key('description') and lookml_field.description != "":
            desc = lookml_field.description.lower()
            ok = not ('subscriber' in desc or 'subscription' in desc or 'studio' in desc)
            passed = passed and ok

        return True, passed
