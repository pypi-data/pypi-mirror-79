import os
import json
import pandas as pd
import logging

logging.basicConfig(format='%(asctime)s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S', level=logging.INFO)
log = logging.getLogger('misc')


def msg_to_chime(webhook_url, msg):
    '''
    This function uses a webhook to send a message to an Amazon Chime chatroom.
    For help setting up a webhook, refer to the below URL.
    https://amzn.to/2OrIu8D
    '''
    resp = requests.post(
        url = webhook_url,
        headers = {'Content-Type': 'application/json'},
        data = json.dumps(msg))

    log.info('Message status: %s' % resp.status_code)
    return resp.status_code


def clean_dataframe(df, drop_dupes=[], drop_cols=[], str_to_int_cols=[],
    int_cols=[], float_to_percent_cols=[], bool_cols=[], float_cols=[],
    str_cols=[], int_to_str_cols=[], date_cols=[], datetime_cols=[]):
    '''
    Takes a pandas dataframe along with the column names as a list to
    adjust data types. For example, if my dataframe is named my_df, and
    my_df has a column named "age" which is currently a string of numbers
    but you want it to be integers, then you would call this function with:
        new_df = clean_dataframe(my_df, str_to_int_cols=['age'])
    '''

    log.info('Cleaning dataframe...')

    if drop_dupes:
        # drop duplicate rows, keep last
        try:
            df = df.drop_duplicates(subset=drop_dupes, keep='last')
        except:
            pass

    if drop_cols:
        # drop columns
        try:
            df = df.drop(drop_cols, axis=1)
        except:
            pass

    for col in str_to_int_cols:
        # empties become 0
        try:
            df[col] = df[col].replace(',', '', regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].fillna(0).astype('int')
        except:
            continue

    for col in int_cols:
        # empties become 0
        try:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].fillna(0).astype('int')
        except:
            continue

    for col in float_to_percent_cols:
        # empties/NA become '-'
        try:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].apply(lambda x: '{0:.1f}%'.format(x * 100) if pd.notna(x) else '-')
        except:
            continue

    for col in bool_cols:
        # empties become False
        try:
            df[col] = df[col].astype('bool')
        except:
            continue

    for col in float_cols:
        # empties become np.nan
        try:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].replace(0, np.nan).astype('float')
        except:
            continue

    for col in str_cols:
        # empties become ''
        try:
            df[col] = df[col].fillna('').apply(lambda x: str(x).replace('\"', ''))
        except:
            continue

    for col in int_to_str_cols:
        # empties become ''; 0's and trailing decimals become ''
        try:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].fillna(0).astype('int')
            df[col] = df[col].apply(lambda x: str(x)).replace({'^(0)*?(\.)*?(0)*?$': '', '\.(0)*?$': ''}, regex=True)
        except:
            continue

    for col in date_cols:
        # empties become NaT
        try:
            df[col] = df[col].dt.date
        except:
            continue

    for col in datetime_cols:
        # empties become NaT
        try:
            df[col] = df[col].apply(lambda x: x.replace(microsecond=0))
        except:
            continue

    log.info('Finished cleaning dataframe')

    return df
