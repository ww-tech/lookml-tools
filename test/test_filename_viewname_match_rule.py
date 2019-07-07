import pytest
import os
import json
from lkmltools.linter.rules.filerules.filename_viewname_match_rule import FilenameViewnameMatchRule
from conftest import get_lookml_from_raw_lookml

def test_run():
    raw_lookml = """
      view: aview {
        dimension: memberID {
          type: string
        }
      }
    """
    lookml = get_lookml_from_raw_lookml(raw_lookml, 'junkyname.view')
    relevant, passed = FilenameViewnameMatchRule().run(lookml)
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
    lookml = get_lookml_from_raw_lookml(raw_lookml, 'aview.view')
    relevant, passed = FilenameViewnameMatchRule().run(lookml)
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
    lookml = get_lookml_from_raw_lookml(raw_lookml, 'amodel.model')
    relevant, passed = FilenameViewnameMatchRule().run(lookml)
    assert not relevant
    assert not passed
    if os.path.exists(lookml.infilepath):
      os.remove(lookml.infilepath)
