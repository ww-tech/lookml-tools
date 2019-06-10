import pytest
from lkmltools.linter.rules.fieldrules.lexicon_rule import LexiconRule
from conftest import get_1st_dimension, get_1st_measure

def test_run():
    raw_lookml = """
      view: aview {
        dimension: memberID {
          type: string
        }
      }
    """
    dj = get_1st_dimension(raw_lookml)
    relevant, passed = LexiconRule().run(dj)
    assert relevant
    assert passed

def test_run2():
    raw_lookml = """
      view: aview {
        dimension: subscription_stuff {
          type: string
        }
      }
    """
    dj = get_1st_dimension(raw_lookml)
    relevant, passed = LexiconRule().run(dj)
    assert relevant
    assert not passed

def test_run3():
    relevant, passed = LexiconRule().run({})
    assert not relevant
    assert not passed

def test_run4():
    raw_lookml = """
      view: aview {
        dimension: memberID {
          type: string
          description: "blah blah subscription"
        }
      }
    """
    dj = get_1st_dimension(raw_lookml)
    relevant, passed = LexiconRule().run(dj)
    assert relevant
    assert not passed
