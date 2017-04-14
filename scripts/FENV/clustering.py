'''
Author : Shivankur Kapoor
Contact : kapoors@usc.edu
Description: Performs PAM clustering on input fasta files and generates fasta flies with major lineage
'''

import pandas as pd
import glob
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import DNAAlphabet
import os
from plotutils import *
from scipy_pam import *
from stats import stats
from prettytable import PrettyTable
from utilityfunc import *
from collections import OrderedDict

colors = cnames.keys() * 20


def clustering(INPUT, OUTPUT, GSI_FILE, THRESHOLD, DIVERSITY_THRESHOLD, GSI_THRESHOLD, SEQ_THRESHOLD, TYPE,
               FINALOUTPUT, GSI_NUM):
    '''
    :param INPUT: input directory for fastsa files
    :param OUTPUT: output directory for clustered fasta flies
    :param GSI_FILE: path for the unclustered gsi file
    :param THRESHOLD: Beta threshold
    :param DIVERSITY_THRESHOLD: diversity threshold
    :param GSI_THRESHOLD: gsi threshold
    :param SEQ_THRESHOLD: threshold for number of sequences
    :param TYPE: type of run
    :param FINALOUTPUT: output directory for generated clustering data
    :param GSI_NUM: type of gsi
    :return: none
    '''
    subject_dict = {}
    gsi_dict = {}
    try:
        file_paths = glob.glob(INPUT + '/*fasta')
        file_paths = sorted(file_paths)
        for file_path in file_paths:
            file_name = file_path.split('/')[-1]
            subname = file_name.split('-')[0] if TYPE == 'longi' else file_name.split('.')[0]
            if subname not in subject_dict:
                subject_dict[subname] = []
            subject_dict[subname].append(file_path)

    except Exception as e:
        print e

    # Reading the GSI File
    try:
        df = pd.read_csv(GSI_FILE, sep="\t", header=0)
        df = df[['File Name', GSI_NUM]]
        for index, row in df.iterrows():
            subject = row['File Name'].split('-')[0] if TYPE == 'longi' else row['File Name'].split('.')[0]
            time = row['File Name'].split('-')[2][3:] if TYPE == 'longi' else 1000.0
            gsi = float(row[GSI_NUM])
            if subject not in gsi_dict:
                gsi_dict[subject] = {}
            gsi_dict[subject][float(time)] = gsi
    except Exception as e:
        print 'Error in reading GSI file ', e

    t = PrettyTable(['Subject', 'Time', 'Number of Clusters', 'Diversity', 'Variance', 'Beta'])
    stats_dict_list = []
    if not os.path.exists(OUTPUT):
        os.makedirs(OUTPUT)
    for subject, files_paths in subject_dict.items():
        for file in files_paths:
            seq_dict = OrderedDict()
            time = float(file.split(os.sep)[-1].rsplit('.', 1)[0].split('-')[2][3:]) if TYPE == 'longi' else 1000.0
            fasta_sequences = SeqIO.parse(open(file), 'fasta')
            for fasta in fasta_sequences:
                name, sequence = fasta.id, str(fasta.seq)
                seq_dict[name + random_string(3)] = clean_seqeunce(sequence)
            seq_list = [seq for seq in seq_dict.values()]

            # Reading the saved HD matrix
            hd_mat = {}
            hd_mat_path = ''.join(file.rsplit('.', 1)[:-1]) + '.npy'
            hd_mat_saved = np.load(hd_mat_path)

            for i in range(len(seq_list)):
                hd_mat[i] = {}
                hd_mat[i][i] = 0

            for i, seq_1 in enumerate(seq_list):
                for j, seq_2 in enumerate(seq_list):
                    if i < j:
                        try:
                            hd = hd_mat_saved[i][j]
                            if i not in hd_mat:
                                hd_mat[i] = {}
                            if j not in hd_mat:
                                hd_mat[j] = {}
                            hd_mat[i][j] = hd
                            hd_mat[j][i] = hd


                        except Exception as e:
                            print 'Error while calculating Hamming Distance', e
                            print 'Sequence 1 : ', seq_1
                            print 'Sequence 2 : ', seq_2
                            print 'Subject : ', subject
                            print 'Time point : ', time

            D = np.array(xrange(len(seq_list)))

            try:

                if len(D) > 3:

                    var_SE, diversity, beta, MC = stats({0: D}, seq_list, hd_mat)
                    gsi = gsi_dict[subject][time]

                    if (diversity > DIVERSITY_THRESHOLD and gsi < GSI_THRESHOLD):
                        t.add_row([subject, str(time), str(1), str(diversity), str(var_SE), str(beta)])
                        stats_dict_list.append({'#SUBJECT': subject,
                                                'TIME': str(time),
                                                'CLUSTERS': str(1),
                                                'DIVERSITY': str(diversity),
                                                'VAR_SE': str(var_SE),
                                                'BETA': str(beta)})

                    elif beta > THRESHOLD:
                        K, var_SE, diversity, beta, C, MC = pam_var(D, hd_mat, seq_list, THRESHOLD, SEQ_THRESHOLD,
                                                                       K=range(1, 20))
                        t.add_row([subject, str(time), str(K), str(diversity), str(var_SE), str(beta)])
                        stats_dict_list.append({'#SUBJECT': subject,
                                                'TIME': str(time),
                                                'CLUSTERS': str(K),
                                                'DIVERSITY': str(diversity),
                                                'VAR_SE': str(var_SE),
                                                'BETA': str(beta)})
                    else:
                        t.add_row([subject, str(time), str(1), str(diversity), str(var_SE), str(beta)])
                        stats_dict_list.append({'#SUBJECT': subject,
                                                'TIME': str(time),
                                                'CLUSTERS': str(1),
                                                'DIVERSITY': str(diversity),
                                                'VAR_SE': str(var_SE),
                                                'BETA': str(beta)})

                else:
                    print 'Too few sequences to cluster ', len(D)
                    print subject
                    print time



            except Exception as e:
                print e
                print subject
                print time
            major_seq = [seq_list[c] for c in MC.values()[0]]
            rec_list = []
            seq_id_list = [id for id in seq_dict.keys()]
            for sequence, idx in zip(major_seq, MC.values()[0]):
                rec = SeqRecord(Seq(sequence, DNAAlphabet), id=seq_id_list[idx])
                rec_list.append(rec)
            if TYPE == 'longi':
                SeqIO.write(rec_list, OUTPUT + os.sep + subject + "-FENV-DFF" + str(time) + ".fasta", "fasta")
            elif TYPE == 'chronic':
                SeqIO.write(rec_list, OUTPUT + os.sep + subject + ".fasta", "fasta")
    print t
    df = pd.DataFrame(stats_dict_list)
    df.to_csv(FINALOUTPUT + os.sep + 'clusterdata.csv', index=False)