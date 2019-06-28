
import pytest
from unittest.mock import patch
import pandas as pd
from lkmltools.updater.mysql_reader import MySQLReader

def test_get_definitions(monkeypatch):
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

    with patch(target='mysql.connector.connect') as mock:

        def fake_df(query, con):
            return pd.DataFrame({'file': ['test/basic.view.lkml'],'type':['dimension'],'name':['tier'],'definition':['this is a new description']})
        monkeypatch.setattr(pd,'read_sql',fake_df)

        df = reader.get_definitions()

        assert list(df.T.to_dict().values())[0] == {'file': 'test/basic.view.lkml','type':'dimension','name':'tier','definition':'this is a new description'}
