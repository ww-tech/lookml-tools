'''
    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)
'''
class SimpleBqWriter():
    '''
        Class that writes dataframe to BigQuery directly (i.e. not via GCS).
        This is simple to configure, but it is slower than via GCS and it probably
        mean that you don't have any backups
    '''

    def upload(self, df, config, destination_table, if_exists='append'):
        '''upload a dataframe df to a biquery table directly

        Args:
            df (pandas dataframe): dataframe
            destination_table (str): name of table to write to
            if_exists (str): what to do if table already exists?

        Returns:
            nothing. uploads dasts to BigQuery

        '''
        cfg = config['output']['simple_biquery']
        destination_table = cfg['field_destination_table']
        project_id = cfg['project_id']
        df.to_gbq(destination_table, project_id=project_id, if_exists=if_exists)
