import pytest
import json
import os
from pandas import DataFrame

from lkmltools.updater.lookml_modifier import LookMlModifier
from conftest import get_lookml_from_raw_lookml

@pytest.fixture()
def config():
    with open("test/config.json", 'r') as f:
        config = json.load(f)
    return config

def test_init(config):
    modifier = LookMlModifier(config)
    assert isinstance(modifier.definitions, DataFrame)

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
    #json_data = get_json_from_lookml(raw_lookml)
    modifier = LookMlModifier(config)
    lookml = get_lookml_from_raw_lookml(raw_lookml, 'aview.view')
    desc, has_key = modifier.find_description(lookml, 'dimension', 'city_code')
    assert has_key
    assert desc == """this
    is
    an
    exsiting
    multiline
    description"""

    desc, has_key = modifier.find_description(lookml, 'measure', 'count')
    assert not has_key

    with pytest.raises(Exception) as e:
        desc, has_key = modifier.find_description(lookml, 'dimension', 'xxx')
    assert 'Did not find dimension xxx' in str(e.value)

    with pytest.raises(Exception) as e:
        desc, has_key = modifier.find_description(lookml, 'xxxx', 'city_code')
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
    lookml = get_lookml_from_raw_lookml(raw_lookml, 'aview.view')
    with pytest.raises(Exception) as e:
        desc, has_key = modifier.find_description(lookml, 'xxx', 'xxx')
    assert 'There should only 1 view. We found 2' in str(e.value)

def test_find_description3(config):
    raw_lookml = """
        connection: "datawarehouse"
        include: "*.view.lkml"
        explore: an_explore {
        }
    """
    filename = "test/amodel.model.lkml"
    modifier = LookMlModifier(config)
    lookml = get_lookml_from_raw_lookml(raw_lookml, 'amodel.model')
    with pytest.raises(Exception) as e:
        desc, has_key = modifier.find_description(lookml, 'xxx', 'xxx')
    assert 'Only views are supported. This is type model' in str(e.value)
    if os.path.exists(filename):
        os.remove(filename)

def test_modify(config):
    infile = "test/basic.view.lkml"
    outfile = "test/temp.view.lkml"

    if os.path.exists(outfile):
        os.remove(outfile)

    modifier = LookMlModifier(config)

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

def test_modify2(config):
    config = {
      "definitions": {
          "type": "CsvDefinitionsProvider",
          "filename": "test/definitions_basename.csv"
      },
      "use_basename": True
    }
    modifier = LookMlModifier(config)

    infile = "test/basic.view.lkml"
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
