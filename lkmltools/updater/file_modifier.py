'''
    modify file with additions or substitutions, and making as few other changes 
    as possible (no formatting, whitespace, encoding etc)

    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)
'''
import os
import logging

class FileModifier():
    '''
        class that modifies file with additions or substitutions, and doing so
        with making as few other changes as possible (no formatting, whitespace, encoding etc)
    '''

    COMMENT = "# programmatically added by LookML modifier"

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
        #FIXME this assumes brace is on same line. Valid LookML means that it doesn't have to be
        if line.strip().startswith(start) and line.split(start)[1].split("{")[0].strip() == header_name:
            return True
        return False

    def handle_description_addition(self, definition_type, name, description):
        '''add in a new description

        Args:
            definition_type (str): 'measure' or 'dimension'
            name (str): name of measure or dimension
            description (str): description to add

        Returns:
            nothing. Side effect is to add lines to self.lines

        '''
        new_lines = []
        for line in self.lines:
            if self.is_header(line, definition_type, name):
                line_to_add = "    description: \"%s\"\t%s\n" % (description, FileModifier.COMMENT)
                logging.info("Adding in line: %s" % line_to_add)
                new_lines.append(line) # header
                new_lines.append(line_to_add)
            else:
                new_lines.append(line)
        self.lines = new_lines

    def handle_desription_substitution(self, num_lines, definition_type, name, description):
        '''as description exists, we need to find the header, then look for description after it,
            consume all the lines of the current description, and add the new description

        Args:
            num_lines (int): number of lines in the existing description
            definition_type (str): 'measure' or 'dimension'
            name (str): name of measure or dimension
            description (str): description to add

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
                        if line.strip().startswith("description"):
                            logging.info("found description %d lines after header", ct)

                            # consume the other lines for this existing description
                            for i in range(num_lines):
                                line = next(iterator)

                            # inject our new description
                            line_to_add = "    description: \"%s\"\t%s\n" % (description, FileModifier.COMMENT)
                            logging.info("Adding in line: %s", line_to_add)
                            new_lines.append(line_to_add)
                            break

                        else:
                            new_lines.append(line)
                new_lines.append(line)
            except StopIteration:
                break
        self.lines = new_lines

    def modify(self, num_lines, definition_type, name, description, has_key):
        '''

        modify an entry

        Args:
            num_lines (int): number of lines to substitute
            has_key (bool): do we have a description key for the definition_type, 
            name (str): name of dimension, dimension_group, or measure
            description (str): correct description

        Returns:
            nothing. Side effect is to update self.lines with correct info

        '''
        if not has_key:
            self.handle_description_addition(definition_type, name, description)
        else:
            self.handle_desription_substitution(num_lines, definition_type, name, description)

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
