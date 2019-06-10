'''

    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)
'''
import os
import pandas as pd
from lkmltools.updater.definition_provider import DefinitionProvider

class CsvDefinitionsProvider(DefinitionProvider):
    """
        A definitions provider that provides definitions from a CSV file
    """

    def get_definitions(self):
        '''get the definitions from the master source

        Returns:
            df (pandas dataframe): dataframe

        '''
        filename = self.config["definitions"]['filename']
        assert os.path.exists(filename)
        return pd.read_csv(filename)
