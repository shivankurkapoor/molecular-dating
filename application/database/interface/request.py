import os
from common.globalconst import *
from common.globalfunct import *
from database import *
from database.domain.request import DatingRequest

from server.filehandler import download_file_direct


def store_request(form_type, data_type, num_request, form_data, files):
    try:
        db.connect()
    except:
        print 'Error in opening database connection'

    request_id = id_generator(INT_LEN_REQUEST_ID)

    #TODO change this logic to use select statements
    try:
        query_res = DatingRequest.select().where(DatingRequest.request_id == request_id)
        while len(query_res) >0:
            request_id = id_generator(INT_LEN_REQUEST_ID)
            query_res = DatingRequest.select().where(DatingRequest.request_id == request_id)
        status, json_data, download_status = _create_form_data(form_type, data_type, num_request, form_data, files, request_id)
        record = DatingRequest(request_id=request_id,
                           form_data=json_data,
                           form_type=form_type,
                           data_type=data_type,
                           are_files_downloaded=download_status)
        record.save(force_insert=True)
        return status, request_id
    except Exception as e:
        print 'Error while inserting new request in Request table', e
        return INT_ERROR_GENERAL, None
    finally:
        db.close()


def _get_file_path(request_id, file, format='fasta'):
    return os.path.join(DOWNLOAD_FILE_PATH.format(request_id=request_id), '.'.join([file,format]))


def _create_form_data(formtype, datatype, numreq, formdata, files, request_id):
    request_list = []
    download_status = False
    if datatype == SANGER_SEQUNCE_DATA:
        for i, request in enumerate(formdata['requests']):
            if formtype == SINGLE:
                download_status_code = download_file_direct(files[request['file']], request_id, request['file'], 'fasta')
                if download_status_code == INT_DOWNLOADED:
                    download_status = True
                meta_data = {}
            else:
                meta_data = request['meta_data']

            request_list.append({'file_id': request_id + '_' + request['file'],
                                 'file_path': _get_file_path(request_id, request['file'],'fasta'),
                                 'align': request['align'],
                                 'hxb2': request['hxb2'],
                                 'meta_data': meta_data})
    elif datatype == NEXT_GEN_DATA:
        for i, request in enumerate(formdata['requests']):
            if formtype == SINGLE:
                download_status_code_list = []
                for file_name, file in files.iteritems():
                    download_status_code_list.append(download_file_direct(file, request_id, file_name, 'fastq'))
                    meta_data = {}
                    request_list.append({'file_id': request_id + '_' + file_name,
                                         'file_path': _get_file_path(request_id, file_name, 'fastq'),
                                         'meta_data': meta_data})

                if all(status  == INT_DOWNLOADED for status in download_status_code_list):
                    download_status = True
            else:
                meta_data = request['meta_data']


    return INT_OK, json_encode({'requests': request_list}), download_status
