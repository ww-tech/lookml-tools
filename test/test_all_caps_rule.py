import pytest
from lkmltools.linter.rules.fieldrules.all_caps_rule import AllCapsRule
from conftest import get_1st_dimension, get_1st_measure
from lkmltools.lookml_field import LookMLField

def test_name():
    # testing on behalf of abstract class
    rule = AllCapsRule()
    assert rule.name() == "AllCapsRule"

def test_run():
    raw_lookml = """
      view: aview {
        dimension: memberID {
          type: string
        }
      }
    """
    dj = get_1st_dimension(raw_lookml)
    relevant, passed = AllCapsRule().run(dj)
    assert relevant
    assert passed

def test_run2():
    raw_lookml = """
      view: aview {
        dimension: SHOUTYNAME {
          type: string
        }
      }
    """
    dj = get_1st_dimension(raw_lookml)
    relevant, passed = AllCapsRule().run(dj)
    assert relevant
    assert not passed

def test_run3():
    relevant, passed = AllCapsRule().run(LookMLField({'_type': 'junk'}))
    assert not relevant
    assert not passed
