import pytest
import json
import os
from lkmltools.linter.rules.filerules.one_view_per_file_rule import OneViewPerFileRule
from conftest import get_lookml_from_raw_lookml

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
    lookml = get_lookml_from_raw_lookml(raw_lookml, 'tmp.view')
    relevant, passed = OneViewPerFileRule().run(lookml)
    assert relevant
    assert not passed
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
    lookml = get_lookml_from_raw_lookml(raw_lookml, 'tmp.view')
    relevant, passed = OneViewPerFileRule().run(lookml)  
    assert relevant
    assert passed
    if os.path.exists(lookml.infilepath):
      os.remove(lookml.infilepath)

def test_run3():
    raw_lookml = """
        connection: "datawarehouse"
        include: "*.view.lkml"
        explore: an_explore {
        }
    """
    lookml = get_lookml_from_raw_lookml(raw_lookml, 'tmp.model')
    relevant, passed = OneViewPerFileRule().run(lookml)    
    assert not relevant
    assert not passed
    if os.path.exists(lookml.infilepath):
      os.remove(lookml.infilepath)
