import pytest
from lkmltools.linter.rules.fieldrules.count_name_rule import CountNameRule
from conftest import get_1st_measure, get_1st_dimension

def test_run():
    raw_lookml = """
      view: aview {
        measure: row_count {
          type: count
        }
      }
    """
    mj = get_1st_measure(raw_lookml)
    relevant, passed = CountNameRule().run(mj)
    assert relevant
    assert passed

def test_run2():
    raw_lookml = """
      view: aview {
        measure: count {
          type: count
        }
      }
    """
    mj = get_1st_measure(raw_lookml)
    relevant, passed = CountNameRule().run(mj)
    assert relevant
    assert not passed

def test_run3():
    raw_lookml = """
      view: aview {
        dimension: memberID {
          type: string
        }
      }
    """
    md = get_1st_dimension(raw_lookml)
    relevant, passed = CountNameRule().run(md)
    assert not relevant
    assert not passed