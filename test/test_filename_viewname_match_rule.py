import pytest
import os
import json
from lkmltools.linter.rules.filerules.filename_viewname_match_rule import FilenameViewnameMatchRule
from conftest import get_json_from_lookml

def test_run():
    raw_lookml = """
      view: aview {
        dimension: memberID {
          type: string
        }
      }
    """
    filename = "test/junkyname.view.lkml"
    json_data = get_json_from_lookml(raw_lookml,filename)
    relevant, passed = FilenameViewnameMatchRule().run(json_data)
    assert relevant
    assert not passed
    if os.path.exists(filename):
      os.remove(filename)

def test_run2():
    raw_lookml = """
      view: aview {
        dimension: memberID {
          type: string
        }
      }
    """
    filename = "test/aview.view.lkml"
    json_data = get_json_from_lookml(raw_lookml, "test/aview.view.lkml")
    rule = FilenameViewnameMatchRule()
    relevant, passed = rule.run(json_data)
    assert relevant
    assert passed
    if os.path.exists(filename):
      os.remove(filename)

def test_run3():
    raw_lookml = """
        connection: "datawarehouse"
        include: "*.view.lkml"
        explore: an_explore {
        }
    """
    filename = "test/amodel.model.lkml"
    json_data = get_json_from_lookml(raw_lookml, filename)
    relevant, passed = FilenameViewnameMatchRule().run(json_data)
    assert not relevant
    assert not passed
    if os.path.exists(filename):
      os.remove(filename)
