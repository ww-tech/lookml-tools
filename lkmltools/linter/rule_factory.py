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
import logging

class RuleFactory():
    '''
        Singleton Factory where one can register Rules for instantiation
    '''
    instance = None

    def __init__(self):
        """instantiate the factory but as a singleton. The guard rails are here"""
        # where the magic happens, only one instance allowed:
        if not RuleFactory.instance:
            RuleFactory.instance = RuleFactory.__HiddenFactory()

    def __getattr__(self, name):
        """getattr with instance name

        Returns:
            gettattr

        """
        return getattr(self.instance, name)

    class __HiddenFactory:
        """actual factory where registry and instantiation happens"""

        def __init__(self):
            """instantiate the HiddenFactory"""
            self.name_dict = {
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

        def instantiate(self, class_name, json_config=None):
            '''instantiate instances of rule, given name of rule class

            Args:
                class_name (str): name of the class

            Returns:
                instance (Rule): instance of a rule

            '''
            return self.name_dict[class_name](json_config)

        def register(self, key, class_obj):
            """Registering class_obj with key

            Args:
                key (str): key such as class name, e.g. 'AllCapsRule'
                class_obj (class obj), e.g. AllCapsRule

            Returns:
                nothing. Side effect is to register the class

            """
            #FIXME do we want to warn/raise on overwriting?
            self.name_dict[key] = class_obj
            logging.debug("Registered %s : %s" % (key, class_obj))

        def is_registered(self, class_key):
            """is this class registered?

            Args:
                class_key (str): key used to register class

            Returns:
                determination (boolean) of whether this is already register

            """
            return class_key in self.name_dict

        def unregister(self, key):
            """unregister an entry

            Arguments:
                key (str): key to unregister

            Returns:
                nothing. Side effect is that the object is unregistered

            """
            if key in self.name_dict:
                del self.name_dict[key]
                logging.info("Unregistered %s", key)
            else:
                raise Exception("Key not found " + key)
