'''understand additions or modifications to be made and then delegate
    to filemodifier to make requested changes

    Authors:
        Carl Anderson (carl.anderson@weightwatchers.com)

'''
import os
import logging
import pandas as pd
from lkmltools.updater.file_modifier import FileModifier
from lkmltools.util import FieldCategory
from lkmltools.lookml import LookML
from lkmltools.updater.definitions_provider_factory import DefinitionsProviderFactory

class LookMlModifier():
    '''
        class that understands additions or modifications to be made and then delegates
        to filemodifier to make requested changes
    '''

    def __init__(self, config):
        '''initialize the LookMlModifier

        Args:
            config (JSON): the JSON configuration

        '''
        #super(LookMlModifier).__init__(filepath)
        self.config = config
        definitions_provider = DefinitionsProviderFactory.instantiate(config["definitions"]['type'], config)
        self.definitions = definitions_provider.get_definitions()

    def find_description(self, lookml, header_type, header_name):
        '''get the description, if any, from this measure or dimension

        Args:
            lookml (LookML): instance of LookML
            header_type (str): 'measure' or 'dimension'
            header_name (str): name of measure or dimension            

        Returns:
            description (str): description, if any, from dimension, dimension_group, or measure
            boolean: whether it has one

        '''
        if lookml.filetype != "view":
            raise Exception("Only views are supported. This is type " + lookml.filetype)

        # coding standards say that we should have one view per file
        n = len(lookml.views())
        if n > 1:
            raise Exception("There should only 1 view. We found %d" % n) 

        v = lookml.views()[0]

        if header_type not in [FieldCategory.DIMENSION.value,  FieldCategory.DIMENSION_GROUP.value, FieldCategory.MEASURE.value]:
            raise Exception("Unrecognized header_type %s" % header_type)

        plural_key = header_type + "s"
        if not plural_key in v:
            raise IOError("Did not find %s %s" % (header_type, header_name))

        found = False
        for d in v[plural_key]:
            if d['name'] == header_name:
                found=True
                break
        if not found:
            raise IOError("Did not find %s %s" % (header_type, header_name))

        if FieldCategory.DESCRIPTION.value in d:
            return d[FieldCategory.DESCRIPTION.value], True
        else:
            return "", False

    def modify(self, infilepath, outfilepath):
        '''modify the LookML

        Notes:
            default behavior is to match on full path when matching LookML files
            with the definitions source. 
            However, you can configure to match on LookML file basename by setting
            ``"use_basename": true`` in the config

        Args:
            infilepath (str): path to input LookML file
            outfilepath (str): path of updated LookML to wtite to

        Returns:
            nothing. Writes out modified file contents to file

        '''
        modifier = FileModifier(infilepath)

        lookml = LookML(infilepath)

        # get definitions for this file. In some cases, we might not
        # easily know the full path (such as full_auto_updater.sh which
        # uses timestamp in the git clone). Thus, just match on basename
        if 'use_basename' in self.config and self.config['use_basename']:
            logging.info("Matching files based on basename")
            defs = self.definitions[self.definitions.file == os.path.basename(infilepath)]
        else:
            defs = self.definitions[self.definitions.file == infilepath]

        for definition in defs.T.to_dict().values():
            logging.info("Processing %s: %s", definition['type'], definition['name'])

            description, has_key = self.find_description(lookml, definition['type'], definition['name'])

            num_lines = len(description.split("\n"))

            if has_key:
                logging.info("Existing description for %s.%s: '%s'", definition['type'], definition['name'], description)
            else:
                logging.info("No description for %s.%s", definition['type'], definition['name'])

            exepected_description = definition['definition']

            if description != exepected_description:
                if has_key:
                    logging.info("Update needed: %s.%s -> '%s'", definition['type'], definition['name'], exepected_description)
                    logging.info("This is %d line existing description", num_lines)
                else:
                    logging.info("Injection needed: %s.%s -> '%s'", definition['type'], definition['name'], exepected_description)

                modifier.modify(num_lines, definition['type'], definition['name'], exepected_description, has_key)

        modifier.write(outfilepath)
