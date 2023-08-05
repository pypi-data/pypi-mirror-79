from requests_ntlm import HttpNtlmAuth
from datetime import datetime, date
import os
import re
import s3fs
import json
import requests
import pandas as pd
import numpy as np
import tempfile
import logging
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(format='%(asctime)s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S', level=logging.INFO)
log = logging.getLogger('sharepoint')


def sharepoint_to_dfs(base_url, site, domain, sp_folder, sp_filename,
    sp_filename_startswith, sheet_names, env_user_var='USER', env_pw_var='PW'):

    '''
    This is a very particular function. As arguments, it takes (among others)
        the name of an excel file that lives in SharePoint, and returns a
        dictionary of pandas dataframes for a the specified tabs within that
        file (sheet_names). For example, if a file exists in SharePoint named
        mydata.xlsx, and had tabs 'Sheet1' and 'Sheet2', this function would
        return a dictionary similar to this:

        {
            'Sheet1': <df for Sheet1>,
            'Sheet2': <df for Sheet2>
        }

    Variables are as follows:

        base_url        This is the first part of the SharePoint URL up to and
                            including "sites".
                            Example: 'https://share.microsoft.com/sites'

        site            Can find this in the URL when you're on SharePoint; it comes
                            after "sites/".
                            https://share.com/sites/<site>. Example: 'mysite'

        domain          Domain?

        sp_folder       The full path to which you want to save the file.
                            Example: "Shared Documents/My Test Folder"
                            Example: "Shared Documents/Team Reports"

        sp_filename     The name of the .xlsx file that holds the tabs you want
                            as Pandas DataFrames.
                            Example: 'mydata_20191021.xlsx'

        sp_filename_startswith     If this is a filename that changes frequently,
                            for example if it ends in the date of upload
                            (i.e. 20191021.xlsx), then you can use this variable.
                            It will search for the first file that starts with
                            the string specified here.
                                Example: 'mydata'

        sheet_names     A list of sheet names that exist in the file (sp_filename).
                            Example: ['Sheet1', 'Sheet2']

        env_user_var    The name of the environment variable that holds your username.
                            Example: 'USER'

        env_pw_var      The name of the environment variable that holds your password.
                            Example: 'PASSWORD'

    '''

    def get_df_dict(sheet_names, temp):
        # get dfs for each tab
        df_dict = {}
        for sheet in sheet_names:
            try:
                df = pd.read_excel(temp.name, sheet_name=sheet)
                df_dict[sheet] = df
                log.info('Successfully created df for sheet: %s' % sheet)
            except Exception as e:
                log.error('Error with sheet %s: %s' % (sheet, e))
                df_dict[sheet] = pd.DataFrame()

        return df_dict

    # create temp file - the SharePoint file will be written to this
    temp = tempfile.NamedTemporaryFile(suffix='.xlsx')

    # authentication
    try:
        auth = HttpNtlmAuth(domain + '\\' + os.environ[env_user_var], os.environ[env_pw_var])
    except Exception as e:
        log.error(e)
        return get_df_dict(sheet_names, temp)


    # create URL to query
    api_url = os.path.join(base_url, site, '_api')
    url = "{0}/web/GetFolderByServerRelativeUrl('/sites/{1}/{2}')/Files".format(
        api_url, site, sp_folder
    )

    # make request
    try:
        headers = {'accept': 'application/json;odata=verbose'}
        req = requests.get(url, auth=auth, verify=False, headers=headers)
        files_dict = json.loads(req.text)
    except Exception as e:
        log.error('Request to root URL (%s) failed: %s' % (url, e))
        return get_df_dict(sheet_names, temp)

    # iterate over all files in folder, find URL of target file
    for f in files_dict['d']['results']:
        if sp_filename_startswith:
            if f['Name'].startswith(sp_filename_startswith):
                file_url = f['__metadata']['uri'] + '/$value'
                break
        else:
            if f['Name'] == sp_filename:
                file_url = f['__metadata']['uri'] + '/$value'
                break

    # if file not found above, file_url will be undefined
    try:
        file_url
    except NameError:
        log.error('File %s not found in folder' % sp_filename)
        return get_df_dict(sheet_names, temp)
    else:
        file = requests.get(file_url, auth=auth, verify=False).content


    # write actual file locally
    with open(temp.name, 'wb') as _f:
        _f.write(file)

    # get dfs for each tab
    df_dict = get_df_dict(sheet_names, temp)

    # remove/close temp file
    temp.close()

    return df_dict







