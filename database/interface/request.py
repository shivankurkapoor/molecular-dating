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
    success_signal = False
    ttl = INT_TTL_GEN_ID

    try:
        query_res = DatingRequest.get(DatingRequest.requestId == request_id)
        while query_res:
            request_id = id_generator(INT_LEN_REQUEST_ID)
            query_res = DatingRequest.get(DatingRequest.requestId == request_id)
    except:
        request = TaxaRequest(requestId=request_id, userId=user_id, file_json=files_reqd, forward_primer_seq=fps,
                              backward_primer_seq=bps, collapse_length=seqlen, percentage=percent, base_count=basecount)
        request.save(force_insert=True)
    finally:
        if dbopen:
            db_disconnect()

