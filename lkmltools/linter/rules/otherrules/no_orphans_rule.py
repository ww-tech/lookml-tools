'''
    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)

'''
import logging
from lkmltools.grapher.lookml_grapher import LookMlGrapher
from lkmltools.linter.rule import Rule

class NoOrphansRule(Rule):
    '''
        Look for views unreferenced by any explores
    '''

    def __init__(self, config):
        '''Initialize the rule

        Args:
            config (JSON): configuration

        '''
        self.config = config
        self.grapher = LookMlGrapher(config)
        self.view_dict = {}

    def run(self, json_data):
        '''run the rule

        Args:
            json_data (JSON): json_data of the lookml-parser dictionary for this file

        Returns:
            (tuple): tuple containing:

                relevant (bool): is this rule relevant for this JSON chunk?

                passed (bool): did the rule pass?

        '''
        pass # pragma: no cover

    def process_file(self, json_data):
        '''process the JSON_DATA of a file, delegating down to the grapher
            also store metadata we'll need in a later stage

        Args:
            json_data (JSON): json_data: parsed lkml file as JSON

        Returns:
            nothing. side effect is to store data in grapher and in this class

        '''
        self.grapher.process_file(filepath=None, json_data=json_data)
        # we'll need the view_namme->filename mapping to output later
        if 'views' in json_data['files'][0]:
            view_name = json_data['files'][0]['views'][0]['_view']
            filepath = json_data['files'][0]['_file_path']
            self.view_dict[view_name] = filepath

    def finish_up(self, file_out):
        '''find the orphans, if any, and add results to file_out

        Args:
            file_out (list): list of results for files

        Returns:
            file_out (list)

        '''
        self.grapher.tag_orphans()
        orphans = self.grapher.orphans()
        for orphan in orphans:
            simple_filepath = self.view_dict[orphan] #['files'][0]['_file_path']
            logging.info("Found orphan %s in %s", orphan, simple_filepath)
            out = {"file": simple_filepath, "rule": self.name(), "passed": 0}
            file_out.append(out)
        return (file_out)
