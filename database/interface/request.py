from database.domain.request import DatingRequest
from database import *
from common.globalfunct import *
from common.globalconst import *

def store_request(fields):
    try:
        db.connect()
    except:
        print 'Database already open'


    formtype = fields['formtype']
    datatype = fields['datatype']

    request_id = id_generator(INT_LEN_REQUEST_ID)

    try:
        query_res = DatingRequest.get(DatingRequest.requestId == request_id)
        while query_res:
            request_id = id_generator(INT_LEN_REQUEST_ID)
            query_res = DatingRequest.get(DatingRequest.requestId == request_id)
    except:
        form_data = _create_form_data(fields, formtype, datatype, request_id)
        request = DatingRequest()
        request.save(force_insert=True)
    finally:
            db.disconnect()

def _create_form_data(fields, formtype, datatype, request_id):
    form_data = {}
    if formtype == SINGLE and datatype == SANGER_SEQUNCE_DATA:
