#append these paths to sys required for bash script files - it appends the path to application directory to sys
import sys
#sys.path.append('../')

from database import *
from database.domain.request import DatingRequest
from database.domain.user import User

try:
    db.connect()
    db.create_tables([User, DatingRequest])
except Exception as e:
    print 'Error while creating schemas',e
finally:
    db.close()