import pytest
from lkmltools.updater.definitions_provider_factory import DefinitionsProviderFactory
from lkmltools.updater.csv_definitions_provider import CsvDefinitionsProvider
from lkmltools.updater.sqlite_reader import SQLiteReader

def test_instantiate():
    obj = DefinitionsProviderFactory.instantiate("CsvDefinitionsProvider", {})
    assert isinstance(obj, CsvDefinitionsProvider)

    obj = DefinitionsProviderFactory.instantiate("SQLiteReader", {})
    assert isinstance(obj, SQLiteReader)
