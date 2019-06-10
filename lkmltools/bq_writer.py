'''
    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)

'''
import os
import logging
import google.cloud.storage as storage
from google.cloud import bigquery
from google.cloud.bigquery.job import WriteDisposition

class BqWriter():
    '''
        Write data to BigQuery via GCS.
    '''

    FILENAME = 'tmp_upload.csv'

    def _write_to_csv(self, dataframe, target_bucket_name, bucket_folder, local_filename=None):
        '''write dataframe to CSV (unless written already and specified in local_filename)

        Args:
            dataframe (pandas dataframe): data to be written, None if local_filename is supplied
            target_bucket_name (str): name of GCS bucket
            bucket_folder (str): name of GCS folder
            local_filename (str): optional, filename of data, if already written out

        Returns:
            filename: filepath of local file daataframe was written to

        '''
        if not local_filename:
            try:
                os.makedirs(os.path.join(target_bucket_name, bucket_folder))
            except OSError:
                pass
            filename = os.path.join(target_bucket_name, bucket_folder, BqWriter.FILENAME)
            dataframe.to_csv(filename, index=False)
            logging.info("data written to %s", filename)
        else:
            filename = local_filename
        return filename

    def _upload_to_gcs(self, gcs_project_id, target_bucket_name, bucket_folder, filename):
        '''upload CSV to file in GCS

        Args:
            gcs_project_id (str): project name
            target_bucket_name (str): name of GCS bucket
            bucket_folder (str): name of GCS folder
            filename (str): filepath to upload

        Returns:
            nothing. Side effect is that data is uploaded to GCS

        '''
        storage_client = storage.Client(gcs_project_id)
        bucket = storage_client.get_bucket(target_bucket_name)
        path = bucket_folder + os.sep + filename
        logging.info("Loading to GCS: %s", path)
        blob = bucket.blob(path) #name in GCS
        blob.upload_from_filename(filename)

    def upload(self, dataframe, config, destination_table_key):
        '''
        Args:
            dataframe (pandas dataframe): dataframe to upload
            config (JSON): JSON configuration
            destination_table_key (str): table to write to

        Returns:
            nothing. upload data to GCS

        '''
        cfg = config['output']['bigquery']
        gcs_project_id = cfg['gcs_project_id']
        project_id = cfg['project_id']
        destination_table = cfg[destination_table_key]
        dataset = cfg['dataset']
        target_bucket_name = cfg['target_bucket_name']
        bucket_folder = cfg['bucket_folder']
        self.upload_to_bq(dataframe, gcs_project_id, project_id, dataset, destination_table, target_bucket_name, \
                    bucket_folder, write_disposition=WriteDisposition.WRITE_APPEND)

    def _create_job_config(self, write_disposition):
        '''create a GCs JobConfiguration

        Args:
            write_disposition (str): JobConfig write disposition (e.g WriteDisposition.WRITE_APPEND)

        Returns:
            job_config (JobConfig): GCS job configuration

        '''
        job_config = bigquery.LoadJobConfig()
        job_config.autodetect = True
        job_config.write_disposition = write_disposition
        job_config.source_format = bigquery.SourceFormat.CSV
        return job_config

    def upload_to_bq(self, dataframe, gcs_project_id, project_id, dataset, tablename, target_bucket_name, bucket_folder, write_disposition=WriteDisposition.WRITE_APPEND):
        '''Write some dataframe to BigQuery via GCS storage. 
            
        Args:
            dataframe (pandas dataframe): data to be written
            gcs_project_id (str): GCS project ID
            target_bucket_name (str): GCS bucket_name
            bucket_folder (str): GCS bucket_folder
            project_id (str): BQ project ID
            dataset (str): BQ dataset
            tablename (str): BQ tablename

        Returns:
            nothing but side effect is to write data to GCS and then to BigQuery

        '''
        filename = self._write_to_csv(dataframe, target_bucket_name, bucket_folder)

        self._upload_to_gcs(gcs_project_id, target_bucket_name, bucket_folder, filename)

        job_config = self._create_job_config(write_disposition)

        # copy from file to table
        bigquery_client = bigquery.Client(project=project_id)
        table_ref = bigquery_client.dataset(dataset).table(tablename)  # to target a partition concat a $date to the

        path = target_bucket_name + os.sep + bucket_folder + os.sep + filename
        logging.info("Loading to %s", path)

        load_job = bigquery_client.load_table_from_uri(
            'gs://{}'.format(path),  # need to make sure this is wildcarded
            table_ref,
            job_config=job_config)  # API request

        load_job.result()  # Waits for table load to complete.
