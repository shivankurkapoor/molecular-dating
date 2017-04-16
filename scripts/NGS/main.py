'''
Author : Shivankur Kapoor
Contact : kapoors@usc.edu
Description: This is the main script which call all other scripts in the run and generates all the data
'''

import matplotlib
import pandas as pd
import glob
import sys

matplotlib.use('Agg')
import sys

sys.path.append('/Users/shivankurkapoor/GitHub/moleculardating/application')
import matplotlib.pyplot as plt

from Bio import SeqIO
from scipy.stats.stats import pearsonr
from clustering import clustering
from gen_data import generate_div_gsi_var
from utilityfunc import *
from stats import *
from hddistribution import hd_distribution
from htmlgen import create_html
from Bio.Alphabet import DNAAlphabet
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from collections import OrderedDict
from argparse import ArgumentParser
from database import *
from database.domain.request import DatingRequest
from common.globalfunct import *
from common.globalconst import *


def process(INPUT, OUTPUT, GSI, DIVERSITY, VAR, REPORT, TYPE, GSI_NUM, CLUSTERED=False):
    '''
    :param INPUT: input directory containing fasta files
    :param OUTPUT: output directory in which output data is generated
    :param GSI: path of the gsi file
    :param DIVERSITY: path of the diversity.npy file
    :param VAR path of var .npy file
    :param REPORT: name of the report file
    :param TYPE: type of run
    :param GSI_NUM: type of gsi
    :param CLUSTERED: if clustered or not
    :return: None
    '''
    subject_dict = dict()
    stats_dict = dict()
    final_stats_dict_list = []
    final_stats_dict = {}
    try:
        file_paths = glob.glob(INPUT + '/*fasta')
        file_paths = sorted(file_paths)
        for file_path in file_paths:
            file_name = file_path.split(os.sep)[-1]
            subname = file_name.split('-')[0] if TYPE == 'longi' else file_name.split('.')[0]
            if subname not in subject_dict:
                subject_dict[subname] = []
            subject_dict[subname].append(file_path)
    except Exception as e:
        print e

    for subject, files_paths in subject_dict.items():
        stats_dict[subject] = {}
        final_stats_dict[subject] = {}
        for file in files_paths:
            seq_dict = OrderedDict()
            time = float(file.split('/')[-1].rsplit('.', 1)[0].split('-')[2][3:]) if TYPE == 'longi' else 1000
            fasta_sequences = SeqIO.parse(open(file), 'fasta')
            for fasta in fasta_sequences:
                name, sequence = fasta.id, str(fasta.seq)
                seq_dict[name] = sequence

            seq_list = [seq for seq in seq_dict.values()]
            num_seq = len(seq_list)
            stats_dict[subject][time] = {}
            final_stats_dict[subject][time] = {}
            final_stats_dict[subject][time]['num_seq'] = len(seq_list)
            final_stats_dict[subject][time]['type'] = TYPE
            stats_dict[subject][time]['seq'] = num_seq

    # Calculating GSI
    df = pd.read_csv(GSI, sep="\t", header=0)
    df = df[['File Name', GSI_NUM]]
    for index, row in df.iterrows():
        subject = row['File Name'].split('-')[0] if TYPE == 'longi' else row['File Name'].split('.')[0]
        time = row['File Name'].split('-')[2][3:] if TYPE == 'longi' else 1000
        gsi = float(row[GSI_NUM])
        final_stats_dict[subject][float(time)]['gsi'] = gsi

    # Calculating Diversity
    diversity_dict = dict(np.load(DIVERSITY).item())
    for subject, dic in diversity_dict.items():
        for time, diversity in dic.items():
            final_stats_dict[subject][float(time)]['diversity'] = diversity

    # Calculating Variance
    var_dict = dict(np.load(VAR).item())
    for subject, dic in var_dict.items():
        for time, var in dic.items():
            final_stats_dict[subject][float(time)]['var_se'] = var

    # Creating final_stats_dict_list
    for subject, dic1 in final_stats_dict.items():
        for time, dic2 in dic1.items():
            if not CLUSTERED:
                final_stats_dict_list.append({'#SUBJECT': subject,
                                              'TIME': time,
                                              'TYPE': dic2['type'],
                                              'DIVERSITY': dic2['diversity'],
                                              'GSI': dic2['gsi'],
                                              'NUM_SEQ': dic2['num_seq'],
                                              'VAR': dic2['var_se'],
                                              'BETA': (float(dic2['var_se']) / float(dic2['diversity'])) if float(
                                                  dic2['diversity']) != 0 else 1})
            else:
                final_stats_dict_list.append({'#SUBJECT': subject,
                                              'TIME': time,
                                              'TYPE': dic2['type'],
                                              'EFFECTIVE_DIVERSITY': dic2['diversity'],
                                              'EFFECTIVE_GSI': dic2['gsi'],
                                              'NUM_SEQ(After Clustering)': dic2['num_seq'],
                                              'VAR(After Clustering)': dic2['var_se'],
                                              'BETA(After Clustering)': (
                                                  float(dic2['var_se']) / float(dic2['diversity'])) if float(
                                                  dic2['diversity']) != 0 else 1,
                                              'CLUSTERED': 'YES'}, )
    df = pd.DataFrame(final_stats_dict_list)
    df.to_csv(OUTPUT + os.sep + REPORT, index=False)

    if not CLUSTERED:
        corr_data = [(each['TIME'], each['DIVERSITY']) for each in final_stats_dict_list]
    else:
        corr_data = [(each['TIME'], each['EFFECTIVE_DIVERSITY']) for each in final_stats_dict_list]
    corr_data = sorted(corr_data, key=lambda x: x[0])
    x, y = zip(*corr_data)[0], zip(*corr_data)[1]
    corr_coeff = pearsonr(x, y)
    print 'Correlation Coefficients : ', corr_coeff


