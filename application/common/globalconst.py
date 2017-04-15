'''
This file contains all the constants
'''
import sys

sys.path.append('../')

STR_UNDEFINED = 'Undefined'

'''
This is the Application secret key of our application.
This is not generated by Google or any third-party API
'''
APP_SECRET_KEY = 'MoleDat:AQWER-WDSEE-DDEWE-WECEG8'

'''
Below fields are related to Google Drive API
'''
# CLIENTSECRET_LOCATION = '/home/web/moleculardating/application/auth/client_secret.json'
# CLIENTSECRET_LOCATION = '/home/leelab/PycharmProjects/moleculardating/application/auth/client_secret.json'
CLIENTSECRET_LOCATION = '/Users/shivankurkapoor/GitHub/moleculardating/application/auth/client_secret.json'
REDIRECT_URI = 'postmessage'
SCOPES = [
    'https://www.googleapis.com/auth/drive.file'
    # Add other requested scopes.
]
ORIGIN = 'http://localhost:5000'
SERVER = 'localhost'

'''
Renew Token URI
'''
RENEW_TOKEN_URL = 'accounts.google.com'
RENEW_TOKEN_PATH = '/o/oauth2/token'
RENEW_TOKEN_PARAMS = 'client_id={client_id}&client_secret={client_secret}&refresh_token={refresh_token}&grant_type={grant_type}'

'''
GOOGLE DRIVE FILE HANDLING
'''
DOWNLOAD_FILE_URL = 'googleapis.com/drive/v2/files/{fileId}?alt=media'
# DOWNLOAD_FILE_PATH = '/home/web/moleculardating/result/{request_id}/{request_idx}'
# DOWNLOAD_FILE_PATH = '/home/leelab/PycharmProjects/moleculardating/result/{request_id}/{request_idx}'
DOWNLOAD_FILE_PATH = '/Users/shivankurkapoor/GitHub/moleculardating/result/{request_id}/{request_idx}'
MIME_TYPE = 'application/octet-stream'
ZIP_MIME_TYPE = 'application/zip'
DESCRIPTION = ''

'''
Dir path for html file
'''
# TEMPLATE_PATH = '/home/web/moleculardating/application/templates'
# TEMPLATE_PATH = '/home/leelab/PycharmProjects/moleculardating/application/templates'
MSG_TEMPLATE_SINGLE = 'display_template_single.html'
MSG_TEMPLATE_MULTIPLE = 'display_template_multiple.html'
TEMPLATE_PATH = '/Users/shivankurkapoor/GitHub/moleculardating/application/templates'

'''
Result dir path
'''
# RESULT_PATH = '/home/web/moleculardating/result/{request_id}/{request_idx}'
# RESULT_PATH = '/home/leelab/PycharmProjects/moleculardating/result/{request_id}/{request_idx}'
RESULT_PATH = '/Users/shivankurkapoor/GitHub/moleculardating/result/{request_id}/{request_idx}'

'''
Bash directories
'''
# BASH_SCRIPT_FASTPROCESS = '/home/web/moleculardating/bash/fastprocess/{request_id}'
# BASH_SCRIPT_PROCESS = '/home/web/moleculardating/bash/process/{request_id}'

# BASH_SCRIPT_FASTPROCESS = '/home/leelab/PycharmProjects/moleculardating/bash/fastprocess/{request_id}'
# BASH_SCRIPT_PROCESS = '/home/leelab/PycharmProjects/moleculardating/bash/process/{request_id}'

BASH_SCRIPT_FASTPROCESS = '/Users/shivankurkapoor/GitHub/moleculardating/bash/fastprocess/{request_id}'
BASH_SCRIPT_PROCESS = '/Users/shivankurkapoor/GitHub/moleculardating/bash/process/{request_id}'

'''
Bash script
'''
DOWNLOAD_SCRIPT = '/Users/shivankurkapoor/GitHub/moleculardating/scripts/download.py'
UPLOAD_SCRIPT = '/Users/shivankurkapoor/GitHub/moleculardating/scripts/fastq_to_fasta.py'
FASTQTOFASTA_SCRIPT = '/Users/shivankurkapoor/GitHub/moleculardating/scripts/upload.py'
FENV_PROCESS_SCRIPT = '/Users/shivankurkapoor/GitHub/moleculardating/scripts/FENV/main.py'
HXB_PROCESS_SCRIPT = '/Users/shivankurkapoor/GitHub/moleculardating/scripts/H4/main.py'
NGS_PROCESS_SCRIPT = '/Users/shivankurkapoor/GitHub/moleculardating/scripts/NGS/main.py'

'''
HTML result path
'''
# HTML_RESULT_PATH = '/home/web/moleculardating/application/templates/result/{request_id}'
# HTML_RESULT_PATH = '/home/leelab/PycharmProjects/moleculardating/application/templates/result/{request_id}'
HTML_RESULT_PATH = '/Users/shivankurkapoor/GitHub/moleculardating/application/templates/result/{request_id}'

'''
Email template and other parameters
'''
EMAIL = 'Thank you for using our web tool. Your results for Request Id : {request_id} have been uploaded to your Google Drive account.' \
        ' You can directly download the results here {link}'
SENDER = 'shivankurkapoor3192@gmail.com'
PASSWORD = '***********'

'''
Request Form Types
'''
SINGLE = 'single'
SANGER_SEQUNCE_DATA = 'ss'  # Sanger Sequence Data
MULTIPLE = 'multiple'
NEXT_GEN_DATA = 'ngs'  # Next Generation Sequence Data

'''
File Types
'''
FASTA = 'fasta'
FASTQ = 'fastq'

'''
Time to wait for processing
'''
DELTA = 10

'''
Fasta file folder name
'''
FASTA_DIR = 'fasta'

'''
Fastq file folder name
'''
FASTQ_DIR = 'fastq'

'''
Output folder
'''
OUTPUT_DIR = 'output'

'''
Directory for clustered files
'''
CLUSTERED_DIR = 'clustered'

'''
MISC
'''
INT_LEN_REQUEST_ID = 8
INT_TTL_GEN_ID = 10

'''
Error Codes for various purpose
'''
INT_ERROR_GENERAL = -1000
INT_ERROR_NOTEXIST = -3000
INT_ERROR_FOUND = -3001
INT_ERROR_PASSEDEXPTIME = -2000
INT_ERROR_FORMAT = -4000
INT_ERROR_TIMEOUT = -4008
INT_ERROR_MAXATTEMPTREACHED = -40080
INT_FAILURE = -1001
INT_FAILURE_AUTH = -1002
INT_FAILURE_RENEW = -1003
INT_ILLEGAL_HTTPMETHOD = -4001
INT_NOTEXISTS = 3000
INT_FOUND = 3001
INT_LOGGEDOUT = 1009
INT_OK = 0
INT_CREATED = 2001
INT_FAILURE_DOWNLOAD = -5001
INT_FAILURE_UPLOAD = -5002
INT_DOWNLOADED = 5001
INT_UPLOADED = 5002
INT_PROCESSED = 6001
INT_NOTPROCESSED = 6002
