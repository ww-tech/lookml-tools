import pytest
from lkmltools.linter.rules.fieldrules.drill_down_rule import DrillDownRule
from conftest import get_1st_dimension, get_1st_measure

def test_run():
    raw_lookml = """
      view: aview {
        measure: count {
          type: count
          drill_fields: []
        }
      }
    """
    mj = get_1st_measure(raw_lookml)
    relevant, passed = DrillDownRule().run(mj)
    assert relevant
    assert not passed

def test_run2():
    raw_lookml = """
      view: aview {
        measure: count {
          type: count
        }
      }
    """
    mj = get_1st_measure(raw_lookml)
    relevant, passed = DrillDownRule().run(mj)
    assert relevant
    assert not passed

def test_run3():
    raw_lookml = """
      view: aview {
        measure: count {
          type: count
          drill_fields: ["year_name",
            "quarter_name",
            "day_name",
            "month_name"]
        }
      }
    """
    mj = get_1st_measure(raw_lookml)
    relevant, passed = DrillDownRule().run(mj)
    assert relevant
    assert passed

def test_run4():
  #this has a hanging comma in list which lkml parser should handle
    raw_lookml = """
      view: aview {
        measure: count {
          type: count
          drill_fields: ["year_name",
            "quarter_name",
            "day_name",
            "month_name",
            ]
        }
      }
    """
    mj = get_1st_measure(raw_lookml)
    relevant, passed = DrillDownRule().run(mj)
    assert relevant
    assert passed

def test_run5():
    raw_lookml = """
      view: aview {
        dimension: memberID {
          type: string
        }
      }
    """
    dj = get_1st_dimension(raw_lookml)
    relevant, passed = DrillDownRule().run(dj)
    assert not relevant
    assert not passed