'''
This is the main file for the backend server
'''

from flask import Flask, request, render_template, session, redirect

from server.connect import *

application = Flask(__name__, )


@application.route('/')
def app_demo():
    """
      This is the homepage with sign-in option
      :return:
      """
    session.pop('userId', None)
    return render_template('index.html')


@application.route('/multiform', )
def app_show_form():
    if 'userId' in session and session['userId']:
        oauthtoken = get_oauth_token(session['userId'])
        return render_template('multi_index.html', oauthtoken=oauthtoken)
    else:
        return render_template('error.html', error='Could not authenticate')


@application.route('/displaypage', methods=['GET'])
def app_display():
    request_params = request.values
    # Todo Add a check for verifying the request id
    if (int(request_params['status']) == INT_OK) or (int(request_params['status']) == INT_NOTPROCESSED):
        return render_template('display/' + request_params['request_id'] + '.html')
    elif int(request_params['status']) == INT_PROCESSED:
        return render_template('result/' + request_params['request_id'] + '.html')
    else:
        return render_template('error.html',
                               error='You are not authorized view this request status. Please log in to view the status')


@application.route('/fetch', methods=['GET'])
def app_fetch():
    request_params = request.values
    status_code = fetch_request(request_params['request_id'], session.get('userId', ''))
    return respond_json(status_code, request_id=request_params['request_id'], user_id=session.get('userId', ''))


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
    user_id = session.get('userId', '')
    status, response = process_request(request.form, request.files, user_id=user_id)
    if status == INT_OK:
        return response
    else:
        return render_template('error.html', error='Failure')


@application.route('/signout')
def signout():
    session.pop('userId', None)
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
    # application.run(host='p512.usc.edu/miseq',port=5000)
    application.run(host='localhost', port=5000, debug=True)