def genoutput(CLUSTER_DATA, FILE1, FILE2, OUTPUT, FINAL_REPORT, COLS, THRESHOLD_GSI):
    '''
     Merge clustered csv data file with unclustered data csv file
    :param FILE1: clustered csv file
    :param FILE2: unclustered csv file
    :param OUTPUT: output directory
    :param FINAL_REPORT: name of the final report file
    :param COLS: list of columns
    :param THRESHOLD_GSI:
    :return:
    '''
    clustered_df = pd.read_csv(FILE1, header=0, dtype={"#SUBJECT": "string"})
    unclustered_df = pd.read_csv(FILE2, header=0, dtype={"#SUBJECT": "string"})
    clusterdata_df = pd.read_csv(CLUSTER_DATA, header=0, dtype={"SUBJECT": "string"})
    clusterdata_df = clusterdata_df[['#SUBJECT', 'TIME', 'CLUSTERS']]
    merged_df = unclustered_df.merge(clustered_df, on=['#SUBJECT', 'TIME', 'TYPE'], how='inner')
    merged_df = merged_df.merge(clusterdata_df, on=['#SUBJECT', 'TIME'], how='inner')
    merged_df = merged_df.sort_values(['#SUBJECT', 'TIME'], ascending=[True, True])
    merged_df = merged_df[COLS]
    for index, row in merged_df.iterrows():
        if int(row['CLUSTERS']) == 1:
            merged_df.set_value(index, 'CLUSTERED', 'NO')

    if not os.path.exists(OUTPUT):
        os.makedirs(OUTPUT)
    df_sub = merged_df[
        ['#SUBJECT', 'TIME', 'EFFECTIVE_DIVERSITY', 'EFFECTIVE_GSI', 'VAR(After Clustering)', 'CLUSTERED', 'DIVERSITY',
         'VAR', 'GSI']]
    merged_df.to_csv(OUTPUT + os.sep + FINAL_REPORT + '.txt', sep='\t', index=False)
    merged_df.to_csv(OUTPUT + os.sep + FINAL_REPORT, index=False)

    '''
    Estimating time interval based on prediction interval coefficients
    '''
    records = []
    for index, row in df_sub.iterrows():
        subject = str(row['#SUBJECT'])
        time = float(row['TIME'])
        eff_div = float(row['EFFECTIVE_DIVERSITY'])
        time_fit = float(FIT_SLOPE) * eff_div + float(FIT_INTERCEPT)
        time_lower = float(LOWER_SLOPE) * eff_div + float(LOWER_INTERCEPT)
        time_lower = 0 if time_lower < 0 else time_lower
        time_upper = float(UPPER_SLOPE) * eff_div + float(UPPER_INTERCEPT)
        days_since_infection = '{tf} [{tl} - {tu}] days'.format(tf=str(round(time_fit, 1)),
                                                                tl=str(round(time_lower, 1)),
                                                                tu=str(round(time_upper,
                                                                             1))) if eff_div <= EFFECTIVE_DIVERSITY_TH else 'Chronic sample (>2 years)'
        records.append({'#SUBJECT': subject,
                        'TIME': time,
                        'Single Lineage Diversity': str(round(eff_div, 3)),
                        'Single Lineage GSI': str(round(float(row['EFFECTIVE_GSI']), 3)),
                        'Single Lineage Variance': str(round(float(row['VAR(After Clustering)']), 3)),
                        'Diversity': str(round(float(row['DIVERSITY']), 3)),
                        'GSI': str(round(float(row['GSI']), 3)),
                        'Variance': str(round(float(row['VAR']), 3)),
                        'CLUSTERED': str(row['CLUSTERED']),
                        'Days Since Infection': days_since_infection})
    df_predintervals = pd.DataFrame(records)
    df_predintervals = df_predintervals[
        ['#SUBJECT', 'TIME', 'Single Lineage Diversity', 'Single Lineage GSI', 'Single Lineage Variance', 'Diversity',
         'GSI', 'Variance', 'CLUSTERED', 'Days Since Infection']]
    df_predintervals.to_csv(OUTPUT + os.sep + PRED_INTERVAL_FILE, index=False)
    df_predintervals.to_csv(OUTPUT + os.sep + PRED_INTERVAL_TXT_FILE, index=False, sep='\t')


