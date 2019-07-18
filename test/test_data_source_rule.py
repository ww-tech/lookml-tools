import pytest
import json
import os
from lkmltools.linter.rules.filerules.data_source_rule import DataSourceRule
from conftest import get_lookml_from_raw_lookml

def test_run1():
    raw_lookml = """
      view: aview {
        sql_table_name: bqdw.engagement_score ;;
      }
    """
    lookml = get_lookml_from_raw_lookml(raw_lookml, 'aview.view')
    relevant, passed = DataSourceRule().run(lookml)
    assert relevant
    assert passed
    if os.path.exists(lookml.infilepath):
      os.remove(lookml.infilepath)

def test_run2():
    raw_lookml = """
      view: aview {
        dimension: memberID {
          type: string
        }
      }
    """
    lookml = get_lookml_from_raw_lookml(raw_lookml, 'aview.view')
    relevant, passed = DataSourceRule().run(lookml)
    assert relevant
    assert not passed
    if os.path.exists(lookml.infilepath):
      os.remove(lookml.infilepath)

def test_run3():
    raw_lookml = """
      view: aview {
        derived_table: {
         sql: SELECT * from table ;;
        }

        dimension: memberID {
          type: string
        }
      }
    """
    lookml = get_lookml_from_raw_lookml(raw_lookml, 'aview.view')
    relevant, passed = DataSourceRule().run(lookml)
    assert relevant
    assert passed
    if os.path.exists(lookml.infilepath):
      os.remove(lookml.infilepath)

def test_run4():
    raw_lookml = """
        connection: "datawarehouse"
        include: "*.view.lkml"
        explore: an_explore {
        }
    """
    lookml = get_lookml_from_raw_lookml(raw_lookml, 'amodel.model')
    relevant, passed = DataSourceRule().run(lookml)
    assert not relevant
    assert not passed
    if os.path.exists(lookml.infilepath):
      os.remove(lookml.infilepath)
