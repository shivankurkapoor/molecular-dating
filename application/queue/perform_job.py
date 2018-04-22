from qscript_utility import *
import os
import sys

qid = sys.argv[1]
list = get_list("queue", "qid=%s " % qid, "queue_type,parameter")
l = list[0]
params = l[1].split(' ', 3)
parameter = ' '
if len(params) == 4:
    parameter = params[3]
idx = params[2]
request_id = params[1]
queue_type = params[0]

update_record('queue', "processed=1", 'qid=%s' % qid)

os.chdir(sys.path[0])
if queue_type == 'fenv':
    os.chdir('../../bash_scripts')
    os.system('bash FENV.sh %s %s' % (request_id, idx))

if queue_type == 'hxb2':
    os.chdir('../../bash_scripts')
    os.system('bash HXB2.sh %s %s' % (request_id, idx))

if queue_type == 'q2a':
    os.chdir('../../scripts')
    os.system(
        sys.executable + ' fastq_to_fasta.py --request_id=%s --request_idx=%s --output_dir=/home/spark/moleculardating/result/%s/%s/fasta ' % (
        request_id, idx, request_id, idx) + parameter)

if queue_type == 'ngs':
    os.chdir('../../bash_scripts')
    os.system('bash NGS.sh %s %s' % (request_id, idx))

if queue_type == 'graph':
    os.chdir('../programs')
    os.system(sys.executable + ' graph_builder.py ' + parameter)

if queue_type == 'upload':
    os.chdir('../server')
    os.system(sys.executable + ' fileuploader.py ' + parameter)

update_record('queue', "processed=2", 'qid=%s' % qid)
