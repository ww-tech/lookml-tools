'''
    parse a LookML file from LookML to JSON

    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)
'''
import logging
import subprocess
import os
import json
import shlex

class LookML():

    def __init__(self, config):
        self.config = config

    def create_command(self, filename):
        '''create the command that will parse the LookML and convert to a JSON object

        Args:
            filename (str): filepath of input LookML file

        Returns:
            list of unix command strings

        '''
        command = [self.config['parser']]
        command.append("--input=%s" % filename) #note: no single quotes around %s for shell=False
        command.append('--whitespace=2')
        return command

    def parse_repo(self, filename):
        '''parse the LookML and convert to a JSON object

        Note: 
            this runs a parser on the command line. It is not Python code

        Args:
            filename (str): filepath of input LookML file

        Returns:
            output: output from subprocess call
            error: error from subprocess call

        '''
        outfile = self.config['tmp_file']
        with open(outfile, 'w') as outf:
            cmd = self.create_command(filename)
            logging.info("running % s", " ".join(cmd + [">", outfile]))
            process = subprocess.Popen(cmd, shell=False, stdout=outf, stderr=outf)
            output, error = process.communicate()
            return output, error

    def get_json_representation(self, infilepath):
        '''parse the LookML infilepath, convert to JSON, and then read into JSON object

        Args:
            infilepath (str): path to input LookML file

        Returns:
            JSON object of LookML

        '''
        if not os.path.exists(infilepath):
            raise IOError("Filename does not exist: %s" % infilepath)

        _, error = self.parse_repo(infilepath)

        if error:
            raise Exception(str(error))

        with open(self.config['tmp_file']) as json_file:
            json_data = json.load(json_file)
            return json_data
