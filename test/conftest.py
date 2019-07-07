
import pytest
import os
from lkmltools.lookml import LookML
from lkmltools.lookml_field import LookMLField

@pytest.fixture(scope="module")
def get_json_from_lookml(raw_lookml, user_defined_filename=None):
    filename = "test/tmp.view.lkml"
    if user_defined_filename:
        filename = user_defined_filename

    with open(filename, "w") as text_file:
        text_file.write(raw_lookml)

    lookml = LookML(filename)

    json_data = lookml.json_data
    teardown(filename)
    return json_data

@pytest.fixture(scope="module")
def get_lookml_from_raw_lookml(raw_lookml, type):
    filename = "test/" + type + ".lkml"
    with open(filename, "w") as text_file:
        text_file.write(raw_lookml)
    lookml = LookML(filename)
    return lookml

@pytest.fixture(scope="module")
def get_1st_dimension(raw_lookml):
    json_data = get_json_from_lookml(raw_lookml)
#    j = json_data['files'][0]['views'][0]['dimensions'][0]
    j = json_data['views'][0]['dimensions'][0]
    j['_type'] = 'dimension'
    return LookMLField(j)

@pytest.fixture(scope="module")
def get_1st_measure(raw_lookml):
    json_data = get_json_from_lookml(raw_lookml)
#    m = json_data['files'][0]['views'][0]['measures'][0]
    m = json_data['views'][0]['measures'][0]
    m['_type'] = 'measure'
    return LookMLField(m)

@pytest.fixture(scope="module")
def teardown(filename):
    if os.path.exists(filename):
        os.remove(filename)
