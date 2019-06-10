import pytest
import json
import os
from lkmltools.linter.rules.filerules.data_source_rule import DataSourceRule
from conftest import get_1st_dimension, get_1st_measure, get_json_from_lookml

def test_run1():
    raw_lookml = """
      view: aview {
        sql_table_name: bqdw.engagement_score ;;
      }
    """
    json_data = get_json_from_lookml(raw_lookml)
    relevant, passed = DataSourceRule().run(json_data)
    assert relevant
    assert passed

def test_run2():
    raw_lookml = """
      view: aview {
        dimension: memberID {
          type: string
        }
      }
    """
    json_data = get_json_from_lookml(raw_lookml)
    relevant, passed = DataSourceRule().run(json_data)
    assert relevant
    assert not passed

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
    json_data = get_json_from_lookml(raw_lookml)
    relevant, passed = DataSourceRule().run(json_data)
    assert relevant
    assert passed

def test_run4():
    raw_lookml = """
        connection: "datawarehouse"
        include: "*.view.lkml"
        explore: an_explore {
        }
    """
    filename = "test/amodel.model.lkml"
    json_data = get_json_from_lookml(raw_lookml, filename)
    rule = DataSourceRule()
    relevant, passed = rule.run(json_data)
    assert not relevant
    assert not passed
    if os.path.exists(filename):
      os.remove(filename)