def sync_s3_sharepoint(s3_path, sp_base_url, sp_site, sp_folder, sp_domain,
    aws_access_key_id='AWS_ACCESS_KEY_ID',
    aws_secret_access_key='AWS_SECRET_ACCESS_KEY',
    env_user_var='USER',
    env_pw_var='PW',
    s3_to_sp = True,
    sp_to_s3 = True,
    overwrite_s3 = True,
    overwrite_sp = True):

    s3 = s3fs.S3FileSystem(
        anon=False,
        key=os.environ[aws_access_key_id],
        secret=os.environ[aws_secret_access_key]
    )

    log.info('Getting all files in s3://%s...' % s3_path)
    s3_filenames = []
    for file in s3.ls(os.path.join('s3://', s3_path)):
        fname = re.search('[a-zA-Z0-9\\_\\.\\s\\-]+$', file)
        try:
            log.info('--Adding %s' % fname.group())
            s3_filenames.append(fname.group())
        except Exception as e:
            continue


    log.info('Getting all files in SharePoint: %s/%s' % (sp_site, sp_folder))

    headers = {'accept': 'application/json;odata=verbose'}
    auth = HttpNtlmAuth(sp_domain + '\\' + os.environ[env_user_var], os.environ[env_pw_var])

    api_url = os.path.join(sp_base_url, sp_site, '_api')
    url = "{0}/web/GetFolderByServerRelativeUrl('/sites/{1}/{2}')/Files".format(
        api_url, sp_site, sp_folder)

    req = requests.get(url, auth=auth, verify=False, headers=headers)
    files_dict = json.loads(req.text)

    sp_filenames = []
    for i in files_dict['d']['results']:
        log.info('--Adding %s' % i['Name'])
        if not i['Name'].startswith('s3_'):
            sp_filenames.append(i['Name'])


    if not overwrite_sp:
        log.info('Getting only S3 files NOT in SharePoint...')
        s3_filenames = np.setdiff1d(
            s3_filenames,
            sp_filenames,
            assume_unique=True).tolist()

    if not overwrite_s3:
        log.info('Getting only SharePoint files NOT in S3...')
        sp_filenames = np.setdiff1d(
            sp_filenames,
            s3_filenames,
            assume_unique=True).tolist()


    if sp_to_s3:
        for f in sp_filenames:
            log.info('Copying file from SharePoint to S3: %s' % f)

            # download from SharePoint
            filepath = download_from_sharepoint(
                sp_base_url = sp_base_url,
                sp_site = sp_site,
                sp_folder = sp_folder,
                sp_filename = f,
                sp_auth = auth
            )

            # upload to S3
            s3.put(filepath.name, os.path.join('s3://', s3_path, f))
            filepath.close()

    if s3_to_sp:
        for f in s3_filenames:
            log.info('Copying file from S3 to SharePoint: %s' % f)

            # download from S3
            s3.get(os.path.join('s3://', s3_path, f), f)

            # upload to SharePoint
            upload_to_sharepoint(
                sp_base_url = sp_base_url,
                sp_site = sp_site,
                sp_folder = sp_folder,
                sp_domain = sp_domain,
                local_fp = f,
                save_as_filename = 's3_' + str(f),
                env_user_var = env_user_var,
                env_pw_var = env_pw_var
            )

    return True


def download_from_sharepoint(sp_base_url, sp_site, sp_folder, sp_filename, sp_auth):
    log.info('Downloading %s from SharePoint...' % sp_filename)

    # build URL
    api_url = os.path.join(sp_base_url, sp_site, '_api')

    # get URL for file download
    url = "{0}/web/GetFileByServerRelativeUrl('/sites/{1}/{2}/{3}')/$value".format(
        api_url, sp_site, sp_folder, sp_filename)

    try:
        file = requests.get(url, auth=sp_auth, verify=False).content
    except Exception as e:
        log.error('Request to SharePoint failed: %s' % e)

    filepath = tempfile.NamedTemporaryFile()

    # write file locally
    filepath.write(file)

    return filepath



def upload_to_s3(filepath, s3_path):
    log.info('Writing file to S3...')
    try:
        s3.put(filepath, s3_path)
        log.info('--successfully wrote to S3!')
        return True
    except Exception as e:
        log.error(e)
        return False





def upload_to_sharepoint(sp_base_url, sp_site, sp_folder, sp_domain, local_fp,
    save_as_filename, env_user_var='USER', env_pw_var='PW'):

    '''
        sp_base_url    This is the first part of the SharePoint URL up to and
                        including "sites/".
                        Example: 'https://share.microsoft.com/sites'

        sp_site        Can find this in the URL when you're on SharePoint; it
                        comes after "sites/".
                        https://share.com/sites/<site>. Example: 'mysite/'

        local_fp    The full path of the file on your local machine that will be
                        uploaded to SharePoint, including filename.
                        Example: '/Users/harroort/Desktop/myfile.txt'

        sp_folder   The full path to which you want to save the file.
                        Example: "Shared Documents/My Test Folder"
                        Example: "Shared Documents/Team Reports"

        save_as_filename    The name as you want it to appear on SharePoint once
                                uploaded.
                                Example: 'myfile.txt'

        sp_domain      Domain?

        env_user_var    The name of the environment variable that holds
                            your username.
                            Example: 'USER'

        env_pw_var      The name of the environment variable that holds your
                            password.
                            Example: 'PASSWORD'
    '''

    # build URL
    api_url = os.path.join(sp_base_url, sp_site, '_api')

    # authentication
    auth = HttpNtlmAuth(sp_domain + '\\' + os.environ[env_user_var], os.environ[env_pw_var])


    def get_context_token(sp_site):
        tkn_url = os.path.join(api_url, 'contextinfo')
        headers = {
            'accept': 'application/json;odata=verbose',
            'content-type': 'application/json;odata=verbose',
            'odata': 'verbose',
            'X-RequestForceAuthentication': 'true'
        }
        resp = requests.post(tkn_url, auth=auth, headers=headers, verify=False)
        resp.raise_for_status()
        return resp.json()['d']['GetContextWebInformation']['FormDigestValue']


    url = "{0}/web/GetFolderByServerRelativeUrl('/sites/{1}/{2}')/Files/add(url='{3}',overwrite=true)".format(
        api_url, sp_site, sp_folder, save_as_filename)

    context = get_context_token(sp_site)
    headers = {
        'accept': 'application/json;odata=verbose',
        'content-type': 'application/json;odata=verbose',
        'odata': 'verbose',
        'X-RequestForceAuthentication': 'true',
        'X-RequestDigest': context
    }

    data = open(local_fp, 'rb').read()
    resp = requests.post(url, auth=auth, headers=headers, data=data, verify=False)
    return resp
