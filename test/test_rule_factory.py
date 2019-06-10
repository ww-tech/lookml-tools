import pytest
from lkmltools.linter.rule_factory import RuleFactory
from lkmltools.linter.rules.fieldrules.all_caps_rule import AllCapsRule

def test_instantiate():
    obj = RuleFactory.instantiate("AllCapsRule")
    assert isinstance(obj, AllCapsRule)