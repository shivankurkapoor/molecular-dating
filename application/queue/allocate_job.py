import sys
import time

from qscript_utility import *

pid = sys.argv[1]
hostname = sys.argv[2]
queue_type = sys.argv[3]
parameter = ''
# gpu_id=''
# with open('allocate_gpu.log',"a") as f, redirect_stdout(f):
assigned = ''
while assigned != pid:
    list = get_list("queue", "queue_type='%s' and processed=0 order by assign_time" % queue_type, "qid,parameter")
    if len(list) == 0: continue
    l = list[0]
    qid = l[0]
    # print "Trying to allocate qid %s at pid %s at %s"%(qid,pid,hostname)," %s"%datetime.now()
    update_record("queue", "pid=%s,hostname='%s',processed=1" % (pid, hostname), "qid=%s" % (qid))
    time.sleep(3)
    check_list = get_list("queue", "qid=%s" % qid, "pid,hostname")
    if str(check_list[0][0]) == pid and check_list[0][1] == hostname:
        parameter = l[1]
        # print "Allocation has been done at pid %s of %s for qid=%s."%(pid,hostname,qid)," %s"%datetime.now()
        assigned = pid

os.system("echo %s" % (pid))
