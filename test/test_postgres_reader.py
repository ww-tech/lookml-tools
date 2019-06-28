
import pytest
from unittest.mock import patch
import pandas as pd
from lkmltools.updater.postgres_reader import PostgreSQLReader

def test_get_definitions(monkeypatch):
    config = {
        "definitions": {
            "type": "PostgreSQLReader",
            "query": "select * from test",
            "username": "myusername",
            "password": "mysecret",
            "port": 5432,
            "host": "127.0.0.1",
            "database": "mydb"
        }
    }
    reader = PostgreSQLReader(config)

    with patch(target='psycopg2.connect') as mock:

        def fake_df(query, con):
            return pd.DataFrame({'file': ['test/basic.view.lkml'],'type':['dimension'],'name':['tier'],'definition':['this is a new description']})
        monkeypatch.setattr(pd,'read_sql',fake_df)

        df = reader.get_definitions()

        assert list(df.T.to_dict().values())[0] == {'file': 'test/basic.view.lkml','type':'dimension','name':'tier','definition':'this is a new description'}
