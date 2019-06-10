import pytest
import json
import os
from pandas import DataFrame

from lkmltools.updater.lookml_modifier import LookMlModifier
from conftest import *

@pytest.fixture()
def config():
    with open("test/config.json", 'r') as f:
        config = json.load(f)
    return config

def test_init(config):
    modifier = LookMlModifier(config)
    assert isinstance(modifier.definitions, DataFrame)

def test_create_command(config):
    modifier = LookMlModifier(config)
    command = modifier.create_command("somefile.lkml")
    assert isinstance(command, list)
    assert "somefile.lkml" in command[1]
    assert config['parser'] in command[0]

def test_find_description(config):
    raw_lookml = """
view: dim_geography {
 sql_table_name: `BQDW.DimGeography` ;;

  dimension: city_code {
    type: string
    description: "this
    is
    an
    exsiting
    multiline
    description"
    sql: ${TABLE}.CityCode ;;
  }

  measure: count {
    type: count
    drill_fields: [detail*]
  }
}
    """
    json_data = get_json_from_lookml(raw_lookml)
    modifier = LookMlModifier(config)
    desc, has_key = modifier.find_description(json_data, 'dimension', 'city_code')
    assert has_key
    assert desc == """this
    is
    an
    exsiting
    multiline
    description"""

    desc, has_key = modifier.find_description(json_data, 'measure', 'count')
    assert not has_key

    with pytest.raises(Exception) as e:
        desc, has_key = modifier.find_description(json_data, 'dimension', 'xxx')
    assert 'Did not find dimension xxx' in str(e.value)

    with pytest.raises(Exception) as e:
        desc, has_key = modifier.find_description(json_data, 'xxxx', 'city_code')
    assert 'Unrecognized header_type xxx' in str(e.value)

def test_find_description2(config):
    modifier = LookMlModifier(config)
    raw_lookml = """
      view: first_view {
        dimension: memberID {
          type: string
        }
      }

      view: second_view {
        dimension: memberID {
          type: string
        }
      }
    """
    json_data = get_json_from_lookml(raw_lookml)
    with pytest.raises(Exception) as e:
        desc, has_key = modifier.find_description(json_data, 'xxx', 'xxx')
    assert 'There should only 1 view. We found 2' in str(e.value)

def test_find_description3(config):
    modifier = LookMlModifier(config)
    raw_lookml = """
        connection: "datawarehouse"
        include: "*.view.lkml"
        explore: an_explore {
        }
    """
    filename = "test/amodel.model.lkml"
    json_data = get_json_from_lookml(raw_lookml, filename)
    with pytest.raises(Exception) as e:
        desc, has_key = modifier.find_description(json_data, 'xxx', 'xxx')
    assert 'Only views are supported. Is this a LookML model?' in str(e.value)
    if os.path.exists(filename):
        os.remove(filename)

def test_get_json_representation(config):
    modifier = LookMlModifier(config)
    json_data = modifier.get_json_representation("test/minimal_multiline.lkml")
    assert isinstance(json_data, dict)

    ## this tests whether the installed lookml-parser is working the same manner
    ## as when this code was being developed
    ## /usr/local/bin/lookml-parser --input='test/minimal_multiline.lkml' --whitespace=2 > test/parsed_minimal_multiline_lookml.json
    with open("test/parsed_minimal_multiline_lookml.json", 'r') as f:
        json_data2 = json.load(f)

    assert json_data == json_data2

    if os.path.exists(config['tmp_file']):
        os.remove(config['tmp_file'])

def test_get_json_representation2(config):
    modifier = LookMlModifier(config)
    with pytest.raises(Exception) as e:
        json_data = modifier.get_json_representation("doesnotexist.lkml")
    assert 'Filename does not exist: doesnotexist.lkml' in str(e.value)
    if os.path.exists(config['tmp_file']):
        os.remove(config['tmp_file'])

def test_get_json_representation3(config):
    config['parser'] = 'binarythatdoesnotexist'
    modifier = LookMlModifier(config)
    with pytest.raises(Exception) as e:
        json_data = modifier.get_json_representation("test/minimal_multiline.lkml")
    assert "No such file or directory: 'binarythatdoesnotexist'" in str(e.value)
    if os.path.exists(config['tmp_file']):
        os.remove(config['tmp_file'])

def test_modify(config):
    modifier = LookMlModifier(config)

    infile = "test/basic.lkml"
    outfile = "test/temp.lkml"

    if os.path.exists(outfile):
        os.remove(outfile)

    modifier.modify(infile, outfile)

    assert os.path.exists(outfile)

    inlines = open(infile, 'r').readlines()
    outlines = open(outfile, 'r').readlines()

    assert len(inlines) == 45
    assert len(outlines) == 46

    assert inlines[22].strip() == 'description: "this'
    assert outlines[27].strip() == 'description: "this is a new description"	# programmatically added by LookML modifier'

    assert inlines[10].strip() == "type: string"
    assert outlines[10].strip() == "description: \"This"
    assert outlines[11].strip() == "is"
    assert outlines[12].strip() == "the"
    assert outlines[13].strip() == "correct"
    assert outlines[14].strip() == "description\"	# programmatically added by LookML modifier"

    if os.path.exists(outfile):
        os.remove(outfile)
    if os.path.exists(config['tmp_file']):
        os.remove(config['tmp_file'])

def test_modify2(config):
    config = {
      "parser": "lookml-parser",
      "tmp_file": "test/parsed_lookml.json",
      "definitions": {
          "type": "CsvDefinitionsProvider",
          "filename": "test/definitions_basename.csv"
      },
      "use_basename": True
    }
    modifier = LookMlModifier(config)

    infile = "test/basic.lkml"
    outfile = "test/temp.lkml"

    if os.path.exists(outfile):
        os.remove(outfile)

    modifier.modify(infile, outfile)

    assert os.path.exists(outfile)

    inlines = open(infile, 'r').readlines()
    outlines = open(outfile, 'r').readlines()

    assert len(inlines) == 45
    assert len(outlines) == 46

    assert inlines[22].strip() == 'description: "this'
    assert outlines[27].strip() == 'description: "this is a new description"	# programmatically added by LookML modifier'

    assert inlines[10].strip() == "type: string"
    assert outlines[10].strip() == "description: \"This"
    assert outlines[11].strip() == "is"
    assert outlines[12].strip() == "the"
    assert outlines[13].strip() == "correct"
    assert outlines[14].strip() == "description\"	# programmatically added by LookML modifier"

    if os.path.exists(outfile):
        os.remove(outfile)
    if os.path.exists(config['tmp_file']):
        os.remove(config['tmp_file'])
