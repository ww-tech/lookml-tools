import pytest
from lkmltools.updater.csv_definitions_provider import CsvDefinitionsProvider

def test_get_definitions():
    config = {
        "definitions": {
            "type": "CsvDefinitionsProvider",
            "filename": "test/definitions.csv"
        }
    }
    provider = CsvDefinitionsProvider(config)
    definitions = provider.get_definitions()
    assert definitions.shape[0] == 3
    assert list(definitions.T.to_dict().values())[1] == {"file":"test/basic.view.lkml", "type":"dimension", "name":"tier", "definition":"this is a new description"}

