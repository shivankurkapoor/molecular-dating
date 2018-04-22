from qscript_utility import *
import sys

if len(sys.argv) != 5:
    exit()
(tablename, id_num, column, value) = sys.argv[1:5]
if tablename == 'queue':
    update_record(tablename, "%s=%s" % (column, value), 'qid=%s' % id_num)
