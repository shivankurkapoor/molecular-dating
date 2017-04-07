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
        query_result = DatingRequest.select().where(request_id == request_id)
        if query_result:
            request = query_result[0]
            generate_bash_scripts(request.request_id, request.form_type, request.data_type,
                                  json_decode(request.form_data), request.user_id)

            output_path = os.path.join(OUTPUT_PATH, request_id)
            generate_html(output_path, request_id, user_id)

            # TODO CREATE OUTPUT FOLDER AND RESPONSE PAGE
            if request.form_type == SINGLE:
                #TODO SHOULD YOU EXECUTE IT OR PUT IT IN REQUEST QUEUE AND WAIT
                # TODO CREATE OUTPUT FOLDER AND RESPONSE PAGE
                pass


            return INT_OK,

    except Exception as e:
        print 'Error in fetching records from database', e
    finally:
        db.close()


def generate_bash_scripts(request_id, form_type, data_type, form_data, user_id):
    try:
        if form_type == MULTIPLE:
            command = 'python file_downloader.py'
            script_path = BASH_SCRIPT_DOWNLOAD
            if data_type == SANGER_SEQUNCE_DATA:
                for idx, request in enumerate(form_data['requests']):
                    file_id = request['fasta_file']['meta_data']['id']
                    file_path = request['fasta_file']['file_path']
                    script_name = '_'.join([request_id, str(idx)])
                    write_bash_file(script_path, script_name, command=command, user_id=user_id, file_id=file_id, file_path=file_path,
                                    request_id=request_id, request_idx=idx)

            elif data_type == NEXT_GEN_DATA:
                for idx, request in enumerate(form_data['requests']):
                    for f in request:
                        file_id = request[f]['meta_data']['id']
                        file_path = request[f]['meta_data']['file_path']
                        script_name = '_'.join([request_id, str(idx), f])
                        write_bash_file(script_path, script_name, command=command, user_id=user_id, file_id=file_id,
                                        file_path=file_path, request_id=request_id, request_idx=idx)

        elif form_type == SINGLE:
            request = form_data['requests'][0]
            script_path = BASH_SCRIPT_EXECUTE
            if data_type == SANGER_SEQUNCE_DATA:
                command = 'python sanger_main.py'
                align = 'TRUE' if request['align'] else 'FALSE'
                hxb2 = 'TRUE' if request['hxb2'] else 'FALSE'
                script_name = request_id
                write_bash_file(script_path, script_name,command=command, align=align, hxb2=hxb2, request_id=request_id, request_idx=0)

            elif data_type == NEXT_GEN_DATA:
                command = 'python next_gen_main.py'
                script_name = request_id
                write_bash_file(script_path, script_name, command=command, request_id=request_id, request_idx=0)

    except Exception as e:
        print 'Error in generating bash scripts', e


def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)

def generate_html(directory, request_id, user_id):
    try:
        db.connect()
    except Exception as e:
        print 'Error in opening database', e
        raise

    try:
        if not os.path.exists(directory):
            os.makedirs(directory)

        query_result = User.select().where(user_id == user_id)
        if query_result:
            user = query_result[0]
            email = user.email
            context = {
                'request_id' : request_id,
                'email' : email
            }
            fname = '_'.join(['display',request_id]) + '.html'

            with open(fname, 'w') as f:
                html = render_template(os.path.join(TEMPLATE_PATH, 'display_template.html'), context)
                f.write(html)
        
    except Exception as e:
        print 'Error in generating html file', e


