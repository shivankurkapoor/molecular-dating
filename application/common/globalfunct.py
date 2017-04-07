import json
from datetime import datetime
from flask import jsonify
import os
import string
import random

def id_generator(size=9, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def json_encode(json_dict=None):
    assert isinstance(json_dict, dict)
    return json.dumps(json_dict)

def json_encode_flask(json_dict=None):
    assert isinstance(json_dict, dict)
    return jsonify(json_dict)

def json_decode(json_str=None):
    assert isinstance(json_str, str)
    return json.loads(json_str)

def datetime_util(date = None):
    '''
    This function converts the datetime format {YYYY-MM-DD HH:MM:SS}
    to {YYYY-MM-DDTHH:MM:SSZ} format. This date format is used by Google APIs
    :param date:
    :return:
    '''
    assert isinstance(date, datetime)
    dtstr = str(date)
    dtstr = dtstr.split('.')[0]
    date, time = dtstr.split(' ')
    return date+'T'+time+'Z'


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def write_bash_file(*args, **kwargs):
    script_path = args[0]
    script_name = args[1]
    command = kwargs.pop('command')
    for key, value in kwargs:
        command+= ' '+ '--' + key + '=' + value
    script = os.path.join(script_path, script_name) + '.sh'

    print command
    with open(script , 'w') as f:
        f.write(command)


