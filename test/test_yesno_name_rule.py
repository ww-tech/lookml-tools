import pytest
from lkmltools.linter.rules.fieldrules.yesno_name_rule import YesNoNameRule
from conftest import get_1st_dimension, get_1st_measure

def test_run():
    raw_lookml = """
      view: aview {
        dimension: active {
          type: yesno
        }
      }
    """
    dj = get_1st_dimension(raw_lookml)
    relevant, passed = YesNoNameRule().run(dj)
    assert relevant
    assert not passed

def test_run2():
    raw_lookml = """
      view: aview {
        dimension: is_active {
          type: yesno
        }
      }
    """
    dj = get_1st_dimension(raw_lookml)
    relevant, passed = YesNoNameRule().run(dj)
    assert relevant
    assert passed

def test_run3():
    raw_lookml = """
      view: aview {
        measure: count {
          type: count
        }
      }
    """
    mj = get_1st_measure(raw_lookml)
    relevant, passed = YesNoNameRule().run(mj)
    assert not relevant
    assert not passed
