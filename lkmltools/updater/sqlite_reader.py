"""
    Read definitions from SQLite
    
    author(s): Carl Anderson (carl.anderson@weightwatchers.com)

"""
import sqlite3
from lkmltools.updater.abstract_sql_reader import AbstractSqlReader

class SQLiteReader(AbstractSqlReader):
    """Runs SQLite queries into pandas dataframes"""

    def get_connection(self):
        '''Create and return connection to SQLite database file

        Returns:
            connection to SQLite file

        '''
        return sqlite3.connect(self.config['definitions']['filename'])
