'''
This is the same as bioinformaticspipeline.py except that it can check mixed base primer sequences!
The following is the universal nomenclature followed for mixed bases:
Symbol	Mixed Bases
R	        A,G
Y	        C,T
M	        A,C
K	        G,T
S	        C,G
W	        A,T
H	        A,C,T
B	        C,G,T
V	        A,C,G
D	        A,G,T
N	        A,C,G,T
'''
import sys

sys.path.append('/home/spark/moleculardating/application')

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from argparse import ArgumentParser
from database.domain.request import DatingRequest
from database import *
from common.globalfunct import *
from common.globalconst import *
import string
import queue.qscript_utility

MIXED_BASE = {'A': {'A'}, 'C': {'C'}, 'G': {'G'}, 'T': {'T'}, 'R': {'A', 'G'},
              'Y': {'C', 'T'}, 'M': {'A', 'C'}, 'K': {'G', 'T'}, 'S': {'C', 'G'},
              'W': {'A', 'T'}, 'H': {'A', 'C', 'T'}, 'B': {'C', 'G', 'T'},
              'V': {'A', 'C', 'G'}, 'D': {'A', 'G', 'T'}, 'N': {'A', 'C', 'G', 'T'}}

NORMAL_BASE = {'A', 'C', 'G', 'T'}


def complementary_strand(strand):
    comple = strand.translate(string.maketrans('TAGCtagc', 'ATCGATCG'))
    return comple[::-1]


def output(output_file_name, primer_match_list, id_primer_dict, count):
    uniqueSequences = len(id_primer_dict)
    with open(output_file_name, 'w') as outputfile:
        for item in primer_match_list:
            '''
            The id for each sequence contains the following items:
            (original_id):(number of copies of this sequence):(total number of sequences):(total number of unique sequences)
            '''
            seqid = id_primer_dict[item[0]] + ':' + str(len(item[1])) + ':' + str(count[0]) + ':' + str(uniqueSequences)
            '''
            Putting duplicate sequences
            '''
            for i in range(len(item[1])):
                seqid_ = seqid + ':' + str(i)
                record = SeqRecord(Seq(item[0]), id=seqid, description='')
                SeqIO.write(record, outputfile, 'fasta')


def check_primer_match(primer, user_seq, type):
    for i in range(len(primer)):
        if not user_seq[i] in MIXED_BASE[primer[i]]:
            return False
    return True


