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
import re

import lkml
class LookML():

    def __init__(self, infilepath):
        '''parse the LookML infilepath, convert to JSON, and then read into JSON object

        Args:
            infilepath (str): path to input LookML file

        Returns:
            JSON object of LookML

        '''
        if not os.path.exists(infilepath):
            raise IOError("Filename does not exist: %s" % infilepath)

        self.infilepath = infilepath
        self.base_filename = os.path.basename(infilepath)

        if self.base_filename.endswith(".model.lkml"):
            self.filetype = 'model'
        elif self.base_filename.endswith(".explore.lkml"):
            self.filetype = 'explore'
        elif self.base_filename.startswith("explore_") and self.base_filename.endswith(".lkml"):
            self.filetype = 'explore'
        elif self.base_filename.endswith(".view.lkml"):
            self.filetype = 'view'
        elif self.base_filename.endswith(".lkml"):
            # consider everything else as a view
            self.filetype = 'view'
        else:
            raise Exception("Unsupported filename " + infilepath)
        
        self.base_name = re.sub(r'\.\w+\.lkml$', '', self.base_filename)
        with open(infilepath, 'r') as file:
            self.json_data = lkml.load(file)

    def views(self):
        """get views (if any) from the LookML

        Returns:
            views (list) if any, None otherwise

        """
        if 'views' in self.json_data:
            return self.json_data['views']
        return None

    def has_views(self):
        """does this have one or more views?

        Returns:
            bool, whether this has views

        """
        vs = self.views()
        return (vs and len(vs) > 0)

    def explores(self):
        """get explores (if any) from the LookML

        Returns:
            explores (list) if any, None otherwise

        """
        if 'explores' in self.json_data:
            return self.json_data['explores']
        return None

    def has_explores(self):
        """does this have one or more explores?

        Returns:
            bool, whether this has explores

        """
        es = self.explores()
        return (es and len(es) > 0)
