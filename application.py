'''
This is the main file for the backend server
'''

from flask import Flask, request, render_template, session, redirect
from server.errorhandler import *
from server.connect import *
from common.globalconst import *
from common.globalfunct import *


application = Flask(__name__)


@application.route('/')
def app_demo():
  """
    This is the homepage with sign-in option
    :return:
    """
  return render_template('index.html')

@application.route('/multiform',)
def app_show_form():
    if 'userId' in session and session['userId']:
        oauthtoken = get_oauth_token(session['userId'])
        return render_template('multi_index.html', oauthtoken = oauthtoken)
    else:
        return render_template('error.html', error='Could not authenticate')


@application.route('/connect', methods=['POST'])
def app_connect():
    '''
    This API authenticates the user
    :return:
    '''
    auth_fields = json_decode(request.data)
    return_data, user_id = connect_proc(auth_fields, request.remote_addr)
    session['userId'] = user_id
    return return_data

@application.route('/upload', methods=['POST'])
def upload():
    status = process_request(request)
    return "Form data submitted!"

@application.route('/signout')
def signout():
    session.pop('userId',None)
    return redirect('/')


@application.route('/error')
def error():
    return render_template('error.html', error='Could not authenticate')


@application.errorhandler(404)
def page_not_found(error):
  """
    This is to process error http requests
    :param error:
    :return:
    """
  print '404 error, redirecting...'
  return '404 error, redirecting...'


@application.errorhandler(500)
def page_not_found(error):
  """
    This is to process error http requests
    :param error:
    :return:
    """
  print '500 Error. Server Internal Error...'
  return '500 Error. Server Internal Error...'


@application.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
  response = json_encode_flask(error.to_dict())
  response.status_code = error.status_code
  return response


# starter
if __name__ == '__main__':
    application.secret_key = APP_SECRET_KEY
    #application.debug = True
    #application.run(host='p512.usc.edu/miseq',port=5000)
    application.run(host='localhost', debug=True)
    # application.run(debug=True)


