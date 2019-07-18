
import pytest
import pandas_gbq
import pandas as pd
from lkmltools.updater.bq_definitions_provider import BqDefinitionsProvider

def test_get_definitions(monkeypatch):
    config = {
        "definitions": {
            "project": "myproject",
            "query": "select * from mytable"
        }
    }
    reader = BqDefinitionsProvider(config)

    def fake_df(q, project_id):
        return pd.DataFrame({'file': ['test/basic.view.lkml'],'type':['dimension'],'name':['tier'],'definition':['this is a new description']})
    monkeypatch.setattr(pandas_gbq,'read_gbq',fake_df)

    df = reader.get_definitions()

    assert list(df.T.to_dict().values())[0] == {'file': 'test/basic.view.lkml','type':'dimension','name':'tier','definition':'this is a new description'}