def process_pipeline(forward_primer_seq, backward_primer_seq, seq_length, percent_seq, base_count, output_file_name,
                     forwardFilename, backwardFilename):
    handle = open(forwardFilename)
    handle1 = open(backwardFilename)
    records = SeqIO.parse(handle, "fastq")
    records1 = SeqIO.parse(handle1, "fastq")
    rec = next(records)
    rec1 = next(records1)
    forward_seq_records = dict()
    forward_score = dict()

    while (rec.id != ""):
        try:
            forward_seq_records[rec.id] = str(rec.seq).upper()
            forward_score[rec.id] = rec.letter_annotations['phred_quality']
            rec = next(records)
        except:
            break

    backward_seq_records = dict()
    backward_score = dict()
    while (rec1.id != ""):
        try:
            backward_seq_records[rec1.id] = str(rec1.seq).upper()
            backward_score[rec1.id] = rec1.letter_annotations['phred_quality']
            rec1 = next(records1)
        except:
            break

    ds = [forward_seq_records, backward_seq_records, forward_score, backward_score]
    seq_records = {}
    for k in forward_seq_records.iterkeys():
        seq_records[k] = tuple(seq_records[k][0:seq_length] for seq_records in ds)

    print 'length of seq_records: ', len(seq_records), '\n'

    collapse_dict = {}
    collapseCount = 0
    id_dict = {}
    for key in seq_records:

        index = str(seq_records[key][0]) + ":" + str(seq_records[key][1])
        collapseCount += 1
        if (collapse_dict.get(index) == None):
            collapse_dict[index] = [[seq_records[key][2], seq_records[key][3]]]
            id_dict[index] = key
        else:
            collapse_dict[index].append([seq_records[key][2], seq_records[key][3]])
    print "len of collapse_dict: ", len(collapse_dict)
    print 'len of id_dict: ', len(id_dict)

    # Part 2
    print 'part 2'
    joinCount = 0
    join_dict = {}
    id_join_dict = {}
    for key in collapse_dict.keys():
        keys = key.split(":")
        forward = keys[0]
        backward = complementary_strand(keys[1])
        for i in range(len(forward), 2, -1):
            if (forward[-i:] == backward[:i]):  #### get last i char in a and first i char in b
                index = str(forward[:-i] + backward)
                if (len(index) > 200):
                    if index not in join_dict:
                        join_dict[index] = []
                        id_join_dict[index] = id_dict[key]

                    joinCount += len(collapse_dict[key])
                    for item in collapse_dict[key]:
                        join_dict[index].append(item[0][:-i] + item[1][::-1])
                    break
    print 'len of join_dict'
    print len(join_dict)
    print 'len of id_join_dict: ', len(id_join_dict)
    print '\n'

    # *************************************************************************************************
    # Part 3
    print 'part 3'
    primer_match_dict = {}
    join_dict_sorted = sorted(join_dict.items(), key=lambda x: len(x[1]), reverse=True)
    id_primer_dict = {}
    if len(join_dict_sorted) > 1:
        second_max = len(join_dict_sorted[1][1])
    if forward_primer_seq != 'NONE' and backward_primer_seq != 'NONE':
        first = forward_primer_seq.upper()
        last = complementary_strand(backward_primer_seq.upper())
        FIRST_LEN = len(first)
        LAST_LEN = len(last)

        for key in join_dict.keys():
            if not check_primer_match(first, key[:FIRST_LEN], 'Forward') or not check_primer_match(last,
                                                                                                   key[-LAST_LEN:],
                                                                                                   'Backward'):
                if (join_dict.get(key) != None):
                    del join_dict[key]
            else:
                index = key[FIRST_LEN:-LAST_LEN]
                if index not in primer_match_dict:
                    primer_match_dict[index] = []
                    id_primer_dict[index] = id_join_dict[key]

                for item in join_dict[key]:
                    primer_match_dict[index].append(item[FIRST_LEN:-LAST_LEN])
    else:
        print 'No primers provided'
        primer_match_dict = join_dict
        id_primer_dict = id_join_dict

    for i in range(0, len(join_dict_sorted)):
        if (len(join_dict_sorted[i][1]) < 10):
            if (join_dict.get(join_dict_sorted[i][0]) != None):
                del primer_match_dict[join_dict_sorted[i][0]]
                del id_primer_dict[join_dict_sorted[i][0]]

    count = [0, 0]
    for key in primer_match_dict.keys():
        count[0] += len(primer_match_dict[key])
    print 'count: ', count

    actualMaxOccurence = [0, 0]
    actualSecondMaxOccurence = [0, 0]
    primer_match_list = sorted(primer_match_dict.items(), key=lambda x: len(x[1]), reverse=True)
    actualMaxOccurence[0] = len(primer_match_list[0][1])
    if len(primer_match_list) > 1:
        actualSecondMaxOccurence[0] = len(primer_match_list[1][1])
    print 'actualMaxOccurence: ', actualMaxOccurence
    print 'unique seq count: ', len(primer_match_dict)
    print 'actualMaxOccurence: ', actualMaxOccurence
    print 'actualSecondMaxOccurence: ', actualSecondMaxOccurence

    ####filter condition 4: Remove sequences with copies less than x% of the copies of maximum occuring sequence
    if percent_seq > 0:
        for i in range(len(primer_match_list)):
            if not (len(primer_match_list[i][1]) * 1.0 / actualMaxOccurence[0]) * 100 >= percent_seq:
                del primer_match_dict[primer_match_list[i][0]]
                del id_primer_dict[primer_match_list[i][0]]
        primer_match_list = sorted(primer_match_dict.items(), key=lambda x: len(x[1]), reverse=True)
        count = [0, 0]
        for key in primer_match_dict.keys():
            count[0] += len(primer_match_dict[key])
        print 'count: ', count

    ####filter condition 5: Remove sequences which have at least one base less than the given score
    if base_count > 0:
        primer_match_rem_scores_less_than_basecount = {}
        for key in primer_match_dict.keys():
            deleteflag = True
            for scores in primer_match_dict[key]:
                if all(i >= base_count for i in scores):
                    deleteflag = False
                    if key in primer_match_rem_scores_less_than_basecount:
                        primer_match_rem_scores_less_than_basecount[key].append(scores)
                    else:
                        primer_match_rem_scores_less_than_basecount[key] = []
                        primer_match_rem_scores_less_than_basecount[key].append(scores)
            if deleteflag:
                del id_primer_dict[key]

        primer_match_list = sorted(primer_match_rem_scores_less_than_basecount.items(), key=lambda x: len(x[1]),
                                   reverse=True)
        count = [0, 0]
        for key in primer_match_rem_scores_less_than_basecount.keys():
            count[0] += len(primer_match_rem_scores_less_than_basecount[key])
        print 'count: ', count
        print 'primer_match_rem_scores_less_than_basecount: ', len(primer_match_rem_scores_less_than_basecount)
        print 'id count: ', len(id_primer_dict)

    output(output_file_name, primer_match_list, id_primer_dict, count)
    # *******************************************************************************************************
    handle.close()
    handle1.close()


