import os
import sys
import time

from qscript_utility import *

pid = sys.argv[1]
hostname = sys.argv[2]
queue_type = sys.argv[3]
parameter = ''
assigned = ''

while assigned != pid:
    list = get_list("queue", "queue_type='%s' and processed=0 order by assign_time" % queue_type, "qid,parameter")
    if len(list) == 0: continue
    l = list[0]
    qid = l[0]
    update_record("queue", "pid=%s,hostname='%s',processed=1" % (pid, hostname), "qid=%s" % (qid))
    time.sleep(1)
    check_list = get_list("queue", "qid=%s" % qid, "pid,hostname")
    if str(check_list[0][0]) == pid and check_list[0][1] == hostname:
        parameter = l[1]
        assigned = pid

os.chdir(sys.path[0])
if queue_type == 'download':
    os.chdir('../application/server')
    os.system(sys.executable + ' filedownloader.py ' + parameter)

if queue_type == 'pipeline':
    os.chdir('../application/programs')
    os.system(sys.executable + ' bioinformaticspipeline.py ' + parameter)

if queue_type == 'taxonomy':
    os.chdir('../application/programs')
    os.system(sys.executable + ' taxonomy_annotation.py ' + parameter)

if queue_type == 'graph':
    os.chdir('../application/programs')
    os.system(sys.executable + ' graph_builder.py ' + parameter)

if queue_type == 'upload':
    os.chdir('../application/server')
    os.system(sys.executable + ' fileuploader.py ' + parameter)
