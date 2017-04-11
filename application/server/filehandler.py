'''
Created by : Shivankur Kapoor
Created on : 12/21/2016
This module contains functions
'''

import errno
import io

from apiclient import errors
from apiclient import http

from common.globalfunct import *
from server.server_common import *


def download_file_direct(file, request_id, filename, format=FASTA):
    if format == FASTA:
        dir = os.path.join(DOWNLOAD_FILE_PATH.format(request_id=request_id, request_idx='0'), FASTA_DIR)
    else:
        dir = os.path.join(DOWNLOAD_FILE_PATH.format(request_id=request_id, request_idx='0'), FASTQ_DIR)

    if not os.path.exists(dir):
        os.makedirs(dir)
    try:
        file.save(os.path.join(dir, '.'.join([filename, format])))
    except Exception:
        print 'Error in downloading file'
        return INT_FAILURE_DOWNLOAD
    return INT_DOWNLOADED

