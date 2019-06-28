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

import lkml
class LookML():

    def get_json_representation(self, infilepath):
        '''parse the LookML infilepath, convert to JSON, and then read into JSON object

        Args:
            infilepath (str): path to input LookML file

        Returns:
            JSON object of LookML

        '''
        if not os.path.exists(infilepath):
            raise IOError("Filename does not exist: %s" % infilepath)

        with open(infilepath, 'r') as file:
            json_data = lkml.load(file)
            m = {}
            m['base_filename'] = os.path.basename(infilepath)
            m['base_name'] = m['base_filename'].replace(".model.lkml", "").replace(".explore.lkml", "").replace(".view.lkml", "")
            m['filename'] = infilepath
            m['filetype'] = ""
            if infilepath.endswith(".model.lkml"):
                m['filetype'] = 'model'
            elif infilepath.endswith(".view.lkml"):
                m['filetype'] = 'view'
            elif infilepath.endswith(".explore.lkml"):
                m['filetype'] = 'explore'
            else:
                raise Exception("Unsupported filename " + infilepath)
            json_data['metadata'] = m
            return json_data