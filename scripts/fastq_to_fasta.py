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

sys.path.append('../application')
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from argparse import ArgumentParser
from database.domain.request import DatingRequest
from database import *
from common.globalfunct import *
from common.globalconst import *


MIXED_BASE = {'A' : {'A'}, 'C' : {'C'}, 'G' : {'G'}, 'T' : {'T'}, 'R' : {'A', 'G'},
              'Y' : {'C', 'T'}, 'M' : {'A', 'C'}, 'K' : {'G', 'T'}, 'S' : {'C', 'G'},
              'W' : {'A', 'T'}, 'H' : {'A', 'C', 'T'}, 'B' : {'C', 'G', 'T'},
              'V' : {'A', 'C', 'G'}, 'D' : {'A', 'G', 'T'}, 'N' : {'A', 'C', 'G', 'T'}}

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
            record = SeqRecord(Seq(item[0]), id=seqid, description='')
            SeqIO.write(record, outputfile, 'fasta')

    '''
	outputdata = ''
	for item in primer_match_list:
		firstline = '>' + id_primer_dict[item[0]] + ' ' + str(len(item[1])) + ' ' + str(count[0]) + ' ' + str(uniqueSequences) + '\n'
		outputdata += firstline
		outputdata += item[0] + '\n'
	return outputdata
	'''

#BASES = 210
#file1 = sys.argv[1]#"D12-3-10-C10-H4_S54_L001_R1_001.fastq"
#file2 = sys.argv[2]#"D12-3-10-C10-H4_S54_L001_R2_001.fastq"
#ref_seq = sys.argv[3]#"D12-3-10-C10-H4.fasta"
#file1 = "D12-3-10-C10-H4_S54_L001_R1_001.fastq"
#file2 = "D12-3-10-C10-H4_S54_L001_R2_001.fastq"
#ref_seq = "D12-3-10-C10-H4.fasta"
#file1 = "list2dicttemp1.fastq"
#file2 = "list2dicttemp2.fastq"
#file1 = "list2dicttemp1OGScores.fastq"
#file2 = "list2dicttemp2OGScores.fastq"
#file1 = "list2dictTestDeletionError1.fastq"
#file2 = "list2dictTestDeletionError2.fastq"
#file1 = "list2dictTestInsertionError1.fastq"
#file2 = "list2dictTestInsertionError2.fastq"
#file1 = "temp1.fastq"
#file2 = "temp2.fastq"
#ref_seq = "tempref.fasta"

#for fileindex in range(len(folders)):
#for fileindex in range(3):

def check_primer_match(primer, user_seq, type):
    print 'type: ', type
    print 'primer: ', primer
    print 'user_s: ', user_seq
    for i in range(len(primer)):
        if user_seq[i] in NORMAL_BASE:
            if not user_seq[i] in MIXED_BASE[primer[i]]:
                return False
        elif primer[i] in NORMAL_BASE:
            if not primer[i] in MIXED_BASE[user_seq[i]]:
                return False
        elif len(MIXED_BASE[primer[i]].intersection(MIXED_BASE[user_seq[i]])) == 0:
            return False
    print 'passed'
    print '\n'
    return True

