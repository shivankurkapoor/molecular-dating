#append these paths to sys required for bash script files - it appends the path to application directory to sys
import sys
sys.path.append('../')

from application.database import *
from application.database.domain import DatingRequest
from application.database.domain import User

try:
    db_connect()
    db.create_tables([User, DatingRequest])
    db_disconnect()
except Exception as e:
    print 'Error while creating schemas ',e
