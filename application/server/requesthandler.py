from database import *
from database.domain.request import DatingRequest
from database.domain.user import User
from common.globalfunct import *
from common.globalconst import *
from jinja2 import Environment, FileSystemLoader

PATH = TEMPLATE_PATH
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(PATH),
    trim_blocks=False)


def handle_request(request_id, user_id):
    try:
        db.connect()
    except Exception as e:
        print 'Error in opening database connection', e
        raise
    try:
        query_result = DatingRequest.select().where(DatingRequest.request_id == request_id)
        if query_result:
            request = query_result[0]
            generate_bash_scripts(request.request_id, request.form_type, request.data_type,
                                  json_decode(str(request.form_data)), request.user_id)

            if request.form_type == MULTIPLE:
                hrml_output_path = os.path.join(TEMPLATE_PATH, 'display')
                generate_html(hrml_output_path, request_id, user_id, MSG_TEMPLATE_MULTIPLE)
                return INT_OK

            elif request.form_type == SINGLE:
                html_output_path = os.path.join(TEMPLATE_PATH, 'display')
                generate_html(html_output_path, request_id, user_id, MSG_TEMPLATE_SINGLE)
                return INT_OK

        return INT_ERROR_GENERAL
    except Exception as e:
        print 'Error in fetching records from database', e
    finally:
        db.close()


def generate_bash_scripts(request_id, form_type, data_type, form_data, user_id):
    try:
        if form_type == MULTIPLE:
            command = 'python download.py'
            script_path = BASH_SCRIPT_DOWNLOAD
            if data_type == SANGER_SEQUNCE_DATA:
                for idx, request in enumerate(form_data['requests']):
                    file_id = request['fasta_file']['meta_data']['id']
                    file_path = request['fasta_file']['file_path']
                    script_name = '_'.join([request_id, str(idx)])
                    write_bash_file(script_path, script_name, command=command, user_id=user_id, file_id=file_id,
                                    file_path=file_path,
                                    request_id=request_id, request_idx=idx, file_type='fasta_file')

            elif data_type == NEXT_GEN_DATA:
                for idx, request in enumerate(form_data['requests']):
                    for f in request:
                        file_id = request[f]['meta_data']['id']
                        file_path = request[f]['file_path']
                        script_name = '_'.join([request_id, str(idx), f])
                        write_bash_file(script_path, script_name, command=command, user_id=user_id, file_id=file_id,
                                        file_path=file_path, request_id=request_id, request_idx=idx, file_type=f)

        elif form_type == SINGLE:
            request = form_data['requests'][0]
            script_path = BASH_SCRIPT_EXECUTE
            if data_type == SANGER_SEQUNCE_DATA:
                command = 'python sanger_main.py'
                align = 'TRUE' if request['align'] else 'FALSE'
                hxb2 = 'TRUE' if request['hxb2'] else 'FALSE'
                script_name = request_id
                write_bash_file(script_path, script_name, command=command, align=align, hxb2=hxb2,
                                request_id=request_id, request_idx=0)

            elif data_type == NEXT_GEN_DATA:
                command = 'python next_gen_main.py'
                script_name = request_id
                write_bash_file(script_path, script_name, command=command, request_id=request_id, request_idx=0)

    except Exception as e:
        print 'Error in generating bash scripts', e


def jinja_render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)


def generate_html(directory, request_id, user_id, template):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)

        query_result = User.select().where(User.user_id == user_id)
        email = None
        if query_result:
            user = query_result[0]
            email = user.email
        context = {
            'request_id': request_id,
            'user_id': user_id
        }
        if email:
            context.update({'email': email})

        fname = os.path.join(directory, request_id+'.html')

        with open(fname, 'w') as f:
            html = jinja_render_template(template, context)
            f.write(html)

    except Exception as e:
        print 'Error in generating html file', e
