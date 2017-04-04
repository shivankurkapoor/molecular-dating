from database.domain.request import DatingRequest
from database import *
from common.globalfunct import *
from common.globalconst import *
from server.filehandler import download_file_direct
import os


def store_request(formtype, datatype, numreq, formdata, files):
    try:
        db.connect()
    except:
        print 'Error in opening database connection'

    request_id = id_generator(INT_LEN_REQUEST_ID)

    try:
        query_res = DatingRequest.get(DatingRequest.requestId == request_id)
        while query_res:
            request_id = id_generator(INT_LEN_REQUEST_ID)
            query_res = DatingRequest.get(DatingRequest.requestId == request_id)
    except:
        status, json_data, download_status = _create_json_data(formtype, datatype, numreq, formdata, files, request_id)
        record = DatingRequest(request_id=request_id,
                               form_data=json_data,
                               form_type=formtype,
                               data_type=datatype,
                               are_files_downloaded=download_status)
        record.save(force_insert=True)
        return status, request_id
    finally:
        db.close()


def _get_file_path(request_id, file, format='fasta'):
    return os.path.join(DOWNLOAD_FILE_PATH.format(request_id=request_id), '.'.join([file,format]))


def _create_json_data(formtype, datatype, numreq, formdata, files, request_id):
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
                meta_data = request.meta_data

            request_list.append({'file_id': request_id + '_' + request['file'],
                                 'file_path': _get_file_path(request_id, request['file'],'fasta'),
                                 'align': request['align'],
                                 'hxb2': request['hxb2'],
                                 'meta_data': meta_data})

    return INT_OK, json_encode({'requests': request_list}), download_status
