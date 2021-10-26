'''
    modify file with additions or substitutions, and making as few other changes 
    as possible (no formatting, whitespace, encoding etc)

    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)

        git add config/linter/config_linter.json
        git add config/updater/config_updater.json
        git add definitions.csv
        git add lkmltools/linter/lookml_linter.py
        git add lkmltools/linter/rule_factory.py
        git add lkmltools/updater/bq_definitions_provider.py
        git add lkmltools/updater/definitions_provider_factory.py
        git add lkmltools/updater/file_modifier.py
        git add lkmltools/updater/lookml_modifier.py

'''
import os
import logging

class FileModifier():
    '''
        class that modifies file with additions or substitutions, and doing so
        with making as few other changes as possible (no formatting, whitespace, encoding etc)
    '''

    COMMENT = ""

    def __init__(self, filename):
        '''initialize the FileModifier

        Args:
            filename (str): filename

        '''
        if not os.path.exists(filename):
            raise IOError("Filename does not exist: %s" % filename)

        logging.info("Reading in file %s", filename)
        self.lines = open(filename, 'r').readlines()

    def is_header(self, line, header_type, header_name):
        '''looking for start of dimension or header, e.g.
                "dimension: header_name {"

        Args:
            line (str): line from a file
            header_type (str): e.g. dimension
            header_name (str): e.g. header_name (in example above)

        Returns:
            bool: is this chunk a header?

        '''
        start = header_type + ":"
        if line.strip().startswith(start) and line.split(start)[1].split("{")[0].strip() == header_name:
            return True
        return False

    def handle_parameter_addition(self, definition_type, name, parameter_name, parameter_value):
        '''add in a new parameter

        Args:
            definition_type (str): 'measure' or 'dimension'
            name (str): name of measure or dimension
            parameter (str): parameter to add

        Returns:
            nothing. Side effect is to add lines to self.lines

        '''
        new_lines = []
        for line in self.lines:
            if self.is_header(line, definition_type, name):
                line_to_add = "    %s: \"%s\"\t%s\n" % (parameter_name, parameter_value, FileModifier.COMMENT)
                logging.info("Adding in line: %s" % line_to_add)
                new_lines.append(line) # header
                new_lines.append(line_to_add)
            else:
                new_lines.append(line)
        self.lines = new_lines

    def handle_parameter_substitution(self, num_lines, definition_type, name, parameter_name, parameter_value):
        '''as parameter exists, we need to find the header, then look for parameter after it,
            consume all the lines of the current parameter, and add the new parameter

        Args:
            num_lines (int): number of lines in the existing parameter
            definition_type (str): 'measure' or 'dimension'
            name (str): name of measure or dimension
            parameter (str): parameter to add

        Returns:
            Nothing. Side effect to save to self.lines

        '''
        new_lines = []
        iterator = iter(self.lines)
        while iterator:
            try:
                line = next(iterator)
                if self.is_header(line, definition_type, name):
                    new_lines.append(line)
                    ct = 0 
                    while True:
                        line = next(iterator)
                        ct += 1
                        if line.strip().startswith(parameter_name):
                            logging.info("found %s %d lines after header", parameter_name, ct)

                            # consume the other lines for this existing parameter
                            for i in range(num_lines):
                                line = next(iterator)

                            # inject our new parameter
                            line_to_add = "    %s: \"%s\"\t%s\n" % (parameter_name, parameter_value, FileModifier.COMMENT)
                            logging.info("Adding in line: %s", line_to_add)
                            new_lines.append(line_to_add)
                            break

                        else:
                            new_lines.append(line)
                new_lines.append(line)
            except StopIteration:
                break
        self.lines = new_lines

    def modify(self, num_lines, definition_type, name, parameter_name, parameter_value, has_key):
        '''

        modify an entry

        Args:
            num_lines (int): number of lines to substitute
            has_key (bool): do we have a parameter key for the definition_type,
            name (str): name of dimension, dimension_group, or measure
            parameter (str): correct parameter

        Returns:
            nothing. Side effect is to update self.lines with correct info

        '''
        if not has_key:
            self.handle_parameter_addition(definition_type, name, parameter_name, parameter_value)
        else:
            self.handle_parameter_substitution(num_lines, definition_type, name, parameter_name, parameter_value)

    def organize(self):


    def write(self, filename):
        '''write modified LookML to filename

        Args:
            filename (str): filepath of file to write to

        Returns:
            nothing. Side effect is to write data to file

        '''
        logging.info("Writing LookML to %s" % filename)
        with open(filename, 'w') as the_file:
            for line in self.lines:
                the_file.write(line)
