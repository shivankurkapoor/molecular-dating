'''
This is the main file for the backend server
'''

from flask import Flask, render_template, session, redirect
from flask import request, current_app

from server.connect import *

application = Flask(__name__, )
application.secret_key = APP_SECRET_KEY


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)

    return decorator


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
    if (int(request_params['status']) == INT_OK):
        # return render_template('display/' + request_params['request_id'] + '.html')
        return render_template(
            os.path.join('result', request_params['request_id'], str(request_params['request_id']) + '.html'))
    elif int(request_params['status']) == INT_PROCESSED or (int(request_params['status']) == INT_NOTPROCESSED):
        return render_template(
            os.path.join('result', request_params['request_id'], str(request_params['request_id']) + '.html'))
    else:
        return render_template('error.html',
                               error='You are not authorized view this request status')


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
@crossdomain(origin='http://p512.usc.edu')
def upload():
    user_id = session.get('userId', '')
    print request.form
    print request.files
    print user_id
    status, response = process_request(request.form, request.files, user_id=user_id)
    if status == INT_OK:
        print 'I am here'
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
    application.run(host='192.168.22.2', port=5000, debug=False)
