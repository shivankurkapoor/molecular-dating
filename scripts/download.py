import sys

sys.path.append('/Users/shivankurkapoor/GitHub/moleculardating/application')
import io
import httplib2
import errno

from oauth2client.client import Credentials
from apiclient import http
from database import *
from database.domain.user import User
from database.domain.request import DatingRequest
from apiclient import discovery
from argparse import ArgumentParser
from common.globalfunct import *
from common.globalconst import *


def download_file_google_drive(user_id, drive_service, file_id, filename, file_path):
    '''
    :param user_id:
    :param drive_service:
    :param file_id:
    :param filename:
    :return: status code
    '''
    try:
        assert user_id
        assert drive_service
        assert file_id
        assert filename
    except AssertionError as e:
        print 'One or more required parameters are missing ', e
        return INT_ERROR_FORMAT

    try:
        request = drive_service.files().get_media(fileId=file_id)
        path = file_path
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        fh = io.FileIO(path + os.sep + filename, 'wb')
        downloader = http.MediaIoBaseDownload(fh, request)
        done = False
        print 'Downloading file {file_id} for user {user_id}'.format(file_id=file_id, user_id=user_id)
        while done is False:
            status, done = downloader.next_chunk()
            print "Download %d%%." % int(status.progress() * 100)
    except Exception as e:
        print 'Error in downloading file ', e
        return INT_FAILURE_DOWNLOAD
    return INT_DOWNLOADED


def check_download_status(requests, data_type):
    download_status_list = []
    for request in requests:
        if data_type == SANGER_SEQUNCE_DATA:
            download_status_list.append(request['fasta_file']['is_downloaded'])
        elif data_type == NEXT_GEN_DATA:
            download_status_list.append(request['backward_file']['is_downloaded'])
            download_status_list.append(request['forward_file']['is_downloaded'])
    return all(status == True for status in download_status_list)


if __name__ == '__main__':

    parser = ArgumentParser(description="Downloading file from Google Drive")

    '''
    Defining arguments
    '''
    parser.add_argument("--user_id", dest="user_id", default="")
    parser.add_argument("--file_id", dest="file_id", default="")
    parser.add_argument("--request_id", dest="request_id", default="")
    parser.add_argument("--file_path", dest="file_path", default="")
    parser.add_argument("--request_idx", dest="request_idx", default="")
    parser.add_argument("--file_type", dest="file_type", default="")

    '''
    Parsing Arguments
    '''
    args = parser.parse_args()

    print args.user_id
    print args.file_id
    print args.request_id
    print args.file_path
    print args.request_idx
    print args.file_type

    try:
        assert args.user_id != ""
        assert args.file_id != ""
        assert args.request_id != ""
        assert args.file_path != ""
        assert args.request_idx != ""
        assert args.file_type != ""
    except AssertionError as e:
        print e
        sys.exit(1)

    try:
        db.connect()
    except Exception as e:
        print 'Error in opening database connection ', e
        raise

    try:
        user_query_res = User.select().where(User.user_id == str(args.user_id))
        if user_query_res:
            user = user_query_res[0]
            credentials = Credentials.new_from_json(user.credentials)
            http_auth = credentials.authorize(httplib2.Http())
            drive_service = discovery.build('drive', 'v2', http_auth)
            file_path, file_name = str(args.file_path).rsplit(os.sep, 1)
            status = download_file_google_drive(str(args.user_id), drive_service, args.file_id, file_name, file_path)

            if status == INT_DOWNLOADED:

                with db.atomic():
                    request_query_res = DatingRequest.select().where(DatingRequest.request_id == str(args.request_id))
                    if request_query_res:
                        dating_request = request_query_res[0]
                        form_data = json_decode(str(dating_request.form_data))
                        form_data['requests'][int(args.request_idx)][str(args.file_type)]['is_downloaded'] = True

                        # Check if files for a single process has been downloaded
                        # In case of NGS, we need to generate bash script for fastq to fasta
                        # In case of Sanger, we need to generate the bash script for molecular dating
                        if dating_request.data_type == SANGER_SEQUNCE_DATA:
                            script_name = args.request_id + '_' + str(args.request_idx)
                            script_path = BASH_SCRIPT_PROCESS.format(request_id=args.request_id)
                            align = form_data['requests'][int(args.request_idx)]['align']
                            hxb2 = form_data['requests'][int(args.request_idx)]['hxb2']
                            input_dir = RESULT_PATH.format(request_id=str(args.request_id),
                                                           request_idx=str(args.request_idx))

                            command = 'python '
                            if hxb2:
                                command += HXB_PROCESS_SCRIPT
                                script_name = 'HXB2_' + script_name
                            else:
                                command += FENV_PROCESS_SCRIPT
                                script_name = 'FENV_' + script_name

                            write_bash_file(script_path, script_name, command=command, align=align,
                                            request_id=args.request_id, request_idx=args.request_idx,
                                            input_dir=input_dir)

                        elif dating_request.data_type == NEXT_GEN_DATA:
                            if form_data['requests'][int(args.request_idx)]['backward_file']['is_downloaded'] and \
                                    form_data['requests'][int(args.request_idx)]['forward_file']['is_downloaded']:
                                command = 'python ' + FASTQTOFASTA_SCRIPT
                                script_name = 'FASTQ_TO_FASTA_' + args.request_id + '_' + str(args.request_idx)
                                script_path = BASH_SCRIPT_PROCESS.format(request_id=args.request_id)
                                forward_primer = form_data['requests'][int(args.request_idx)]['forward_primer']
                                backward_primer = form_data['requests'][int(args.request_idx)]['backward_primer']
                                seq_len = form_data['requests'][int(args.request_idx)]['seq_len']
                                base_count = form_data['requests'][int(args.request_idx)]['base_count']
                                percent = form_data['requests'][int(args.request_idx)]['percent']
                                output_dir = os.path.join(
                                    RESULT_PATH.format(request_id=args.request_id, request_idx=str(args.request_idx)),
                                    FASTA_DIR)
                                forward_file = form_data['requests'][int(args.request_idx)]['forward_file']['file_path']
                                backward_file = form_data['requests'][int(args.request_idx)]['backward_file'][
                                    'file_path']
                                write_bash_file(script_path, script_name, command=command,
                                                forward_primer=forward_primer,
                                                backward_primer=backward_primer,
                                                seq_len=seq_len, base_count=base_count, percent=percent,
                                                forward_file=forward_file,
                                                backward_file=backward_file, request_id=args.request_id,
                                                output_dir=output_dir,
                                                request_idx=0)

                        # Updaing form
                        query_form_update = DatingRequest.update(form_data=str(json_encode(form_data))).where(
                            DatingRequest.request_id == str(args.request_id))
                        query_form_update.execute()

                        # Checking the download status of all files in the request
                        download_status = check_download_status(form_data['requests'], dating_request.data_type)

                        if download_status:
                            query_download_status_update = DatingRequest.update(are_files_downloaded=True).where(
                                DatingRequest.request_id == str(args.request_id))
                            query_download_status_update.execute()


    except Exception as e:
        print 'Error in updating records in downloading function ', e
    finally:
        db.close()
