
import pytest
import os
import pandas as pd
from lkmltools.bq_writer import BqWriter
from google.cloud.storage.blob import Blob
from google.cloud.bigquery.job import WriteDisposition
from google.cloud.bigquery.job import LoadJobConfig

def test_write_to_csv():
    writer = BqWriter()
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

    target_bucket_name = "tmp_bucket"
    bucket_folder = "tmp_bucket"
    expected_filename  =  target_bucket_name + os.sep + bucket_folder + os.sep + BqWriter.FILENAME

    if os.path.exists(expected_filename):
        os.remove(expected_filename)

    filename = writer._write_to_csv(df, target_bucket_name,bucket_folder, local_filename=None)
    assert filename == target_bucket_name + os.sep + bucket_folder + os.sep + BqWriter.FILENAME
    assert os.path.exists(filename)

    if os.path.exists(expected_filename):
        os.remove(expected_filename)

def test_write_to_csv2():
    writer = BqWriter()
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    local_filepath = "some/path/to/file"
    filename = writer._write_to_csv(df, target_bucket_name=None,bucket_folder=None, local_filename=local_filepath)
    assert filename == local_filepath

def test__create_job_config():
    writer = BqWriter()
    wd = WriteDisposition.WRITE_TRUNCATE
    config = writer._create_job_config(WriteDisposition.WRITE_TRUNCATE)
    assert isinstance(config, LoadJobConfig)
    assert config.write_disposition == wd

def test_upload(monkeypatch):
    writer = BqWriter()
    def mock_upload_to_bq(*args, **kwargs):
        pass
    monkeypatch.setattr(writer, 'upload_to_bq', mock_upload_to_bq)

    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

    config = {
        "output": {
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
    writer.upload(df, config, "file_destination_table")

#def test__upload_to_gcs(monkeypatch):
#    def mock_upload_from_filename(*args, **kwargs):
#        pass
#    monkeypatch.setattr(Blob, 'upload_from_filename', mock_upload_from_filename)
#
#    writer = BqWriter()
#    gcs_project_id = "some_project"
#    target_bucket_name = "some_bucket_name"
#    bucket_folder = "some_bucket_folder"
#    filename = "some_filename"
#    writer._upload_to_gcs(gcs_project_id, target_bucket_name, bucket_folder, filename)
