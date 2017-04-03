"""
This script implements methods to make HTTP requests
If you want to directly analyze the http response, use simple_http_request
Otherwise, if you want directly the responding data, use http_request
Simplify as simple_http_request to return the raw http response
and http_request to return the processed data

"""
from common.globalconst import *
from common.globalfunct import *
from server.httpcomm.const import *

import httplib
import urllib
import socket


def http_request(url=STR_UNDEFINED,
                 body='',
                 method='GET',
                 url2='',
                 ishttps=False,
                 headers=None,
                 debug=False):
    """
    This is the more complex http request, it processes the response and extract data for you
    :param url:
    :param method:
    :param body: str
    :param headers: dict, includes all header fields
    :param url2: This is the sub URL addr at Finicity side
    :param ishttps:
    :param debug: whether we print out more details on screen
    :return: status and response data (no http return code)
    """
    try:
        r1 = simple_http_request(url, body, method, url2, ishttps, headers, debug)
        assert isinstance(r1.status, int)
        if r1.status // 100 == 2 or r1.status // 100 == 3:
            try:
                data1 = r1.read()
            except all as e:
                print 'Error in read http response:', e
                return INT_ERROR_GENERAL, e
                # raise
            return INT_OK, data1
        else:
            print ('HTTP Request Status Code Not Right:',
                   r1.status, ',', r1.reason)
            return INT_ERROR_GENERAL, ('Error Status:', r1.status, ',Reason:', r1.reason)
    except all as e:
        print 'http_request error:', e
        raise


def simple_http_request(url=STR_UNDEFINED,
                        body='',
                        method='GET',
                        url2='',
                        ishttps=False,
                        headers=None,
                        debug=False):
    """
    This is the method for requesting simple http request, the raw version
    :param url:
    :param method:
    :param body: str
    :param headers: dict, includes all header fields
    :param url2: This is the sub URL addr at Finicity side
    :param ishttps:
    :param debug: whether we print out more details on screen
    :return: the actual response object
    """
    assert url != STR_UNDEFINED
    assert method in LIST_HTTP_METHODS
    assert isinstance(headers, dict) or headers is None
    try:
        conn = httplib.HTTPSConnection(url) \
            if ishttps \
            else httplib.HTTPConnection(url)
    except all as e:
        print 'Error occurred during connection:', e
        raise
    try:
        if isinstance(headers, dict):
            if len(headers):
                conn.request(method, url2,
                             body, headers)
            else:
                conn.request(method, url2, body)
        else:
            conn.request(method, url2, body)
    except all as e:
        print 'HTTP Request Error at Connection Stage: ', e
        raise
    try:
        r1 = conn.getresponse()
        return r1
    except all as e:
        print 'Error in get response from http request:', e
        raise
