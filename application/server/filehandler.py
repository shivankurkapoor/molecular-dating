'''
Created by : Shivankur Kapoor
Created on : 12/21/2016
This module contains functions
'''

import errno
import httplib2
import io
import logging
import os
from apiclient import discovery
from apiclient import errors
from apiclient import http
from common.globalconst import *
from common.globalfunct import *
from googleapiclient.discovery import build
from oauth2client.client import Credentials
from oauth2client.client import FlowExchangeError
from oauth2client.client import flow_from_clientsecrets
from server.errorhandler import *
from server.server_common import *

from server.httpcomm import *


def download_file_direct(file, request_id, filename, format=FASTA):
    dir = DOWNLOAD_FILE_PATH.format(request_id=request_id)
    if not os.path.exists(dir):
        os.makedirs(dir)
    try:
        file.save(os.path.join(dir, '.'.join([filename, format])))
    except Exception:
        print 'Error in downloading file'
        return INT_FAILURE_DOWNLOAD
    return INT_DOWNLOADED



def download_file_google_drive(user_id, drive_service, file_id, filename):
    '''
    :param user_id:
    :param drive_service:
    :param file_id:
    :param filename:
    :return: status code
    '''
    try:
        assert user_id
        assert drive_service
        assert file_id
        assert filename
    except AssertionError as e:
        print 'One or more required parameters are missing ', e
        return INT_ERROR_FORMAT

    try:
        request = drive_service.files().get_media(fileId=file_id)
        path = DOWNLOAD_FILE_PATH.format(user_id=user_id)
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        fh = io.FileIO(path + '\\' + filename, 'wb')
        downloader = http.MediaIoBaseDownload(fh, request)
        done = False
        print 'Downloading file {file_id} for user {user_id}'.format(file_id=file_id, user_id=user_id)
        while done is False:
            status, done = downloader.next_chunk()
            print "Download %d%%." % int(status.progress() * 100)
    except Exception as e:
        print 'Error in downloading file ', e
        return INT_FAILURE_DOWNLOAD
    return INT_DOWNLOADED


def upload_file_google_drive(service, title, description, parent_id, mime_type, filename):
    """Insert new file.
    Args:
      service: Drive API service instance.
      title: Title of the file to insert, including the extension.
      description: Description of the file to insert.
      parent_id: Parent folder's ID.
      mime_type: MIME type of the file to insert.
      filename: Filename of the file to insert.
    Returns:
      Inserted file metadata if successful, None otherwise.
    """
    media_body = http.MediaFileUpload(filename, mimetype=mime_type, resumable=True)
    body = {
        'title': title,
        'description': description,
        'mimeType': mime_type
    }
    # Set the parent folder.
    if parent_id:
        body['parents'] = [{'id': parent_id}]

    try:
        file = service.files().insert(
            body=body,
            media_body=media_body).execute()

        # Uncomment the following line to print the File ID
        print 'File ID: %s' % file['id']
    except errors.HttpError, error:
        print 'An error occured: %s' % error
        return INT_FAILURE_UPLOAD,None
    return INT_UPLOADED, file['id']