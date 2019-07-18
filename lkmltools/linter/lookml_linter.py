'''
    LookML linter: applies set of rules to some LookML file

    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)
'''
import logging
import datetime
import glob
import os
import pandas as pd
from lkmltools.linter.rule_factory import RuleFactory
from lkmltools.lookml import LookML
from lkmltools.lookml_field import LookMLField
from lkmltools.linter.rules.otherrules.no_orphans_rule import NoOrphansRule
from lkmltools.bq_writer import BqWriter
from lkmltools.simple_bq_writer import SimpleBqWriter

class LookMlLinter():
    '''
        A LookML linter that lints a set of LookML files specified in some config
        using a set of rules, specified in same config
    '''

    def __init__(self, config):
        '''instantiate this linter

        Args:
            config (JSON): the config

        '''
        self.config = config
        self.initialize_rules(config)

    def initialize_rules(self, config):
        '''create the set of rules, as specified in the config file

        Args:
            config (JSON): the config

        Returns:
            nothing. side effect is to create internal list of file level rules and internal list
            of field level rules

        '''
        def create_rules(k, s):
            out = []
            if k in config['rules']:
                for rule in config['rules'][k]:
                    if rule['run']:
                        logging.info("Creating %s Rule %s" % (s, rule['name']))
                        out.append(RuleFactory().instantiate(rule['name'], rule))
            return out

        self.file_rules = create_rules('file_level_rules', 'File-level')
        self.field_rules = create_rules('field_level_rules', 'Field-level')

    def run_file_rules(self, lookml, simple_filepath, file_out):
        '''run the set of file level rules against some json_data, that came from simple_filepath,
            and append results to file_out list

        Args:
            lookml (LookML): instance of LookML
            simple_fileapath (str): path to some file
            file_out (list): list of results for file-level rules

        Returns:
            input file_out list with additional dictionary results

        '''
        for rule in self.file_rules:
            relevant, passed = rule.run(lookml)
            if relevant:
                d = {"file": simple_filepath, "rule": rule.name(), "passed": int(passed)}
                file_out.append(d)
                logging.debug(d)
        return file_out

    def run_field_rules(self, v, single_key, plural_key, simple_filepath, field_out):
        '''run the set of field-level rules against some json_data, that came from simple_filepath,
            and append results to field_out list

        Args:
            v (JSON): list of views
            single_key (str): e.g. dimension
            plural_key (str): e.g. dimensions
            simple_fileapath (str): path to some file
            field_out (list): list of results for field-level rules

        Returns:
            input field_out list with additional dictionary results

        '''
        ## unfortunately, "view: dim_date {}" is a valid file so it might not have any measures or dimensions
        if not plural_key in v:
            return field_out

        for json_d in v[plural_key]:
            json_d['_type'] = single_key
            f = LookMLField(json_d)
            for rule in self.field_rules:
                relevant, passed = rule.run(f)
                if relevant:
                    d = {"file": simple_filepath, "rule": rule.name(), "passed": int(passed), "type": single_key, "fieldname": json_d['name']} #['_' + single_key]}
                    field_out.append(d)
                    logging.debug(d)
        return field_out

    def write_file_csv(self, df):
        '''write file data to CSV

        Args:
            df (pandas dataframe): dataframe

        Returns:
            nothing. Writes data to CSV

        '''
        df.to_csv(self.config['output']['csv']['file_output'], index=False, columns=["time", "file", "rule", "passed","repo", "glob"])
        logging.info("File output written to %s", self.config['output']['csv']['file_output'])

    def write_field_csv(self, df):
        '''
            write field data to CSV
            Args:
                df (pandas dataframe): dataframe

            Returns:
                nothing. Writes data to CSV
        '''
        df.to_csv(self.config['output']['csv']['field_output'], index=False, columns=["time", "file", "rule", "type", "fieldname", "passed","repo", "glob"])
        logging.info("Field output written to %s", self.config['output']['csv']['field_output'])

    def other_rules_to_run(self):
        '''
            Get set of other rules to run
            
            Returns:
                out (set): set of names of rules
        '''
        out=set()
        if 'other_rules' in self.config['rules']:
            for rule in self.config['rules']['other_rules']:
                if 'name' in rule and 'run' in rule and rule['run']:
                    out.add(rule['name'])
        return out

    def run(self):
        '''
            run the set of file and field-level rules against all files in the file glob

            Returns:
                nothing. Saves two CSV files, specified in the config
        '''

        file_out = []
        field_out = []

        timestr = datetime.datetime.now().isoformat()

        no_orphans_rule = None
        if "NoOrphansRule" in self.other_rules_to_run():
            no_orphans_rule = NoOrphansRule(self.config)

        globstrings = self.config['infile_globs']
        for globstring in globstrings:
            filepaths = glob.glob(globstring)
            for filepath in filepaths:

                simple_filepath = os.path.basename(filepath)

                logging.info("Processing %s", filepath)

                lookml = LookML(filepath)

                file_out = self.run_file_rules(lookml, simple_filepath, file_out)

                if lookml.has_views():
                    v = lookml.views()[0]
                    field_out = self.run_field_rules(v, 'dimension', 'dimensions', simple_filepath, field_out)
                    field_out = self.run_field_rules(v, 'dimension_group', 'dimension_groups', simple_filepath, field_out)
                    field_out = self.run_field_rules(v, 'measure', 'measures', simple_filepath, field_out)

                if no_orphans_rule:
                    no_orphans_rule.process_lookml(lookml)

            #add some metadata for each of the records we created above
            [f.update({'glob': globstring}) for f in field_out + file_out if not 'glob' in f]

        # for this rule, we can only assess who failed after all files are processed
        if no_orphans_rule:
            file_out = no_orphans_rule.finish_up(file_out)

        if 'simple_biquery' in self.config['output']:
            simple_bq_writer = SimpleBqWriter()
        if 'bigquery' in self.config['output']:
            bq_writer = BqWriter()

        if len(file_out) > 0:
            df = pd.DataFrame(file_out)
            df['time'] = timestr
            df['repo'] = self.config['git']['url']

            if 'csv' in self.config['output']:
                self.write_file_csv(df)

            if 'simple_biquery' in self.config['output']:
                simple_bq_writer.upload(df, self.config, 'file_destination_table')

            if 'bigquery' in self.config['output']:
                bq_writer.upload(df, self.config, 'file_destination_table')

        if len(field_out) > 0:
            df = pd.DataFrame(field_out)
            df['time'] = timestr
            df['repo'] = self.config['git']['url']

            if 'csv' in self.config['output']:
                self.write_field_csv(df)

            if 'simple_biquery' in self.config['output']:
                simple_bq_writer.upload(df, self.config, 'field_destination_table')

            if 'bigquery' in self.config['output']:
                bq_writer.upload(df, self.config, 'field_destination_table')

        return file_out, field_out
