from abc import abstractmethod
import pandas as pd
from lkmltools.updater.definition_provider import DefinitionProvider

class AbstractSqlReader(DefinitionProvider):
    """A reader that explicitly reads from relational DB using SQL and is able to run pd.read_sql"""

    @abstractmethod
    def get_connection(self):
        """
            Returns:
                a database connection, one that is compatible with pd.read_sql
        """
        pass # pragma: no cover

    def get_credentials(self):
        """extract credentials from config

        Returns:
            host (str): hostname
            port (int): port
            database (str): database name
            username (str): username
            password (str): password

        """
        section = self.config['definitions']
        host = section['host']
        port = int(section['port'])
        database = section['database']
        username = section['username']
        password = section['password']
        return (host, port, username, password, database)

    def get_definitions(self):
        '''get the definitions from the master source

        Returns:
            df (pandas dataframe): dataframe

        '''
        query = self.config['definitions']['query']
        conn = self.get_connection()
        return pd.read_sql(query, con=conn)
