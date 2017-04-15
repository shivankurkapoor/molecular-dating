import json
import os
import random
import string
import shutil
from datetime import datetime
from distutils.dir_util import copy_tree

from flask import jsonify


def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
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


def datetime_util(date=None):
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
    return date + 'T' + time + 'Z'


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def write_bash_file(*args, **kwargs):
    script_path = args[0]
    script_name = args[1]
    command = kwargs.pop('command')
    for key, value in kwargs.items():
        command += ' ' + '--' + str(key) + '=' + str(value)
    script = '.'.join([os.path.join(script_path, script_name), 'sh'])

    try:
        if not os.path.exists(script_path):
            os.makedirs(script_path)
        with open(script, 'w') as f:
            f.write(command)
    except IOError as e:
        print 'Error in generating bash script', e


def copy_dir(source_dir, destination_dir):
    try:
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
    except Exception as e:
        print 'Error while creating ', destination_dir, e
    copy_tree(source_dir, destination_dir)


def make_zip(file_name, format, directory):
    try:
        return shutil.make_archive(file_name, format, directory)
    except Exception as e:
        print 'Error while archiving ', file_name, e
        raise
