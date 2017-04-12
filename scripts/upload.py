import smtplib
import sys

sys.path.append('../application')
import httplib2
from oauth2client.client import Credentials
from apiclient import http
from database import *
from database.domain.user import User
from database.domain.request import DatingRequest
from server.httpcomm.interface import *
from apiclient import discovery
from argparse import ArgumentParser
from apiclient import errors
from common.globalfunct import *
from email.mime.text import MIMEText


def send_email(sender, receiver, SMTP_server, message, request_id, password):
    '''

    :param sender:
    :param receiver:
    :param SMTP_server:
    :param message:
    :param request_id:
    :return:
    '''
    msg = MIMEText(message)
    msg['Subject'] = 'HIV Molecular Dating Request ID %s' % request_id
    msg['From'] = sender
    msg['To'] = receiver
    s = smtplib.SMTP('localhost')
    s.ehlo()
    s.starttls()
    s.login(sender,password)
    s.sendmail(sender, [receiver], msg.as_string())
    s.quit()


def upload_file_google_drive(service, title, description, parent_id, mime_type, filename):
    """Insert new file.
    Args:
      service: Drive API service instance.
      title: Title of the file to insert, including the extension.
      description: Description of the file to insert.
      parent_id: Parent folder's ID.
      mime_type: MIME type of the file to insert.
      filename: Filename of the file to insert.
    Returns:
      Inserted file metadata if successful, None otherwise.
    """
    media_body = http.MediaFileUpload(filename, mimetype=mime_type, resumable=True)
    body = {
        'title': title,
        'description': description,
        'mimeType': mime_type
    }
    # Set the parent folder.
    if parent_id:
        body['parents'] = [{'id': parent_id}]

    try:
        file = service.files().insert(
            body=body,
            media_body=media_body).execute()

        # Uncomment the following line to print the File ID
        print 'File ID: %s' % file['id']
    except errors.HttpError, error:
        print 'An error occured: %s' % error
        return INT_FAILURE_UPLOAD, None
    return INT_UPLOADED, file


if __name__ == '__main__':

    parser = ArgumentParser(description="Upload file to Google Drive")

    '''
    Defining arguments
    '''
    parser.add_argument("--user_id", dest="user_id", default="")
    parser.add_argument("--request_id", dest="request_id", default="")
    parser.add_argument("--file_path", dest="file_path", default="")

    '''
    Parsing Arguments
    '''
    args = parser.parse_args()

    print args.user_id
    print args.request_id
    print args.file_path

    try:
        assert args.user_id != ""
        assert args.request_id != ""
        assert args.file_path != ""
    except AssertionError as e:
        print e
        raise


    upload_status = False
    download_link = ''
    email = ''

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
            description = 'Output files for request_id : {request_id}'.format(request_id=args.request_id)
            status, meta_data = upload_file_google_drive(drive_service, file_name, description, None, ZIP_MIME_TYPE,
                                                         str(args.file_path))

            upload_status = status
            email = user.email
            if status == INT_UPLOADED:
                download_link = meta_data['alternateLink']

                with db.atomic():
                    request_query_res = DatingRequest.select().where(DatingRequest.request_id == str(args.request_id))
                    if request_query_res:
                        dating_request = request_query_res[0]
                        query_form_update = DatingRequest.update(is_uploaded=True, upload_file_meta_data=str(
                            json_encode(meta_data))).where(
                            DatingRequest.request_id == str(args.request_id))
                        query_form_update.execute()

    except Exception as e:
        print 'Error in updating records in uploading function ', e
    finally:
        db.close()

    if upload_status:
        try:
            email = EMAIL.format(request_id=args.request_id, link=download_link)
            send_email(SENDER, str(email), SERVER, email, args.request_id, PASSWORD)
        except Exception as e:
            print 'Error in sending email to ',email, e
