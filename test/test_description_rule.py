import pytest
from lkmltools.linter.rules.fieldrules.description_rule import DescriptionRule
from conftest import get_1st_dimension, get_1st_measure
from lkmltools.lookml_field import LookMLField
def test_run():
    raw_lookml = """
      view: aview {
        dimension: memberID {
          type: string
          description: "I'm a description"
        }
      }
    """
    dj = get_1st_dimension(raw_lookml)
    relevant, passed = DescriptionRule().run(dj)
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
    dj = get_1st_dimension(raw_lookml)
    relevant, passed = DescriptionRule().run(dj)
    assert relevant
    assert not passed

def test_run3():
    raw_lookml = """
      view: aview {
        dimension: memberID {
          type: string
          description: ""
        }
      }
    """
    dj = get_1st_dimension(raw_lookml)
    relevant, passed = DescriptionRule().run(dj)
    assert relevant
    assert not passed

def test_run4():
    relevant, passed = DescriptionRule().run(LookMLField({'_type': 'junk'}))
    assert not relevant
    assert not passed
