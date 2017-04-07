import httplib2
import logging
from apiclient import errors
from common.globalconst import *
from common.globalfunct import *
from database import *
from database.domain.user import User
from database.interface.request import *
from datetime import datetime, timedelta
from dateutil import parser
from googleapiclient.discovery import build
from oauth2client.client import Credentials
from oauth2client.client import FlowExchangeError
from oauth2client.client import flow_from_clientsecrets
from server.errorhandler import *
from server.server_common import *
from server.httpcomm.interface import *
from server.httpcomm.const import *


# ...


# Path to client_secret.json which should contain a JSON document such as:
#   {
#     "web": {
#       "client_id": "[[YOUR_CLIENT_ID]]",
#       "client_secret": "[[YOUR_CLIENT_SECRET]]",
#       "redirect_uris": [],
#       "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#       "token_uri": "https://accounts.google.com/o/oauth2/token"
#     }
#   }

def renew_access_token(client_id = '', client_secret='', refresh_token = '', grant_type = 'refresh_token'):
    try:
        assert client_id
        assert client_secret
        assert refresh_token
        assert grant_type
    except AssertionError:
        print 'Missing parameters for token renewal'
        return INT_FAILURE, None
    try:
        params = RENEW_TOKEN_PARAMS.format(client_id=client_id, client_secret=client_secret,
                                           refresh_token=refresh_token,grant_type=grant_type)
        headers = {'Cache-Control':'no-cache',
                   'content-type':'application/x-www-form-urlencoded'}
        response = simple_http_request(url=RENEW_TOKEN_URL, method='POST', url2=RENEW_TOKEN_PATH, body=params, ishttps=True, headers=headers)
        data = json_decode(response.read())
        if 'access_token' in data:
            return INT_OK, data
        else:
            print 'Could not retrieve access token'
            return INT_FAILURE_RENEW, None
    except Exception as e:
        print 'Error in renew_access_token ',e
        return INT_ERROR_GENERAL, None



def get_stored_credentials(user_id):
    """Retrieved stored credentials for the provided user ID.

    Args:
      user_id: User's ID.
    Returns:
      Stored oauth2client.client.OAuth2Credentials if found, None otherwise.
    """
    #
    #       To instantiate an OAuth2Credentials instance from a Json
    #       representation, use the oauth2client.client.Credentials.new_from_json
    #       class method.

    try:
        db.connect()
    except:
        print 'db already open'
    try:
        user = User.select().where(User.user_id == user_id)
        user = user[0]
        if user.credentials:
            # credentials =  Credentials.new_from_json(user['credentials'])
            credentials = json.loads(user.credentials)
            token_expiry = credentials['token_expiry']
            dexp = parser.parse(str(token_expiry))
            dexp = dexp.replace(tzinfo=None)
            dnow = datetime.now()

            if dexp > dnow:
                return Credentials.new_from_json(user.credentials)
            else:
                status_code, data = renew_access_token(client_id=credentials['client_id'],
                                                       client_secret=credentials['client_secret'],
                                                       refresh_token=credentials['refresh_token'],
                                                       )
                if status_code == INT_OK:
                    credentials['access_token'] = data['access_token']
                    credentials['token_expiry'] = datetime_util(datetime.now() + timedelta(seconds=float(str(data['expires_in']))))
                    credentials = Credentials.new_from_json(json_encode(credentials))
                    user.update_credentials(credentials.to_json())

                    return credentials
                else:
                    return None
        else:
            return None
    except Exception as e:
        print e
        return None
    finally:
            db.close()


def store_credentials(user_id, credentials, user_info):
    """Store OAuth 2.0 credentials in the application's database.

    This function stores the provided OAuth 2.0 credentials using the user ID as
    key.

    Args:
      user_id: User's ID.
      credentials: OAuth 2.0 credentials to store.
    """
    #
    #       To retrieve a Json representation of the credentials instance, call the
    #       credentials.to_json() method.
    try:
        db.connect()
    except:
        print 'Error in connecting to database'
    try:
        query_requests = User.select().where(User.user_id == user_id)
        if query_requests:
            user = query_requests[0]
            user.update_credentials(credentials.to_json())
            user.save_user_info(user_info)
        else:
            user = User(user_id=user_id, credentials=credentials.to_json())
            user.save(force_insert=True)

    except Exception as e:
        print 'Error while storing credentials ',e
    finally:
            db.close()


    '''
    try:
        user.sync()
    except Exception as e:
        print 'Error in saving user details in database ',e
    '''


def exchange_code(authorization_code):
    """Exchange an authorization code for OAuth 2.0 credentials.

    Args:
      authorization_code: Authorization code to exchange for OAuth 2.0
                          credentials.
    Returns:
      oauth2client.client.OAuth2Credentials instance.
    Raises:
      CodeExchangeException: an error occurred.
    """

    flow = flow_from_clientsecrets(CLIENTSECRET_LOCATION, ' '.join(SCOPES))
    flow.redirect_uri = REDIRECT_URI
    try:
        print authorization_code
        credentials = flow.step2_exchange(authorization_code)
        return credentials
    except FlowExchangeError, error:
        logging.error('An error occurred: %s', error)
        raise CodeExchangeException(None)


