import psycopg2
import pandas as pd

class LookmlFieldUsageProvider():

    def __init__(self):
        self.engine = psycopg2.connect(
                        dbname='peloton',
                        host='localhost',
                        port=5439
                        )

    def get_field_usage(self, df):
        fields_to_check = df['full_fieldname'].tolist()
        query_template = """
            WITH fields as (
                SELECT
                    CASE WHEN
                        reverse(split_part(reverse(field),'_',1)) IN ('time', 'date', 'week', 'month', 'quarter', 'year')
                        THEN REPLACE(field, '_' + reverse(split_part(reverse(field),'_',1)), '')
                        ELSE field
                    END as full_fieldname,
                    COUNT(*) as usage_count
                FROM abyrne_schema.looker_field_usage
                GROUP BY 1
            )
            SELECT
                full_fieldname,
                usage_count
            FROM fields
            WHERE full_fieldname IN {}
        """
        query = query_template.format(tuple(fields_to_check))
        df_field_usage = pd.read_sql(query, con=self.engine, index_col=['full_fieldname'])
        return df.join(df_field_usage, on='full_fieldname')
