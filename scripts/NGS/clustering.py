'''
Author : Shivankur Kapoor
Contact : kapoors@usc.edu
Description: Performs PAM clustering on input fasta files and generates fasta flies with major lineage
'''

import glob
import os
from collections import OrderedDict

import pandas as pd
from Bio import SeqIO
from Bio.Alphabet import DNAAlphabet
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from prettytable import PrettyTable

from scipy_pam import *
from stats import stats
from utilityfunc import *


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
            time = row['File Name'].split('-')[2][3:] if TYPE == 'longi' else 1000
            if subject not in gsi_dict:
                gsi_dict[subject] = {}
            gsi = float(row[GSI_NUM])
            gsi_dict[subject][float(time)] = gsi
    except Exception as e:
        print 'Error in reading GSI file ', e

    t = PrettyTable(['Subject', 'Time', 'Number of Clusters', 'Diversity', 'Variance', 'Beta', 'GSI',
                     'Diversity(before clustering)'])
    stats_dict_list = []
    if not os.path.exists(OUTPUT):
        os.makedirs(OUTPUT)
    for subject, files_paths in subject_dict.items():
        for file in files_paths:
            file_name = file.split('/')[-1]
            seq_dict = OrderedDict()
            seq_id_dict = OrderedDict()
            time = float(file.split('/')[-1].rsplit('.', 1)[0].split('-')[2][3:]) if TYPE == 'longi' else 1000
            fasta_sequences = SeqIO.parse(open(file), 'fasta')
            for fasta in fasta_sequences:
                name, sequence = fasta.id, str(fasta.seq)
                seq_dict[name] = sequence
                seq_id_dict[sequence] = name
            seq_tup = seq_dict.items()
            seq_list = [seq for _, seq in seq_tup]

            # Creating unique sequences
            seq_count_dict = OrderedDict()
            for id, seq in seq_tup:
                count = int(id.strip().split(':')[7])
                seq_count_dict[seq] = count
            unique_seq_list = seq_count_dict.keys()

            # Reading the saved HD matrix
            hd_mat = {}
            hd_mat_path = ''.join(file.rsplit('.', 1)[:-1]) + '.npy'
            hd_mat_saved = np.load(hd_mat_path)

            for i in range(len(unique_seq_list)):
                hd_mat[i] = {}
                hd_mat[i][i] = 0

            for i in range(len(unique_seq_list)):
                for j in range(len(unique_seq_list)):
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
                            print 'Subject : ', subject
                            print 'Time point : ', time

            D = np.array(range(len(unique_seq_list)))
            major_seq = []
            try:

                var_SE, diversity, beta, MC = stats({0: D}, unique_seq_list, hd_mat, seq_count_dict)
                gsi = gsi_dict[subject][time]
                old_div = diversity

                if len(D) < 3:
                    t.add_row(
                        [subject, str(time), str(1), str(diversity), str(var_SE), str(beta), str(gsi), str(old_div)])
                    stats_dict_list.append({'#SUBJECT': subject,
                                            'TIME': str(time),
                                            'CLUSTERS': str(1),
                                            'DIVERSITY': str(diversity),
                                            'VAR_SE': str(var_SE),
                                            'BETA': str(beta)})

                elif (diversity > DIVERSITY_THRESHOLD and gsi < GSI_THRESHOLD):
                    t.add_row(
                        [subject, str(time), str(1), str(diversity), str(var_SE), str(beta), str(gsi), str(old_div)])
                    stats_dict_list.append({'#SUBJECT': subject,
                                            'TIME': str(time),
                                            'CLUSTERS': str(1),
                                            'DIVERSITY': str(diversity),
                                            'VAR_SE': str(var_SE),
                                            'BETA': str(beta)})

                elif beta > THRESHOLD:
                    K, var_SE, diversity, beta, C, MC = pam_var(D, hd_mat, unique_seq_list, THRESHOLD, SEQ_THRESHOLD,
                                                                seq_count_dict, K=range(1, 20))
                    t.add_row(
                        [subject, str(time), str(K), str(diversity), str(var_SE), str(beta), str(gsi), str(old_div)])
                    stats_dict_list.append({'#SUBJECT': subject,
                                            'TIME': str(time),
                                            'CLUSTERS': str(K),
                                            'DIVERSITY': str(diversity),
                                            'VAR_SE': str(var_SE),
                                            'BETA': str(beta)})
                else:
                    t.add_row(
                        [subject, str(time), str(1), str(diversity), str(var_SE), str(beta), str(gsi), str(old_div)])
                    stats_dict_list.append({'#SUBJECT': subject,
                                            'TIME': str(time),
                                            'CLUSTERS': str(1),
                                            'DIVERSITY': str(diversity),
                                            'VAR_SE': str(var_SE),
                                            'BETA': str(beta)})

                for c in MC.values()[0]:
                    sequence = unique_seq_list[c]
                    major_seq.append(sequence)


            except Exception as e:
                print e
                print subject
                print time

            rec_list = []
            for sequence in major_seq:
                rec = SeqRecord(Seq(sequence, DNAAlphabet), id=seq_id_dict[sequence], description='')
                rec_list.append(rec)
            if TYPE == 'longi':
                SeqIO.write(rec_list, OUTPUT + '/' + file_name, "fasta")
            elif TYPE == 'chronic':
                SeqIO.write(rec_list, OUTPUT + '/' + file_name, "fasta")
    print t
    df = pd.DataFrame(stats_dict_list)
    df.to_csv(FINALOUTPUT + '/' + 'clusterdata.csv', index=False)