def plot(file, OUTPUT, PLOTFILE):
    df = pd.read_csv(file, index_col=False, dtype={"#SUBJECT": "string"})
    time = map(lambda x: float(x), list(df.TIME))
    diversity = map(lambda x: float(x), list(df.DIVERSITY))
    effective_diversity = map(lambda x: float(x), list(df.EFFECTIVE_DIVERSITY))
    data = sorted(zip(time, diversity, effective_diversity), key=lambda x: x[0])
    data = zip(*data)
    plt.scatter(data[0], data[1], color='Red', label='Before clustering')
    plt.scatter(data[0], data[2], color='Blue', label='After clustering')
    plt.xlabel('Time')
    plt.ylabel('Diversity')
    plt.title('Time vs Diversity')
    plt.legend()
    plt.savefig(OUTPUT + os.sep + PLOTFILE, dpi=400)


def clean_directories(DIRS):
    for dir in DIRS:
        if not os.path.exists(dir):
            os.makedirs(dir)
        else:
            files = glob.glob(dir + '/*')
            for f in files:
                if not os.path.isdir(f):
                    os.remove(f)


def clean_fasta_files(INPUT, OUTPUT):
    try:
        file_paths = glob.glob(INPUT + '/*fasta')
        file_paths = sorted(file_paths)
        for file in file_paths:
            rec_list = []
            seq_dict = {}
            filename = file.split('/')[-1]
            print filename
            fasta_sequences = SeqIO.parse(open(file), 'fasta')
            for fasta in fasta_sequences:
                name, sequence = fasta.id, str(fasta.seq)
                seq_dict[name + random_string(9)] = clean_seqeunce(sequence)

            for seq_id, seq in seq_dict.iteritems():
                rec = SeqRecord(Seq(seq, DNAAlphabet), id=seq_id, description='')
                rec_list.append(rec)
            SeqIO.write(rec_list, OUTPUT + '/' + filename, "fasta")
    except Exception as e:
        print 'Error in cleaning fasta files', e
        sys.exit(1)


