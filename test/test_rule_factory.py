import pytest
from lkmltools.linter.rule_factory import RuleFactory
from lkmltools.linter.rules.fieldrules.all_caps_rule import AllCapsRule

from lkmltools.linter.field_rule import FieldRule
from lkmltools.lookml_field import LookMLField

def test_instantiate():
    obj = RuleFactory().instantiate("AllCapsRule")
    assert isinstance(obj, AllCapsRule)

def test_register():
    rf = RuleFactory()
    class TestRule(FieldRule):
        def run(self, lookml_field):
            return True, True

    assert not rf.is_registered('TestRule')

    rf.register('TestRule', TestRule)

    assert rf.is_registered('TestRule')

    obj = rf.instantiate('TestRule')

    assert isinstance(obj, TestRule)

    rf.unregister('TestRule')

    assert not rf.is_registered('TestRule')

    with pytest.raises(Exception) as e:
        rf.unregister('TestRule')
    assert " Key not found TestRule" in str(e)