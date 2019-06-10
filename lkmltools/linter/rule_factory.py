'''
    a rule factory

    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)
'''
from lkmltools.linter.rules.filerules.one_view_per_file_rule import OneViewPerFileRule
from lkmltools.linter.rules.filerules.filename_viewname_match_rule import FilenameViewnameMatchRule
from lkmltools.linter.rules.filerules.data_source_rule import DataSourceRule
from lkmltools.linter.rules.fieldrules.description_rule import DescriptionRule
from lkmltools.linter.rules.fieldrules.all_caps_rule import AllCapsRule
from lkmltools.linter.rules.fieldrules.count_name_rule import CountNameRule
from lkmltools.linter.rules.fieldrules.yesno_name_rule import YesNoNameRule
from lkmltools.linter.rules.fieldrules.drill_down_rule import DrillDownRule
from lkmltools.linter.rules.fieldrules.lexicon_rule import LexiconRule

class RuleFactory():
    '''
        factory to instantiate rules
    '''

    @staticmethod
    def instantiate(class_name):
        '''instantiate instances of rule, given name of rule class

        Args:
            class_name (str): name of the class

        Returns:
            instance (Rule): instance of a rule

        '''
        dictionary = {
            "OneViewPerFileRule": OneViewPerFileRule,
            "FilenameViewnameMatchRule": FilenameViewnameMatchRule,
            "DataSourceRule": DataSourceRule,
            "DescriptionRule": DescriptionRule,
            "AllCapsRule": AllCapsRule,
            "CountNameRule": CountNameRule,
            "DrillDownRule": DrillDownRule,
            "YesNoNameRule": YesNoNameRule,
            "LexiconRule": LexiconRule
        }
        return dictionary[class_name]()
