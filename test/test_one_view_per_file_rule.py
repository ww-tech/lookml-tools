import pytest
import json
import os
from lkmltools.linter.rules.filerules.one_view_per_file_rule import OneViewPerFileRule
from conftest import get_json_from_lookml

def test_run():
    raw_lookml = """
      view: first_view {
        dimension: memberID {
          type: string
        }
      }

      view: second_view {
        dimension: memberID {
          type: string
        }
      }
    """
    json_data = get_json_from_lookml(raw_lookml)
    relevant, passed = OneViewPerFileRule().run(json_data)
    assert relevant
    assert not passed

def test_run2():
    raw_lookml = """
      view: aview {
        dimension: memberID {
          type: string
        }
      }
    """
    json_data = get_json_from_lookml(raw_lookml)
    relevant, passed = OneViewPerFileRule().run(json_data)    
    assert relevant
    assert passed

def test_run3():
    raw_lookml = """
        connection: "datawarehouse"
        include: "*.view.lkml"
        explore: an_explore {
        }
    """
    filename = "test/amodel.model.lkml"
    json_data = get_json_from_lookml(raw_lookml, filename)
    relevant, passed = OneViewPerFileRule().run(json_data)    
    assert not relevant
    assert not passed
    if os.path.exists(filename):
      os.remove(filename)
