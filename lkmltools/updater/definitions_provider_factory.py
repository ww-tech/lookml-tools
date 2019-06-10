'''
    definitions provider factory

    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)
'''
from lkmltools.updater.csv_definitions_provider import CsvDefinitionsProvider
from lkmltools.updater.sqlite_reader import SQLiteReader
from lkmltools.updater.bq_definitions_provider import BqDefinitionsProvider
from lkmltools.updater.mysql_reader import MySQLReader
from lkmltools.updater.postgres_reader import PostgreSQLReader

class DefinitionsProviderFactory():
    '''
        factory to instantiate DefinitionsProvider
    '''

    @staticmethod
    def instantiate(class_name, config):
        '''instantiate instances of definitions provider, given name of class

        Args:
            config (JSON): configuration JSON

        Returns:
            instance of a DefinitionsProvider

        '''
        dictionary = {
            "CsvDefinitionsProvider": CsvDefinitionsProvider,
            "BqDefinitionsProvider": BqDefinitionsProvider,
            "SQLiteReader": SQLiteReader,
            "MySQLReader": MySQLReader,
            "PostgreSQLReader": PostgreSQLReader
        }
        return dictionary[class_name](config)
