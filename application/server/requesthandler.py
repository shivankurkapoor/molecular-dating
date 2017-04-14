from jinja2 import Environment, FileSystemLoader

from common.globalconst import *
from common.globalfunct import *
from database import *
from database.domain.request import DatingRequest
from database.domain.user import User

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
                html_output_path = os.path.join(TEMPLATE_PATH, 'display')
                generate_html(html_output_path, request_id, user_id, MSG_TEMPLATE_MULTIPLE)
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
            command = 'python ' + DOWNLOAD_SCRIPT
            script_path = BASH_SCRIPT_PROCESS.format(request_id=request_id)
            if data_type == SANGER_SEQUNCE_DATA:
                for idx, request in enumerate(form_data['requests']):
                    file_id = request['fasta_file']['meta_data']['id']
                    file_path = request['fasta_file']['file_path']
                    script_name = '_'.join(['DOWNLOAD', 'FASTA_FILE', request_id, str(idx)])
                    write_bash_file(script_path, script_name, command=command, user_id=user_id, file_id=file_id,
                                    file_path=file_path,
                                    request_id=request_id, request_idx=idx, file_type='fasta_file')

            elif data_type == NEXT_GEN_DATA:
                for idx, request in enumerate(form_data['requests']):
                    for f in ['forward_file', 'backward_file']:
                        file_id = request[f]['meta_data']['id']
                        file_path = request[f]['file_path']
                        script_name = '_'.join(['DOWNLOAD' , f.upper(), request_id, str(idx)])
                        write_bash_file(script_path, script_name, command=command, user_id=user_id, file_id=file_id,
                                        file_path=file_path, request_id=request_id, request_idx=idx, file_type=f)

        elif form_type == SINGLE:
            request = form_data['requests'][0]
            script_path = BASH_SCRIPT_FASTPROCESS.format(request_id=request_id)
            if data_type == SANGER_SEQUNCE_DATA:
                command = 'python '
                script_name = request_id
                align = request['align']
                hxb2 =  request['hxb2']
                input_dir = RESULT_PATH.format(request_id=request_id, request_idx = '0')
                html_result_dir = HTML_RESULT_PATH.format(request_id=request_id)
                if hxb2:
                    command+= HXB_PROCESS_SCRIPT
                    script_name = 'HXB2_' + script_name
                else:
                    command+= FENV_PROCESS_SCRIPT
                    script_name = 'FENV_' + script_name

                write_bash_file(script_path, script_name, command=command, align=align, request_id=request_id, input=input_dir, request_idx=0, html_dir=html_result_dir)

            elif data_type == NEXT_GEN_DATA:
                command = 'python ' + FASTQTOFASTA_SCRIPT
                script_name = 'FASTQ_TO_FASTA_' + request_id
                forward_primer = request['forward_primer']
                backward_primer = request['backward_primer']
                seq_len = request['seq_len']
                base_count = request['base_count']
                percent = request['base_count']
                forward_file = request['forward_file']['file_path']
                backward_file = request['backward_file']['file_path']
                output_dir = os.path.join(RESULT_PATH.format(request_id=request_id, request_idx = '0'), FASTQ_DIR)
                write_bash_file(script_path, script_name, command=command, forward_primer=forward_primer,
                                backward_primer=backward_primer,
                                seq_len=seq_len, base_count=base_count, percent=percent, forward_file=forward_file,
                                backward_file=backward_file, request_id=request_id, output_dir=output_dir,
                                request_idx=0)

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

        fname = os.path.join(directory, request_id + '.html')

        with open(fname, 'w') as f:
            html = jinja_render_template(template, context)
            f.write(html)

    except Exception as e:
        print 'Error in generating html file', e
