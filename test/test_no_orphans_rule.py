import os
import json
import glob
import pytest
from lkmltools.linter.rules.otherrules.no_orphans_rule import NoOrphansRule
from lkmltools.lookml import LookML
from conftest import get_json_from_lookml

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
    json_data = get_json_from_lookml(raw_lookml, filename)
    rule = NoOrphansRule(config)
    rule.process_file(json_data)
    d = rule.view_dict
    assert len(d) == 1
    assert 'aview' in d
    assert d['aview'] == filename
    if os.path.exists(filename):
        os.remove(filename)

def test_finish_up():
    config = {
        "parser": "lookml-parser",
        "infile_globs": [
            "test/test_orphans_repo/*.*.lkml"
        ],
        "tmp_file": "test/parsed_lookml.json",
        "rules": {
            "other_rules": [
                {"name": "NoOrphansRule", "run": True}
            ]
        }
    }
    lookml = LookML(config)
    rule = NoOrphansRule(config)
    globstrings = config['infile_globs']
    for globstring in globstrings:
        filepaths = glob.glob(globstring)
        for filepath in filepaths:
            json_data = lookml.get_json_representation(filepath)
            rule.process_file(json_data)
    file_out = rule.finish_up([])
    assert file_out == [{"file": "test/test_orphans_repo/orphan.view.lkml", "rule": rule.name(), "passed": 0}]

    if os.path.exists(config['tmp_file']):
        os.remove(config['tmp_file'])