def get_user_info(credentials):
    """Send a request to the UserInfo API to retrieve the user's information.

    Args:
      credentials: oauth2client.client.OAuth2Credentials instance to authorize the
                   request.
    Returns:
      User information as a dict.
    """
    user_info_service = build(
        serviceName='oauth2', version='v2',
        http=credentials.authorize(httplib2.Http()))
    user_info = None
    try:
        user_info = user_info_service.userinfo().get().execute()
    except errors.HttpError, e:
        logging.error('An error occurred: %s', e)
    if user_info and user_info.get('id'):
        return user_info
    else:
        raise NoUserIdException()


def get_authorization_url(email_address, state):
    """Retrieve the authorization URL.

    Args:
      email_address: User's e-mail address.
      state: State for the authorization URL.
    Returns:
      Authorization URL to redirect the user to.
    """
    flow = flow_from_clientsecrets(CLIENTSECRET_LOCATION, ' '.join(SCOPES))
    flow.params['access_type'] = 'offline'
    flow.params['approval_prompt'] = 'force'
    flow.params['user_id'] = email_address
    flow.params['state'] = state
    flow.params['origin'] = ORIGIN
    return flow.step1_get_authorize_url(REDIRECT_URI)


def get_credentials(authorization_code, state=None):
    """Retrieve credentials using the provided authorization code.

    This function exchanges the authorization code for an access token and queries
    the UserInfo API to retrieve the user's e-mail address.
    If a refresh token has been retrieved along with an access token, it is stored
    in the application database using the user's e-mail address as key.
    If no refresh token has been retrieved, the function checks in the application
    database for one and returns it if found or raises a NoRefreshTokenException
    with the authorization URL to redirect the user to.

    Args:
      authorization_code: Authorization code to use to retrieve an access token.
      state: State to set to the authorization URL in case of error.
    Returns:
      oauth2client.client.OAuth2Credentials instance containing an access and
      refresh token.
    Raises:
      CodeExchangeError: Could not exchange the authorization code.
      NoRefreshTokenException: No refresh token could be retrieved from the
                               available sources.
    """
    email_address = ''
    try:
        credentials = exchange_code(authorization_code)
        user_info = get_user_info(credentials)
        user_id = user_info.get('id')
        if credentials.refresh_token is not None:
            store_credentials(user_id, credentials, user_info)
            return user_id, INT_OK
        else:
            credentials = get_stored_credentials(user_id)
            if credentials and credentials.refresh_token is not None:
                return user_id,INT_OK
    except CodeExchangeException, error:
        logging.error('An error occurred during code exchange.')
        # Drive apps should try to retrieve the user and credentials for the current
        # session.
        # If none is available, redirect the user to the authorization URL.
        error.authorization_url = get_authorization_url(email_address, state)
        raise error
    except NoUserIdException:
        logging.error('No user ID could be retrieved.')
    # No refresh token has been retrieved.
    authorization_url = get_authorization_url(email_address, state)
    raise NoRefreshTokenException(authorization_url)


def connect_proc(fields=None, client_ip=STR_UNDEFINED):
    _connect_proc_parsing_fields(fields)
    user_id, auth_status_code = get_credentials(fields['authcode'])
    return respond_json(auth_status_code), user_id


def get_oauth_token(user_id):
    try:
        db.connect()
    except:
        print 'Error in opening database'
    try:
        user = User.select().where(User.user_id == str(user_id))
        if user[0].credentials:
            credentials = json.loads(user[0].credentials)
            access_token = credentials['access_token']
            return access_token
    except Exception as e:
        print e
        return None
    finally:
            db.close()
    return None


def _connect_proc_parsing_fields(fields):
    try:
        assert 'authcode' in fields
    except AssertionError:
        print 'Error : Authorization code not received in the request'
        raise InvalidUsage('Wrong fields format', status_code=400)


def process_request(fields, files):
    _request_parsing_fields(fields)
    status_code, request_id = store_request(fields['form_type'],
                                fields['data_type'],
                                fields['num_request'],
                                json_decode(str(fields['form_data'])),
                                files)

    if fields['form_type'] == SINGLE:
        if status_code == INT_OK:
            #call the respective process
            html = '<html><HELLO></html>'
            return status_code, respond_json(status_code, html=html)
        else:
            return INT_ERROR_GENERAL, None
    else:
        html = '<html>HELLO</hello>'
        return status_code, respond_json(status_code, html=html)




'''
Private Functions
'''
def _request_parsing_fields(fields):
    try:
        assert 'form_type' in fields
        assert 'data_type' in fields
        assert 'num_request' in fields
        assert 'form_data' in fields
    except AssertionError:
        print 'Error while parsing requests, one or more fields are missing'
        raise InvalidUsage('Wrong fields form', status_code=400)

    form_type = fields['form_type']
    data_type = fields['data_type']
    num_request = int(fields['num_request'])
    form_data = json_decode(str(fields['form_data']))

    try:
        assert len(form_data['requests']) == num_request
        if form_type == SINGLE and data_type  == SANGER_SEQUNCE_DATA:
            pass
        elif form_type == SINGLE and data_type == NEXT_GEN_DATA:
            pass
        elif form_type == MULTIPLE and data_type == SANGER_SEQUNCE_DATA:
            pass
        elif form_type == MULTIPLE and data_type == NEXT_GEN_DATA:
            pass

    except AssertionError:
        print 'Error while parsing requests, one or more fields are missing'
        raise InvalidUsage('Wrong fields form', status_code=400)
