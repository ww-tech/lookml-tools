"""
    Read definitions from MySQL
    
    author(s): Carl Anderson (carl.anderson@weightwatchers.com)

"""
import mysql.connector
from lkmltools.updater.abstract_sql_reader import AbstractSqlReader

class MySQLReader(AbstractSqlReader):
    """Runs MySQL queries into pandas dataframes"""

    def get_connection(self):
        '''Create and return connection to a MySQL database

        Returns:
            connection to MySQL DB

        '''
        host, port, username, password, database = self.get_credentials()
        conn = mysql.connector.connect(database=database, user=username, passwd=password, host=host, port=port, auth_plugin='mysql_native_password')
        return conn
