
import pytest
import os
from lkmltools.lookml import LookML

@pytest.fixture(scope="module")
def get_json_from_lookml(raw_lookml, user_defined_filename=None):
    filename = "test/tmp.view.lkml"
    if user_defined_filename:
        filename = user_defined_filename

    with open(filename, "w") as text_file:
        text_file.write(raw_lookml)

    config = {
        "parser": "lookml-parser",
        "tmp_file": "test/parsed_lookml.json"
    }

    lookml = LookML(config)

    json_data = lookml.get_json_representation(filename)
    teardown(filename)
    teardown(config['tmp_file'])
    return json_data

@pytest.fixture(scope="module")
def get_1st_dimension(raw_lookml):
    json_data = get_json_from_lookml(raw_lookml)
    j = json_data['files'][0]['views'][0]['dimensions'][0]
    return j

@pytest.fixture(scope="module")
def get_1st_measure(raw_lookml):
    json_data = get_json_from_lookml(raw_lookml)
    m = json_data['files'][0]['views'][0]['measures'][0]
    return m

@pytest.fixture(scope="module")
def teardown(filename):
    if os.path.exists(filename):
        os.remove(filename)
