import os
import json
import pytest
from pandas import DataFrame
from lkmltools.linter.lookml_linter import LookMlLinter
from lkmltools.linter.rules.filerules.data_source_rule import DataSourceRule
from lkmltools.linter.rules.filerules.filename_viewname_match_rule import FilenameViewnameMatchRule
from lkmltools.linter.rules.fieldrules.description_rule import DescriptionRule
from lkmltools.lookml import LookML
from conftest import get_1st_dimension, get_json_from_lookml
from lkmltools.bq_writer import BqWriter 

def test_initialize_rules():
    config = {
        "rules": {
            "file_level_rules" : [
                {"name": "DataSourceRule", "run": True},
                {"name": "OneViewPerFileRule", "run": False},
                {"name": "FilenameViewnameMatchRule", "run": True}
            ],
            "field_level_rules": [
                {"name": "DescriptionRule", "run": True},
                {"name": "DrillDownRule", "run": False},
            ]
        },
    }
    linter = LookMlLinter(config)
    file_rules = linter.file_rules
    field_rules = linter.field_rules
    assert len(file_rules) == 2
    assert len(field_rules) == 1
    assert isinstance(file_rules[0], DataSourceRule)
    assert isinstance(file_rules[1], FilenameViewnameMatchRule)
    assert isinstance(field_rules[0], DescriptionRule)

def test_run_file_rules():
    config = {
        "rules": {
            "file_level_rules" : [
                {"name": "DataSourceRule", "run": True},
                {"name": "OneViewPerFileRule", "run": False},
                {"name": "FilenameViewnameMatchRule", "run": True}
            ]
        },
    }
    linter = LookMlLinter(config)

    rule = DataSourceRule()
    lookml = LookML("test/minimal_multiline.view.lkml")
    out = linter.run_file_rules(lookml, "xxx", [])
    assert len(out) == 2
    assert out[0] == {'file': 'xxx', 'passed': 1, 'rule': 'DataSourceRule'}
    assert out[1] == {'file': 'xxx', 'passed': 0, 'rule': 'FilenameViewnameMatchRule'}

def test_run_field_rules():
    config = {
        "rules": {
            "field_level_rules": [
                {"name": "DescriptionRule", "run": True},
                {"name": "YesNoNameRule", "run": True},
            ]
        },
    }
    linter = LookMlLinter(config)
    lookml = LookML("test/minimal_multiline.view.lkml")
    v = lookml.views()[0]

    print("v",v)

    out = linter.run_field_rules(v, 'dimension', 'dimensions', "xxx", [])
    assert out[0] == {'file': 'xxx', 'rule': 'DescriptionRule', 'passed': 1, 'type': 'dimension', 'fieldname': 'city_code'}

def test_run_field_rules2():
    config = {
        "rules": {
            "field_level_rules": [
                {"name": "DescriptionRule", "run": True},
                {"name": "YesNoNameRule", "run": True},
            ]
        },
    }
    linter = LookMlLinter(config)

    raw_lookml = """
      view: engagement_score {
      }
    """
    json_data = get_json_from_lookml(raw_lookml)
    v = json_data['views'][0]
    out = linter.run_field_rules(v, 'dimension', 'dimensions', "xxx", [])
    assert out == []

def test_run(monkeypatch):
    config = {
        "git": {
            "url": "https://github.com/exampleorg/examplerepo.git",
            "folder": "gitrepo"
        },

        "infile_globs": [
            "test/test_linter.view.lkml"
        ],

        "rules": {
            "file_level_rules" : [
                {"name": "FilenameViewnameMatchRule", "run": True}
            ],
            "field_level_rules": [
                {"name": "DescriptionRule", "run": True},
                {"name": "YesNoNameRule", "run": True},
            ]
        },

        "output": {
            "csv":{
                "file_output": "test/linter_file_report.csv",
                "field_output": "test/linter_field_report.csv"
            },
            "simple_biquery": {
                "project_id": "some_project",
                "file_destination_table": "some_dataset.lookml_linter_file_report",
                "field_destination_table": "some_dataset.lookml_linter_field_rep"
            },
            "bigquery": {
                "target_bucket_name": "some_bucket",
                "bucket_folder": "some_folder",
                "gcs_project_id": "some_project",
                "project_id": "some_data_lake",
                "dataset": "some_dataset",
                "file_destination_table": "lookml_linter_file_report",
                "field_destination_table": "lookml_linter_field_report"
            }
        }
    }

    def do_nothing(*args, **kwargs): #destination_table, project_id, if_exists):
        pass
    monkeypatch.setattr(DataFrame, 'to_gbq', do_nothing)
    monkeypatch.setattr(BqWriter, 'upload', do_nothing)

    if os.path.exists(config['output']['csv']['file_output']):
        os.remove(config['output']['csv']['file_output'])
    if os.path.exists(config['output']['csv']['field_output']):
        os.remove(config['output']['csv']['field_output'])

    linter = LookMlLinter(config)
    linter.run()

    lines = open(config['output']['csv']['file_output'], 'r').readlines()
    assert lines[0] == "time,file,rule,passed,repo,glob\n"
    # we are using in here as 1st col is current time and I decided it wasnt worth mocking for the test
    assert "test_linter.view.lkml,FilenameViewnameMatchRule,0,https://github.com/exampleorg/examplerepo.git,test/test_linter.view.lkml\n" in lines[1]

    lines = open(config['output']['csv']['field_output'], 'r').readlines()
    assert lines[0] == 'time,file,rule,type,fieldname,passed,repo,glob\n'
    assert 'test_linter.view.lkml,DescriptionRule,dimension,city_code,1,https://github.com/exampleorg/examplerepo.git,test/test_linter.view.lkml\n' in lines[1]
    assert 'test_linter.view.lkml,DescriptionRule,dimension_group,current_week_start,0,https://github.com/exampleorg/examplerepo.git,test/test_linter.view.lkml\n' in lines[2]
    assert 'test_linter.view.lkml,DescriptionRule,measure,count,0,https://github.com/exampleorg/examplerepo.git,test/test_linter.view.lkml\n' in lines[3]

    if os.path.exists(config['output']['csv']['file_output']):
        os.remove(config['output']['csv']['file_output'])
    if os.path.exists(config['output']['csv']['field_output']):
        os.remove(config['output']['csv']['field_output'])

def test_other_rules_to_run():
    config = {
        "rules": {
            "other_rules": [
                {"name":"a", "run":True},
                {"name":"b", "run":False},
                {"name":"c", "run":True},
            ]
        }
    }
    linter = LookMlLinter(config)
    rules = linter.other_rules_to_run()
    assert len(rules) == 2
    assert "a" in rules
    assert "c" in rules

def test_run_orphans():
    config = {
        "git": {
            "url": "https://github.com/exampleorg/examplerepo.git"
        },
        "infile_globs": [
            "test/test_orphans_repo/*.*.lkml"
        ],
        "rules": {
            "other_rules": [
                {"name": "NoOrphansRule", "run": True}
            ]
        },
        "output":{}
    }
    linter = LookMlLinter(config)
    file_out, field_out = linter.run()

    assert len(file_out) == 1
    assert len(field_out) == 0
    assert file_out[0] == {'file': 'test/test_orphans_repo/orphan.view.lkml','passed': 0,'rule': 'NoOrphansRule'}
