import pytest
import os
import sqlite3
from lkmltools.updater.sqlite_reader import SQLiteReader

def test_get_definitions():
    db_filename = "test/test_abstract_sqlite.db"
    if os.path.exists(db_filename):
        os.remove(db_filename)

    conn = sqlite3.connect(db_filename)
    c = conn.cursor()
    c.execute("create table test(file text, type text, name text, definition text);")
    c.execute("insert into test(file, type, name, definition) values('test/basic.view.lkml','dimension','tier','this is a new description');")
    conn.commit()
    conn.close()

    config = {
        "definitions": {
            "type": "SQLiteReader",
            "filename": "test/test_abstract_sqlite.db",
            "query": "select * from test"
        }
    }

    reader = SQLiteReader(config)
    df = reader.get_definitions()
    results = list(df.T.to_dict().values())
    assert results[0] == {'file': 'test/basic.view.lkml','type':'dimension','name':'tier','definition':'this is a new description'}
   
    if os.path.exists(db_filename):
        os.remove(db_filename)