def process_pipeline(forward_primer_seq, backward_primer_seq, seq_length, percent_seq, base_count, output_file_name, forwardFilename, backwardFilename):
    handle = open(forwardFilename)
    handle1 = open(backwardFilename)
    #handle_ref = open(ref_seq)
    '''
    handle = gzip.open(pathFile1)
    handle1 = gzip.open(pathFile2)
    handle_ref = open(pathFile3)
    '''
    records = SeqIO.parse(handle, "fastq")
    records1 = SeqIO.parse(handle1, "fastq")
    #records2 = SeqIO.parse(handle_ref,"fasta")

    rec = next(records)
    rec1 = next(records1)
    #rec2 = next(records2)

    forward_seq_records = dict()
    forward_score = dict()

    while(rec.id != ""):
        try:
            forward_seq_records[rec.id] = str(rec.seq).upper()
            forward_score[rec.id] = rec.letter_annotations['phred_quality']
            rec = next(records)
        except:
            break

    #print "forward seq records: ", forward_seq_records, '\n'
    #print "length of forward_seq_records: ", len(forward_seq_records), '\n'
    #print(forward_score)
    backward_seq_records = dict()
    backward_score = dict()
    while(rec1.id != ""):
        try:
            backward_seq_records[rec1.id] = str(rec1.seq).upper()
            backward_score[rec1.id] = rec1.letter_annotations['phred_quality']
            rec1 = next(records1)
        except:
            break

    #print(backward_score)
    #print 'backward_seq_records: ', backward_seq_records, '\n'
    #print 'length of backward_seq_records: ', len(backward_seq_records), '\n'

    ds = [forward_seq_records, backward_seq_records, forward_score, backward_score]
    seq_records = {}
    for k in forward_seq_records.iterkeys():
        seq_records[k] = tuple( seq_records[k][0:seq_length] for seq_records in ds)

    #print 'seq_records: ', seq_records, '\n'
    print 'length of seq_records: ', len(seq_records), '\n'

    collapse_dict = {}
    #collapse_lst = []
    collapseCount = 0
    qscore = []
    b_set = {}
    join_index = {}
    key_to_seq = {}
    read_number = 0
    #idDict = {}
    id_dict = {}
    for key in seq_records:

        index = str(seq_records[key][0]) + ":" + str(seq_records[key][1])
        #if index not in collapse_lst:
        #collapse_lst.append(index)
        collapseCount += 1
        if(collapse_dict.get(index) == None):
            collapse_dict[index] = [[seq_records[key][2], seq_records[key][3]]]
            id_dict[index] = key
            #idDict[index] = [key]
        else:
            collapse_dict[index].append([seq_records[key][2], seq_records[key][3]])
            #idDict[index].append(key)
    #print(collapse_dict[index])
    print "len of collapse_dict: ", len(collapse_dict)
    print 'len of id_dict: ', len(id_dict)
    print id_dict, '\n'
    '''
    templist = [len(i) for i in idDict.values()]
    maxOcuuringSeqTimes = max(templist)
    print 'idDict.items = ', maxOcuuringSeqTimes
    for i in idDict:
        if len(idDict[i]) == maxOcuuringSeqTimes:
            print idDict[i]
            print "key is: ", i
            break
    '''
    #collapse_dict_sorted = sorted(collapse_dict.items(), key = lambda x: len(x), reverse = True)
    #print collapse_dict_sorted[0]
    '''
        q1 = rec.letter_annotations['phred_quality'][:seq_length]
        print '\n\nq1: \n', q1
        q2 = rec1.letter_annotations['phred_quality'][:seq_length]
        print '\n\nq2: \n', q2
        qscore.append([q1,q2])
        print '\n\nqscore: \n', qscore
        #print(qscore)
        '''
    '''
    print 'collapse_dict: ', collapse_dict, '\n'
    print 'length of collapse_dict: ', len(collapse_dict), '\n'
    print 'collapse_lst: ', collapse_lst, '\n'
    print 'length of collapse_lst: ', len(collapse_lst), '\n'
    '''
    """
        if index in b_set.keys():
            b_set[index].add(read_number)
        else:
            b_set[index] = set()
            b_set[index].add(read_number)

        read_number += 1

    print(b_set)

    """
    #print(len(collapse_lst), len(collapse_dict))

    #Part 2
    print 'part 2'
    #join_list = []
    joinCount = 0
    join_dict = {}
    id_join_dict = {}
    for key in collapse_dict.keys():
        keys = key.split(":")
        forward = keys[0]
        backward = complementary_strand(keys[1])
        #print 'backward: ', backward
        # for i in range(len(forward), 4, -1):
        for i in range(len(forward), 2, -1):
            if(forward[-i:] == backward[:i]): #### get last i char in a and first i char in b
                #print 'forward is equal to backward for key: ', key
                '''
                print 'value of i: ', i
                print 'forward[-i:]: ', forward[-i:]
                print 'backward[:i]: ', backward[:i]
                print 'forward[-31:]: ', forward[-31:]
                print 'backward[:31]: ', backward[:31]
                '''
                index = str(forward[:-i] + backward)
                #index = str(forward[:-i] + backward) + ':' + key
                if(len(index) > 200):
                    print 'hi'
                    join_dict[index] = []
                    joinCount += len(collapse_dict[key])
                    #join_list.append(str(forward[:-i] + backward))
                    for item in collapse_dict[key]:
                        join_dict[index].append(item[0][:-i] + item[1][::-1])
                    id_join_dict[index] = id_dict[key]
                    break
                    #join_index[key] = i
                    #key_to_seq[key] = index
    print 'len of join_dict'
    print len(join_dict)
    print 'len of id_join_dict: ', len(id_join_dict)
    print id_join_dict
    #for i in join_dict:
    #    print 'seq: ', i
    #    print 'len(seq): ', len(join_dict[i])
    print '\n'
    '''
    for item in join_list:
        if(item not in join_dict):
            join_dict[item] = 1
        else:
            join_dict[item] += 1

    '''
    #print("\n\n Join Dict: \n")
    #print(join_dict)
    #print 'join_list: ', join_list, '\n'
    #print 'len of join_list: ', len(join_list), '\n'
    #print 'join_dict: ', join_dict, '\n'
    #print 'length of join_dict: ', len(join_dict), '\n'

    #print(len(join_list) , len(join_dict), len(set(join_list)))

    #*************************************************************************************************

    #Part 3
    print 'part 3'
    #print join_dict
    primer_match_list = []
    primer_match_dict = {}
    join_dict_sorted = sorted(join_dict.items(), key = lambda x: len(x[1]), reverse = True)
    id_primer_dict = {}
    #max_occurence = len(max(primer_match_dict.iteritems(), key=lambda x: len(x[1]))[1])
    #print 'join_dict_sorted: ', join_dict_sorted, '\n'
    #print 'len of join_dict_sorted: ', len(join_dict_sorted), '\n'
    element = join_dict_sorted[0][0]
    #print 'max max_occurence element is: ' + element
    #print join_dict_sorted
    max_occurence = len(join_dict_sorted[0][1])
    #print max_occurence
    second_max = 0
    if len(join_dict_sorted) > 1:
        second_max = len(join_dict_sorted[1][1])
    #print 'element: ', element, ' max_occurence: ', max_occurence, '\n'
    #first = element[:22]#rec2.seq[:22]
    #last = element[-23:]#rec2.seq[-23:]
    #print(max_occurence)
    #check if primers are given or not. If not given, then skip this step!
    if forward_primer_seq != 'NONE' and backward_primer_seq != 'NONE':
        first = forward_primer_seq.upper()
        last = complementary_strand(backward_primer_seq.upper())
        FIRST_LEN = len(first)
        LAST_LEN = len(last)

        print 'first:'
        print first
        print 'last'
        print last

        for key in join_dict.keys():
            '''
            print 'key[:22]'
            print key[:22]
            print 'key[-23:]'
            print key[-23:]
            '''
            #if(key[:FIRST_LEN]!=first or last!=key[-LAST_LEN:]):
            if not check_primer_match(first, key[:FIRST_LEN], 'Forward') or not check_primer_match(last, key[-LAST_LEN:], 'Backward'):
                #join_list.remove(item)
                if(join_dict.get(key) != None):
                    del join_dict[key]
            else:
                #primer_match_list.append(item[22:-23])
                #print 'hi'
                index = key[FIRST_LEN:-LAST_LEN]
                primer_match_dict[index] = []
                for item in join_dict[key]:
                    primer_match_dict[index].append(item[FIRST_LEN:-LAST_LEN])
                #id_primer_dict[index] = [id_join_dict[key], len(primer_match_dict[index])]
                id_primer_dict[index] = id_join_dict[key]
    else:
        print 'No primers provided'
        primer_match_dict = join_dict
        id_primer_dict = id_join_dict

    #print '\n\nPrimer Match Dict:\n ', primer_match_dict
    '''
    for item in primer_match_list:
        if item not in primer_match_dict:
            primer_match_dict[item] = 1
        else:
            primer_match_dict[item] += 1
    '''

    #print 'join_dict: ', join_dict, '\n'
    #print 'length of join_dict: ', len(join_dict), '\n'

    '''
    for i in range(0,len(join_dict_sorted)):
        if(len(join_dict_sorted[i][1]) <10):
            if(join_dict.get(join_dict_sorted[i][0]) != None):
                del join_dict[join_dict_sorted[i][0]]
    '''

    '''
    for key in primer_match_dict.keys():
        #print 'deleting keys with length less than 10'
        #print key
        #print len(primer_match_dict[key])
        if(len(primer_match_dict[key]) <= 10):
            #red_key.append(key)
            del primer_match_dict[key]
            del id_primer_dict[key]
    '''

    count = [0, 0]
    for key in primer_match_dict.keys():
        count[0] += len(primer_match_dict[key])
    print 'count: ', count

    #total_err = [0, 0]
    #total_insertion_err, total_deletion_err, total_mismatch_err = [0, 0], [0, 0], [0, 0]
    #total_reads = [0, 0]
    #errorHistogram = [{}, {}]
    #signalHistogram = [{}, {}]
    actualMaxOccurence = [0, 0]
    actualSecondMaxOccurence = [0, 0]
    #print 'len of primer_match_dict:'
    primer_match_list = sorted(primer_match_dict.items(), key = lambda x: len(x[1]), reverse = True)
    #primer_match_dict_lengths = [len(primer_match_dict[k]) for k in primer_match_dict]
    #primer_match_dict_lengths = sorted(primer_match_dict_lengths, reverse=True)
    #print 'sorted(primer_match_dict_lengths): ', primer_match_dict_lengths
    #actualMaxOccurence[0] = primer_match_dict_lengths[0]
    actualMaxOccurence[0] = len(primer_match_list[0][1])
    if len(primer_match_list) > 1:
        #actualSecondMaxOccurence[0] = primer_match_dict_lengths[1]
        actualSecondMaxOccurence[0] = len(primer_match_list[1][1])
    #actualMaxOccurence[0] = len(primer_match_dict[max(primer_match_dict, key=lambda x: len(primer_match_dict[x]))])
    #print 'actualMaxOccurence: ', actualMaxOccurence
    #print 'actualSecondMaxOccurence: ', actualSecondMaxOccurence

    #proportionMatchValues = [0, 0]
    #totalReadCountVsErrorCount = [{}, {}]

    print 'actualMaxOccurence: ', actualMaxOccurence
    #for i in range(0, length_jds):
    #print primer_match_dict
    print 'unique seq count: ', len(primer_match_dict)
    print 'actualMaxOccurence: ', actualMaxOccurence
    print 'actualSecondMaxOccurence: ', actualSecondMaxOccurence

    ####filter condition 4: Remove sequences with copies less than x% of the copies of maximum occuring sequence
    if percent_seq > 0:
        for i in range(len(primer_match_list)):
            if not (len(primer_match_list[i][1]) * 1.0 / actualMaxOccurence[0]) * 100 >= percent_seq:
                del primer_match_dict[primer_match_list[i][0]]
                del id_primer_dict[primer_match_list[i][0]]
        primer_match_list = sorted(primer_match_dict.items(), key = lambda x: len(x[1]), reverse = True)
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

        primer_match_list = sorted(primer_match_rem_scores_less_than_basecount.items(), key = lambda x: len(x[1]), reverse = True)
        count = [0, 0]
        for key in primer_match_rem_scores_less_than_basecount.keys():
            count[0] += len(primer_match_rem_scores_less_than_basecount[key])
        print 'count: ', count
        print 'primer_match_rem_scores_less_than_basecount: ', len(primer_match_rem_scores_less_than_basecount)
        print 'id count: ', len(id_primer_dict)
    #print 'id_primer_dict: ', id_primer_dict
    #OUTPUTFILE = forwardFilename.replace('fastq', 'fasta')
    output(output_file_name, primer_match_list, id_primer_dict, count)
    #print(count, len(join_dict))

    #print("Proportion match : " + str((float(max_occurence)/count) * 100))
    #print("Maximum Proportion : " + str((float(second_max)/max_occurence)*100))
    #print join_dict
    #primer_dict_sorted = sorted(primer_match_dict.items(), key = operator.itemgetter(1), reverse = True)
    #print 'primer_dict_sorted before NW: ', primer_dict_sorted, '\n'
    #element = primer_dict_sorted[0]
    #length_jds = len(primer_dict_sorted)
    #if len(primer_match_dict) == 0:
    #    continue
    #*******************************************************************************************

    #modified.close()


    #*******************************************************************************************************

    handle.close()
    handle1.close()
    #return outputdata



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
                if dating_request.form_type == SINGLE:
                    script_path = BASH_SCRIPT_FASTPROCESS.format(request_id=args.request_id)
                    html_result_dir = HTML_RESULT_PATH.format(request_id=args.request_id)
                    write_bash_file(script_path, script_name, command=command, request_id=args.request_id,
                                    request_idx=args.request_idx, input_dir=input_dir, html_dir=html_result_dir)

                elif dating_request.form_type == MULTIPLE:
                    script_path = BASH_SCRIPT_PROCESS.format(request_id=args.request_id)
                    write_bash_file(script_path, script_name, command=command, request_id=args.request_id,
                                    request_idx=args.request_idx, input_dir=input_dir)



    except Exception as e:
        print 'Error in updating database in fastq to fasta processing ', e

    finally:
        db.close()
