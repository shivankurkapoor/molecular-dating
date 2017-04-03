"""
This is the python file that defines common functions for server module
"""
from common.globalconst import *
from common.globalfunct import json_encode_flask


def respond_json(status_code, **kw):
    myjson = kw
    if status_code == INT_OK:
        myjson['status'] = 'ok'
    elif status_code == INT_ERROR_FORMAT:
        myjson['status'] = 'error'
        myjson['message'] = 'Incorrect fields sent'
    elif status_code == INT_ERROR_PASSEDEXPTIME:
        myjson['status'] = 'failure'
        myjson['message'] = 'Token expired. Please Login Again.'
    elif status_code == INT_ERROR_GENERAL:
        myjson['status'] = 'error'
    elif status_code == INT_CREATED:
        myjson['status'] = 'created'
    elif status_code == INT_LOGGEDOUT:
        myjson['status'] = 'loggedout'
    elif status_code == INT_ERROR_MAXATTEMPTREACHED:
        myjson['status'] = 'error'
        myjson['message'] = 'max attempt reached'
    elif status_code == INT_ERROR_FOUND:
        myjson['status'] = 'failure'
        myjson['message'] = 'user already exists'
    elif status_code == INT_ERROR_NOTEXIST:
        myjson['status'] = 'failure'
        myjson['message'] = 'user not exists'
    elif status_code == INT_FAILURE_AUTH:
        myjson['status'] = 'failure'
        myjson['message'] = 'user authentication failure'
    else:
        myjson['status'] = 'error'
        myjson['message'] = 'missing error message'
    myjson['code'] = status_code
    return json_encode_flask(myjson)

