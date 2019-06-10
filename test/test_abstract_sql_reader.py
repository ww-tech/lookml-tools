
import pytest
from unittest.mock import patch
import pandas as pd
from lkmltools.updater.mysql_reader import MySQLReader

def test_get_credentials():
    config = {
        "definitions": {
            "type": "MySQLReader",
            "query": "select * from test",
            "username": "myusername",
            "password": "mysecret",
            "port": 3306,
            "host": "127.0.0.1",
            "database": "mydb"
        }
    }
    reader = MySQLReader(config)
    host, port, username, password, database = reader.get_credentials()
    assert host == "127.0.0.1"
    assert port == 3306
    assert username == "myusername"
    assert password == "mysecret"
    assert database == "mydb"