if __name__ == '__main__':
    from utils import *

    '''
    Reading input parameters
    '''
    parser = ArgumentParser(description="FENV Process")

    '''
    Defining arguments
    '''
    parser.add_argument("--align", dest="align", default="")
    parser.add_argument("--request_id", dest="request_id", default="")
    parser.add_argument("--input_dir", dest="input_dir", default="")
    parser.add_argument("--request_idx", dest="request_idx", default="")
    parser.add_argument("--html_dir", dest="html_dir", default="")

    '''
    Parsing Arguments
    '''
    args = parser.parse_args()

    print args.align
    print args.request_id
    print args.input_dir
    print args.request_idx
    print args.html_dir

    try:
        assert args.request_id != ""
        assert args.input_dir != ""
        assert args.request_idx != ""
    except AssertionError as e:
        print e
        sys.exit(1)

    '''
    Updating Paths
    '''
    INPUT = os.path.join(args.input_dir, INPUT)
    INPUT_UNCLUSTERED = os.path.join(args.input_dir, INPUT_UNCLUSTERED)
    INPUT_CLUSTERED = os.path.join(args.input_dir, INPUT_CLUSTERED)
    OUTPUT = os.path.join(args.input_dir, OUTPUT)
    GSI_UNCLUSTERED = INPUT_UNCLUSTERED + os.sep + GSI_FILE
    GSI_CLUSTERED = INPUT_CLUSTERED + os.sep + GSI_FILE
    DIVERSITY_UNCLUSTERED = INPUT_UNCLUSTERED + os.sep + DIVERSITY_FILE
    DIVERSITY_CLUSTERED = INPUT_CLUSTERED + os.sep + DIVERSITY_FILE
    HD_UNCLUSTERED = INPUT_UNCLUSTERED + os.sep + HD_FILE
    HD_CLUSTERED = INPUT_CLUSTERED + os.sep + HD_FILE
    VAR_UNCLUSTERED = INPUT_UNCLUSTERED + os.sep + VAR_FILE
    VAR_CLUSTERED = INPUT_CLUSTERED + os.sep + VAR_FILE
    REQUEST_TYPE = 'SINGLE'

    if args.html_dir:
        HTML_OUTPUT = args.html_dir
    else:
        HTML_OUTPUT = OUTPUT
        REQUEST_TYPE = 'MULTIPLE'
    if args.align == 'True':
        ALIGN = True

    print 'Cleaning Directories'
    clean_directories([INPUT_CLUSTERED, OUTPUT, INPUT_UNCLUSTERED])

    TYPE = TYPE.strip().lower()
    assert TYPE == 'longi' or TYPE == 'chronic'

    '''
    Clean fasta files
    '''
    print '\n\nCleaning the fasta files'
    clean_fasta_files(INPUT=INPUT, OUTPUT=INPUT_UNCLUSTERED)

    '''
    Parameter dict for sequence alignment
    '''
    alignment_param = {'ms': MS,
                       'q': Q,
                       'r': R,
                       'l': L,
                       'b': B}

    try:
        '''
        Calculating gsi, variance and diversity for un-clustered data
        '''
        print '\n\nGenerating diversity, gsi and variance for unclustered data'
        generate_div_gsi_var(INPUT=INPUT_UNCLUSTERED, OUTPUT_DIVERSITY=DIVERSITY_UNCLUSTERED,
                             OUTPUT_GSI=GSI_UNCLUSTERED,
                             OUTPUT_VAR=VAR_UNCLUSTERED, OUTPUT_HD=HD_UNCLUSTERED, TYPE=TYPE, GAPS_IGNORE=GAPS_IGNORE,
                             **alignment_param)

        '''
        Performing clustering
        '''
        print '\n\nPerforming clustering with Threshold=', THRESHOLD
        print 'Clustering Threshold = ', THRESHOLD
        clustering(INPUT=INPUT_UNCLUSTERED, OUTPUT=INPUT_CLUSTERED, GSI_FILE=GSI_UNCLUSTERED, THRESHOLD=THRESHOLD,
                   DIVERSITY_THRESHOLD=DIVERSITY_THRESHOLD, GSI_THRESHOLD=THRESHOLD_GSI, SEQ_THRESHOLD=THRESHOLD_NUMSEQ,
                   TYPE=TYPE, FINALOUTPUT=OUTPUT, GSI_NUM=GSI_NUM)

        '''
        Calculating gsi, variance and diversity for clustered data
        '''
        print '\n\nGenerating diversity, gsi and variance for clustered data'
        generate_div_gsi_var(INPUT=INPUT_CLUSTERED, OUTPUT_DIVERSITY=DIVERSITY_CLUSTERED, OUTPUT_GSI=GSI_CLUSTERED,
                             OUTPUT_VAR=VAR_CLUSTERED, OUTPUT_HD=HD_CLUSTERED, TYPE=TYPE, GAPS_IGNORE=GAPS_IGNORE,
                             **alignment_param)

        '''
        Generating report files for clustered and unclustered data
        '''
        print '\n\nGenerating report file for unclustered data....'
        process(INPUT=INPUT_UNCLUSTERED, OUTPUT=INPUT_UNCLUSTERED, GSI=GSI_UNCLUSTERED, REPORT=REPORT,
                DIVERSITY=DIVERSITY_UNCLUSTERED, VAR=VAR_UNCLUSTERED, TYPE=TYPE, GSI_NUM=GSI_NUM, CLUSTERED=False)
        print '\n\nGenerating report file for clustered data....'
        process(INPUT=INPUT_CLUSTERED, OUTPUT=INPUT_CLUSTERED, GSI=GSI_CLUSTERED, REPORT=REPORT,
                DIVERSITY=DIVERSITY_CLUSTERED, VAR=VAR_CLUSTERED, TYPE=TYPE, GSI_NUM=GSI_NUM, CLUSTERED=True)

        '''
        Generating final output file
        '''
        print '\n\nGenerating final report file...'
        REPORT_CLUSTERED = INPUT_CLUSTERED + os.sep + REPORT
        REPORT_UNCLUSTERED = INPUT_UNCLUSTERED + os.sep + REPORT
        CLUSTER_DATA = OUTPUT + os.sep + 'clusterdata.csv'
        genoutput(CLUSTER_DATA, REPORT_CLUSTERED, REPORT_UNCLUSTERED, OUTPUT, FINAL_REPORT, COLS, THRESHOLD_GSI)

        '''
        Generating HD distribution plots
        '''
        hd_distribution(HD_CLUSTERED, HD_UNCLUSTERED, OUTPUT + os.sep + PRED_INTERVAL_FILE, HTML_OUTPUT, REQUEST_TYPE,
                        args.request_id)

        '''
        Generating html
        '''
        print '\n\nGenerating html file...'
        create_html(OUTPUT + os.sep + PRED_INTERVAL_FILE, HTML_OUTPUT, REQUEST_TYPE, args.request_id)

        # '''
        # Generating plot
        # '''
        # if TYPE == 'longi':
        #     '''
        #     Generating plot file
        #     '''
        #     print '\n\nGenerating plot file....'
        #     plot(OUTPUT + os.sep + FINAL_REPORT, OUTPUT=OUTPUT, PLOTFILE=PLOT)

    except Exception as e:
        print 'Error in NGS processing for request_id', e, args.request_id

    '''
    The code below updates the database
    I don't find it a good practice to update DB here
    I will move it to a separate script
    '''

    try:
        db.connect()
    except Exception as e:
        print 'Error in opening database connection ', e
        sys.exit(1)

    try:
        with db.atomic():
            request_query_res = DatingRequest.select().where(DatingRequest.request_id == str(args.request_id))
            if request_query_res:
                dating_request = request_query_res[0]
                form_data = json_decode(str(dating_request.form_data))
                form_data['requests'][int(args.request_idx)]['is_processed'] = True

                # Updating form data
                query_form_update = DatingRequest.update(form_data=str(json_encode(form_data))).where(
                    DatingRequest.request_id == args.request_id)
                query_form_update.execute()

                if dating_request.form_type == SINGLE:
                    query_is_processed = DatingRequest.update(is_processed=True, time_processed=datetime.now()).where(
                        DatingRequest.request_id == args.request_id)
                    query_is_processed.execute()


                elif dating_request.form_type == MULTIPLE:
                    processed_status = []
                    for request in form_data['requests']:
                        processed_status.append(request['is_processed'])

                    if all(status == True for status in processed_status):
                        # Updating databse
                        query_is_processed = DatingRequest.update(is_processed=True,
                                                                  time_processed=datetime.now()).where(
                            DatingRequest.request_id == args.request_id)
                        query_is_processed.execute()

                        # Creating zip
                        base_path = args.input_dir.rsplit('/', 1)[0]
                        dest_dir = os.path.join(base_path, 'Archive')
                        for i in range(int(dating_request.number_requests)):
                            source_dir = os.path.join(base_path, str(i), OUTPUT_DIR)
                            dest_dir_ = os.path.join(dest_dir, str(i))
                            copy_dir(source_dir, dest_dir_)
                        archive_file_name = os.path.join(base_path, args.request_id + '_ARCHIVE')
                        zip_file = make_zip(archive_file_name, 'zip', dest_dir)

                        # Creating upload bash script
                        command = 'python ' + UPLOAD_SCRIPT
                        script_name = 'UPLOAD_' + args.request_id
                        script_path = BASH_SCRIPT_PROCESS.format(request_id=args.request_id)
                        user_id = dating_request.user_id
                        write_bash_file(script_path, script_name, command=command, request_id=args.request_id,
                                        user_id=user_id, file_path=zip_file)


    except Exception as e:
        print 'Error in updating database in FENV processing for request_id', e, args.request_id

    finally:
        db.close()
