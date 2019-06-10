'''
    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)
'''
import pandas_gbq
from lkmltools.updater.definition_provider import DefinitionProvider

class BqDefinitionsProvider(DefinitionProvider):
    """
        A definitions provider that provides definitions from a BigQuery table
    """
    def get_definitions(self):
        '''get the definitions from the master source

        Returns:
            df (pandas dataframe): dataframe

        '''
        projectid = self.config["definitions"]['project']

        if 'query' in self.config["definitions"]:
            q = self.config["definitions"]['query']
        else:
            dataset = self.config["definitions"]['dataset']
            table = self.config["definitions"]['table']
            q = """SELECT * FROM `%s.%s`""" % (dataset, table)

        return pandas_gbq.read_gbq(q, project_id=projectid)
