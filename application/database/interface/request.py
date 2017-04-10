import os
from common.globalconst import *
from common.globalfunct import *
from database import *
import time
from database.domain.request import DatingRequest

from server.filehandler import download_file_direct


def store_request(form_type, data_type, num_request, form_data, files, user_id):
    try:
        db.connect()
    except:
        print 'Error in opening database connection'

    request_id = id_generator(INT_LEN_REQUEST_ID)

    try:
        query_res = DatingRequest.select().where(DatingRequest.request_id == request_id)
        while len(query_res) > 0:
            request_id = id_generator(INT_LEN_REQUEST_ID)
            query_res = DatingRequest.select().where(DatingRequest.request_id == request_id)
        status, json_data, download_status = _create_form_data(form_type, data_type, num_request, form_data, files,
                                                               request_id)
        record = DatingRequest(request_id=request_id,
                               user_id=user_id,
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


def fetch_request(request_id, session_user_id):
    try:
        db.connect()
    except Exception as e:
        print 'Error in opening database ', e
        raise

    try:
        query_res = DatingRequest.select().where(DatingRequest.request_id == request_id)
        if query_res:
            request = query_res[0]
            if request.form_type == SINGLE:
                is_processed = request.is_processed
                start_time = datetime.now()
                while not is_processed and (datetime.now() - start_time).seconds < DELTA:
                    time.sleep(5)
                    is_processed = request.is_processed

                if is_processed:
                    return INT_OK
                else:
                    return INT_NOTPROCESSED

            elif request.form_type == MULTIPLE:
                user_id = request.user_id
                if session_user_id == user_id:
                    return INT_OK

        return INT_FAILURE
    except Exception as e:
        print 'Error in fetching request from database ', e
    finally:
        db.close()


'''
Private Functions
'''


def _get_file_path(request_id, file, format=FASTA):
    return os.path.join(DOWNLOAD_FILE_PATH.format(request_id=request_id), '.'.join([file, format]))


def _create_form_data(form_type, data_type, num_request, form_data, files, request_id):
    request_list = []
    download_status = False
    if data_type == SANGER_SEQUNCE_DATA:
        for i, request in enumerate(form_data['requests']):
            if form_type == SINGLE:
                download_status_code = download_file_direct(files[request['file']], request_id, request['file'],
                                                            FASTA)
                if download_status_code == INT_DOWNLOADED:
                    download_status = True
                request_list.append({'fasta_file': {'file_id': request_id + '_' + request['file'],
                                                    'file_path': _get_file_path(request_id, request['file'], FASTA),
                                                    'meta_data': {},
                                                    'is_downloaded': True
                                                    },
                                     'align': request['align'],
                                     'hxb2': request['hxb2'],
                                     })
            elif form_type == MULTIPLE:
                request_list.append({'fasta_file': {'file_id': request_id + '_' + request['file'],
                                                    'file_path': _get_file_path(request_id, request['file'], FASTA),
                                                    'meta_data': request['meta_data'],
                                                    'is_downloaded': False
                                                    },
                                     'align': request['align'],
                                     'hxb2': request['hxb2'],
                                     })

    elif data_type == NEXT_GEN_DATA:
        for i, request in enumerate(form_data['requests']):
            request_dict = {}
            request_dict['forward_file'] = {}
            request_dict['backward_file'] = {}
            if form_type == SINGLE:
                download_status_code_list = []
                for f in request_dict:
                    download_status_code_list.append(download_file_direct(files[f], request_id, request[f], FASTQ))
                    request_dict[f] = {'file_id': request_id + '_' + request[f],
                                       'file_path': _get_file_path(request_id, request[f], FASTQ),
                                       'meta_data': {},
                                       'is_downloaded': True}

                if all(status == INT_DOWNLOADED for status in download_status_code_list):
                    download_status = True
            elif form_type == MULTIPLE:
                for f in request_dict:
                    request_dict[f] = {'file_id': request_id + '_' + request[f],
                                       'file_path': _get_file_path(request_id, request[f], FASTQ),
                                       'meta_data': request['meta_data'][f],
                                       'is_downloaded': False}

            # TODO ADD ALL THE FIELDS OF FASTQ FORM AND UPDATE THE DICTIONARY
            request_list.append(request_dict)

    return INT_OK, json_encode({'requests': request_list}), download_status
