'''
    a lexicon rule

    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)
'''
from lkmltools.linter.rule import Rule

class LexiconRule(Rule):
    '''
        does dimension, dimension group, or measure follow some lexicon rules?
    '''

    def run(self, json_data):
        '''apply some lexion rules:

        we want:
            member not "Subscriber"
            membership not "Subscription"
            workshop not "studio"

        so this is a has subscriber, has suscription, or has studio rule in name or description.

        Args:
            json_data (JSON): json_data of the lookml-parser dictionary for this dimension, dimension_group, or measure only

        Returns:
            (tuple): tuple containing:

                relevant (bool): is this rule relevant for this JSON chunk?

                passed (bool): did the rule pass?

        '''
        # not relevant
        if not '_type' in json_data or not json_data['_type'] in ['dimension', 'measure', 'dimension_group']:
            return False, None

        # check name
        name = json_data['_' + json_data['_type']].lower()
        passed = not ('subscriber' in name or 'subscription' in name or 'studio' in name)

        # check description
        if 'description' in json_data:
            desc = json_data['description'].lower()
            ok = not ('subscriber' in desc or 'subscription' in desc or 'studio' in desc)
            passed = passed and ok

        return True, passed