def process_fastq(output_dir, forward_file, backward_file, fps, bps, seq_len, percent, base_count, request_id,
                  request_idx):
    output_file_name = request_id + '_' + str(request_idx) + '.fasta'
    output_file_name = os.path.join(output_dir, output_file_name)
    process_pipeline(fps, bps, seq_len, percent, base_count, output_file_name, forward_file, backward_file)


if __name__ == '__main__':
    parser = ArgumentParser(description="Fastq to Fasta processing")

    '''
    Defining arguments
    '''
    parser.add_argument("--forward_primer", dest="forward_primer", default="")
    parser.add_argument("--backward_primer", dest="backward_primer", default="")
    parser.add_argument("--seq_len", dest="seq_len", default="")
    parser.add_argument("--base_count", dest="base_count", default="")
    parser.add_argument("--percent", dest="percent", default="")
    parser.add_argument("--forward_file", dest="forward_file", default="")
    parser.add_argument("--backward_file", dest="backward_file", default="")
    parser.add_argument("--request_id", dest="request_id", default="")
    parser.add_argument("--output_dir", dest="output_dir", default="")
    parser.add_argument("--request_idx", dest="request_idx", default="")

    '''
    Parsing Arguments
    '''
    args = parser.parse_args()

    print args.forward_primer
    print args.backward_primer
    print args.seq_len
    print args.base_count
    print args.percent
    print args.forward_file
    print args.backward_file
    print args.request_id
    print args.output_dir
    print args.request_idx

    try:
        assert args.seq_len != ""
        assert args.base_count != ""
        assert args.percent != ""
        assert args.forward_file != ""
        assert args.backward_file != ""
        assert args.request_id != ""
        assert args.output_dir != ""
        assert args.request_idx != ""

    except AssertionError as e:
        print e
        sys.exit()

    try:
        forward_primer = 'NONE' if args.forward_primer == "" else args.forward_primer
        backward_primer = 'NONE' if args.backward_primer == "" else args.backward_primer
        if not os.path.exists(args.output_dir):
            os.makedirs(args.output_dir)
        process_fastq(args.output_dir, args.forward_file, args.backward_file, forward_primer, backward_primer,
                      int(args.seq_len), float(args.percent), int(args.base_count), args.request_id, args.request_idx)

    except Exception as e:
        print 'Error in fastq to fasta processing'
        raise

    try:
        db.connect()
    except Exception as e:
        print 'Error in opening database'
        sys.exit(1)

    try:
        with db.atomic():
            request_query_res = DatingRequest.select().where(DatingRequest.request_id == str(args.request_id))
            if request_query_res:
                dating_request = request_query_res[0]
                form_data = json_decode(str(dating_request.form_data))
                form_data['requests'][int(args.request_idx)]['fastqtofasta'] = True

                # Updating form
                query_form_update = DatingRequest.update(form_data=str(json_encode(form_data))).where(
                    DatingRequest.request_id == args.request_id)
                query_form_update.execute()

                # Generating bash script for processing
                command = 'python ' + NGS_PROCESS_SCRIPT
                script_name = 'NGS_' + args.request_id + '_' + str(args.request_idx)
                input_dir = RESULT_PATH.format(request_id=args.request_id, request_idx=str(args.request_idx))

                script_path = None
                db.close()
                if dating_request.form_type == SINGLE:
                    script_path = BASH_SCRIPT_FASTPROCESS.format(request_id=args.request_id)
                    html_result_dir = HTML_RESULT_PATH.format(request_id=args.request_id)
                    queue.qscript_utility.submit_job_into_queue("single", args.request_id, "%s %s %s" % (
                        "ngs", args.request_id, str(args.request_idx)))
                    write_bash_file(script_path, script_name, command=command, request_id=args.request_id,
                                    request_idx=args.request_idx, input_dir=input_dir, html_dir=html_result_dir)
                    sys.exit()

                elif dating_request.form_type == MULTIPLE:
                    script_path = BASH_SCRIPT_PROCESS.format(request_id=args.request_id)
                    write_bash_file(script_path, script_name, command=command, request_id=args.request_id,
                                    request_idx=args.request_idx, input_dir=input_dir)



    except Exception as e:
        print 'Error in updating database in fastq to fasta processing ', e

    finally:
        db.close()
