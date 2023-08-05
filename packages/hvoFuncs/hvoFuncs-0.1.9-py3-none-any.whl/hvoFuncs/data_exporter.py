import csv
import logging
import json
import os
import pprint
from tempfile import TemporaryDirectory
import time
import pathlib
import boto3
import numpy as np
import pandas as pd
import sqlalchemy as sa
from hvoFuncs import misc

logging.basicConfig(format='%(asctime)s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.INFO)
log = logging.getLogger('data_exporter')


class DataExporter:
    """Extract data and send to redshift"""

    def __init__(self, database, data, schema, table, bucket, s3_path,
        del_id=None, date_col=None, null_as='', replace=False, truncate=False,
        del_between_dates=None):

        if data.__class__ is not pd.core.frame.DataFrame:
            raise TypeError("""Data object is: %s'.
                            Object must be dataframe for export!""",
                            str(data.__class__))
        self.database = database
        self.data = data
        self.schema = schema
        self.replace = replace
        self.truncate = truncate
        self.table = table
        self.null_as = null_as

        self.create_tbl = False
        self.bucket = bucket
        self.s3_path = s3_path
        self.del_id = del_id
        self.date_col = date_col
        self.del_between_dates = del_between_dates

        self.aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
        self.aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
        self.con = sa_connection(self.database)

    def create_table(self):
        log.info('Creating sql builder...')
        pd_engine = pd.io.sql.pandasSQL_builder(self.con, schema=self.schema)
        log.info('Defining table schema...')
        pprint.pprint(self.data.columns)
        self.con.engine.execute("""
                                DROP TABLE IF EXISTS {schema}.{table};
                                COMMIT;
                                """.format(table=self.table,
                                           schema=self.schema))

        table = pd.io.sql.SQLTable(name=self.table, frame=self.data,
                                   pandas_sql_engine=pd_engine, index=False)
        log.info('Creating table: %s...', self.table)
        table.create()
        return

    def truncate_table(self):
        log.info('Truncating table before writing...')
        self.con.engine.execute("""
                                TRUNCATE TABLE {schema}.{table};
                                COMMIT;
                                """.format(table=self.table,
                                           schema=self.schema))

        log.info('Truncated table: %s...', self.table)
        return

    def fix_column_names(self):
        """Remove whitespace, punctuation, and capitalization from columns."""
        log.info('Conforming column names...')
        for thing in [' ', '\\n', '/', '.', '(', ')']:
            self.data.columns = [c.replace(thing, '_')
                                 for c in self.data.columns]
        self.data.columns = [c.lower() for c in self.data.columns]

        order = self.get_column_order()

        if self.replace or self.create_tbl:
            return

        for col in order:
            if col not in list(self.data.columns):
                log.warn('Adding blank column for %s', col)
                self.data[col] = None

        self.data = self.data[order]
        return

    def get_column_order(self):
        order = self.con.engine.execute("""SELECT column_name
                                        FROM information_schema.columns
                                        WHERE table_name = '{table}' AND
                                            table_schema = '{schema}'
                                        ORDER BY ordinal_position""".format(
                                        table=self.table, schema=self.schema))
        columns = [o['column_name'] for o in order]
        if len(columns) == 0:
            log.info('Target table does not exist...setting create to True...')
            self.create_tbl = True
            return columns

        # log.info('Column order in db: ')
        # pprint.pprint(columns)
        return columns

    def write_csv_to_s3(self):
        """Write pandas dataframe to s3."""
        log.info('Writing local csv file for %d rows', self.data.shape[0])
        self.data.is_copy = False
        self.data.replace('\n', '', inplace=True, regex=True)
        self.data.replace('\r', '', inplace=True, regex=True)

        cur_time = time.time()
        partitions = 8
        s3_subfolder = '%s.%s_%d' % (self.schema, self.table, cur_time)
        s3_dir = os.path.join(self.s3_path, s3_subfolder)
        partitioned_df = np.array_split(self.data, partitions)

        with TemporaryDirectory() as tmp:

            local_dir = os.path.join(tmp, s3_subfolder)
            try:
                pathlib.Path(local_dir).mkdir(parents=True)
            except FileExistsError:
                log.info('Temporary directory already exists')

            log.info('Uploading partitions to s3 at: %s...' % (s3_dir))

            for i in range(partitions):
                file_name = 'partition_%d.csv.gzip' % (i+1)
                local_csv = os.path.join(local_dir, file_name)
                partitioned_df[i].to_csv(local_csv, sep='|', header=True,
                    index=False, quoting=csv.QUOTE_NONNUMERIC,
                    compression='gzip')

                s3_file = s3_dir + '/' + file_name

                s3_client = boto3.client('s3')
                s3_client.upload_file(local_csv, self.bucket, s3_file)
                log.info('Partition %d uploaded to s3 successfully...' % (i+1))

        return s3_dir

    def copy_to_redshift(self, s3_file):
        """Copy data from s3 to redshift."""
        log.info('Copying data from s3 to redshift...')
        try:
            if not self.replace and not self.create_tbl and not self.truncate:

                if self.del_between_dates is not None:
                    del_between_dates_clause = """
                        DELETE FROM {schema}.{table}
                        WHERE ({date_col} BETWEEN GETDATE()::date - interval '{lag_start} days'
                            AND GETDATE()::date - interval '{lag_end} days')""".format(
                                schema=self.schema, table=self.table,
                                date_col=self.del_between_dates['date_col'],
                                lag_start=self.del_between_dates['lag_start'],
                                lag_end=self.del_between_dates['lag_end'])
                else:
                    del_between_dates_clause = ""

                if self.date_col is not None:
                    where_clause = """AND
                    {table}.{date_col} = tmp_{table}.{date_col}
                    """.format(date_col=self.date_col, table=self.table)
                else:
                    where_clause = ""


                delete_stmt = """
                             DELETE FROM {schema}.{table}
                             USING tmp_{table}
                             WHERE ({table}.{delete_id}=tmp_{table}.{delete_id}
                                {dates_clause})
                             """.format(delete_id=self.del_id,
                                        schema=self.schema,
                                        table=self.table,
                                        dates_clause=where_clause)

                copy_stmt = """
                            BEGIN;
                            CREATE TEMP TABLE tmp_{table} (LIKE {schema}.{table});
                            COPY tmp_{table} FROM 's3://{bucket}/{file_path}'
                            CREDENTIALS 'aws_access_key_id={id};aws_secret_access_key={secret}'
                            REMOVEQUOTES
                            BLANKSASNULL
                            IGNOREHEADER 1
                            {null_as}
                            DELIMITER '|'
                            GZIP;
                            {delete_between_dates};
                            {delete_params};
                            INSERT INTO {schema}.{table} (
                                            SELECT * FROM tmp_{table});
                            DROP TABLE IF EXISTS tmp_{table};
                            COMMIT;
                            """.format(schema=self.schema,
                                       table=self.table,
                                       null_as=self.null_as,
                                       bucket=self.bucket,
                                       file_path=s3_file,
                                       id=self.aws_access_key_id,
                                       secret=self.aws_secret_access_key,
                                       delete_between_dates=del_between_dates_clause,
                                       delete_params=delete_stmt)

            else: # if self.replace OR self.create_tbl OR self.truncate
                copy_stmt = """
                            BEGIN;
                            COPY {schema}.{table} FROM 's3://{bucket}/{file_path}'
                            CREDENTIALS 'aws_access_key_id={id};aws_secret_access_key={secret}'
                            REMOVEQUOTES
                            BLANKSASNULL
                            IGNOREHEADER 1
                            {null_as}
                            DELIMITER '|'
                            GZIP;
                            COMMIT;
                            """.format(schema=self.schema,
                                       table=self.table,
                                       null_as=self.null_as,
                                       bucket=self.bucket,
                                       file_path=s3_file,
                                       id=self.aws_access_key_id,
                                       secret=self.aws_secret_access_key)


            self.con.engine.execute(copy_stmt)
            log.info('Data uploaded successfully!')
        except Exception as e:
            try:
                adjust_schema_def(self.con, self.table, self.data, copy_stmt,
                                  error=e)
            except Exception as e:
                log.error(e)
                log.error('Could not insert data!')
                raise
        return

    def write_dataframe_to_redshift(self):
        """Main method to export to database"""
        if self.data.shape[0] == 0:
            return

        # pprint.pprint(self.data.columns)
        self.fix_column_names()
        self.conform_data_types()
        s3_dir_path = self.write_csv_to_s3()

        if self.replace or self.create_tbl:
            self.create_table()
        elif self.truncate:
            self.truncate_table()
        self.copy_to_redshift(s3_file=s3_dir_path)
        return

    def conform_data_types(self):
        log.info('Conforming data types to types declared in Redshift...')

        # get dictionary of column names and types
        results = self.con.engine.execute("""SELECT column_name, data_type,
                                        character_maximum_length as max_length
                                        FROM information_schema.columns
                                        WHERE table_name = '{table}' AND
                                            table_schema = '{schema}'""".format(
                                        table=self.table, schema=self.schema))
        results_dict = [dict(row) for row in results]

        # conform all values in self.data to the data type declared for that column in Redshift
        db_cols = {row['column_name']: row['data_type'] for row in results_dict}
        self.data = misc.clean_dataframe(
            self.data,
            int_cols = [k for k,v in db_cols.items() if 'int' in v and '_id' not in k],
            bool_cols = [k for k,v in db_cols.items() if 'boolean' in v],
            str_cols = [k for k,v in db_cols.items() if 'char' in v],
            float_cols = [k for k,v in db_cols.items() if 'numeric' in v or 'precision' in v],
            date_cols = [k for k,v in db_cols.items() if 'date' in v and 'time' not in v],
            datetime_cols = [k for k,v in db_cols.items() if 'datetime' in v or 'timestamp' in v])

        # truncate string fields to max length
        for row in results_dict:
            if 'char' in row['data_type'] and row['max_length']:
                try:
                    self.data[row['column_name']] = \
                        self.data[row['column_name']].apply(lambda x: str(x)[:int(row['max_length'])])
                except KeyError:
                    continue

        return



def alter_rs_schema(con, schema, table, column, new_dtype):
    """Alter schema by creating new column, dropping old, and renaming."""
    stmt = """
        ALTER table {schema}.{table} ADD COLUMN new_col {new_dtype};
        UPDATE {schema}.{table} SET new_col = cast({column} as {new_dtype});
        ALTER table {schema}.{table} DROP COLUMN {column};
        ALTER table {schema}.{table} RENAME COLUMN new_col to {column}
        """.format(table=table, new_dtype=new_dtype, column=column,
                   schema=schema)

    print(stmt)
    con.engine.execute(stmt)

    return


def adjust_schema_def(con, schema, table, error, copy_stmt):
    log.warn('Schema error found in database... attempting to reconcile...')
    result = con.engine.execute("""SELECT * FROM stl_load_errors
                                ORDER BY starttime DESC LIMIT 1""")
    result = [r for r in result][0]
    if result['err_reason'].strip() != 'String length exceeds DDL length':
        raise ValueError("Error Inserting data", error)

    line_length = len(str(result['raw_field_value']))
    new_type = 'varchar(%d)' % int(line_length*1.25)
    alter_rs_schema(con, schema, table, result['colname'], new_type)

    log.info('Attempting copy command again...')
    con.engine.execute(copy_stmt)

    return


def cp_to_redshift(con, schema, table, s3_file, delete_stmt='', col_order='',
                   null_as='', access_key=None, secret_key=None):
    """Copy data from s3 to redshift."""
    log.info('Copying data from s3 to redshift...')

    if access_key is None:
        access_key = os.environ['AWS_ACCESS_KEY_ID']
    if secret_key is None:
        secret_key = os.environ['AWS_SECRET_ACCESS_KEY']

    if type(col_order) is list:
        col_order = '(' + ','.join(col_order) + ')'

    try:
        copy_stmt = """
                    BEGIN;
                    CREATE TEMP TABLE tmp_{table} (LIKE {schema}.{table});
                    COPY tmp_{table} FROM '{s3_file}' {col_order}
                    CREDENTIALS 'aws_access_key_id={id};aws_secret_access_key={secret}'
                    REMOVEQUOTES
                    IGNOREHEADER 1
                    BLANKSASNULL
                    {null_as}
                    DELIMITER '|'
                    GZIP;
                    {delete_params}
                    INSERT INTO {schema}.{table} (
                                    SELECT * FROM tmp_{table});
                    DROP TABLE IF EXISTS tmp_{table};
                    COMMIT;
                    """.format(schema=schema,
                               col_order='',
                               table=table,
                               null_as=null_as,
                               s3_file=s3_file,
                               file_path=s3_file,
                               id=access_key,
                               secret=secret_key,
                               delete_params=delete_stmt)

        con.engine.execute(copy_stmt)
        log.info('Data uploaded successfully!')
    except Exception as e:
        try:
            adjust_schema_def(con=con, schema=schema, table=table, error=e,
                              copy_stmt=copy_stmt)
        except Exception as e:
            log.error(e)
            log.error('Could not insert data!')
            raise
    return


def sa_connection(database):
    """Create sqlalchemy connection to database."""
    log.info('Getting dsn for %s', database)
    dsn = 'redshift+psycopg2://{user}:{password}@'\
          '{host}:{port}/{db_name}?sslmode=prefer'.format(
            user = os.environ['RS_USER'],
            password = os.environ['RS_PASSWORD'],
            host = os.environ['RS_HOST'],
            port = os.environ['RS_PORT'],
            db_name = os.environ['RS_DATABASE']
          )

    log.info('Creating sql connection...')
    con = sa.create_engine(dsn)
    return con


def get_column_order_from_s3(file_path):
    """Get current file column order from remote file"""
    log.info('Downloading remote object to get column order...')

    import io
    import boto3
    import gzip

    resource = boto3.resource('s3')

    obj = io.BytesIO()
    file_path = file_path.replace("s3://", "")
    file_path = file_path.split('/')
    bucket = file_path[0]
    s3_path = "/".join(file_path[1:])
    log.info('Requesting file from %s', s3_path)

    resource.meta.client.download_fileobj(bucket, s3_path, obj)
    obj.seek(0)

    data = io.BytesIO()
    data.write(gzip.decompress(obj.getbuffer()))
    data.seek(0)

    all_columns = pd.read_csv(data, sep='|', nrows=0).columns
    return list(all_columns)
