"""
    Read definitions from PostgreSQL
    
    author(s): Carl Anderson (carl.anderson@weightwatchers.com)

"""
import psycopg2
from lkmltools.updater.abstract_sql_reader import AbstractSqlReader

class PostgreSQLReader(AbstractSqlReader):
    """Runs PostgreSQL queries into pandas dataframes"""

    def get_connection(self):
        '''Create and return connection to a MySQL database

        Returns:
            connection to PostgreSQL DB

        '''
        host, port, username, password, database = self.get_credentials()
        conn = psycopg2.connect(dbname=database, user=username, password=password, host=host, port=port, sslmode='require')
        return conn
