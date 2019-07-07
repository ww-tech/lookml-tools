import os
import json
import glob
import pytest
from lkmltools.linter.rules.otherrules.no_orphans_rule import NoOrphansRule
from lkmltools.lookml import LookML
from conftest import get_lookml_from_raw_lookml

def test_process_file():
    config = {
        "rules": {
            "other_rules": [
                {"name": "NoOrphansRule", "run": True}
            ]
        }
    }
    raw_lookml = """
      view: aview {
        dimension: dimname {
          type: string
        }
      }
    """
    filename = "test/aview.view.lkml"
    lookml = get_lookml_from_raw_lookml(raw_lookml, 'aview.view')
    rule = NoOrphansRule(config)
    rule.process_lookml(lookml)
    d = rule.view_dict
    assert len(d) == 1
    assert 'aview' in d
    assert d['aview'] == filename
    if os.path.exists(filename):
        os.remove(filename)

def test_finish_up():
    config = {
        "infile_globs": [
            "test/test_orphans_repo/*.*.lkml"
        ],
        "rules": {
            "other_rules": [
                {"name": "NoOrphansRule", "run": True}
            ]
        }
    }
    rule = NoOrphansRule(config)
    globstrings = config['infile_globs']
    for globstring in globstrings:
        filepaths = glob.glob(globstring)
        for filepath in filepaths:
            rule.process_lookml(LookML(filepath))
    file_out = rule.finish_up([])
    assert file_out == [{"file": "test/test_orphans_repo/orphan.view.lkml", "rule": rule.name(), "passed": 0}]
