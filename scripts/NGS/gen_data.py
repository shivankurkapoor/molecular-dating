'''
Author : Shivankur Kapoor
Contact : kapoors@usc.edu
Description : Generates diveristy, variance and gsi for input fasta files
'''
import glob
from collections import defaultdict, OrderedDict

import pandas as pd
from Bio import SeqIO

from hammingdistance import hamming_distance
from stats import *

max_iterations = 10000
HDrange = 6


def generate_div_gsi_var(INPUT, OUTPUT_DIVERSITY, OUTPUT_GSI, OUTPUT_VAR, OUTPUT_HD, TYPE, **alignment_param):
    '''
    Calculates diversity, varaince and gsi using using frequency based formulae
    :param INPUT: directory path for the input fasta files
    :param OUTPUT_DIVERSITY: output path for the diversity .npy file
    :param OUTPUT_GSI: output path for the gsi .txt file
    :param OUTPUT_VAR: output path the for variance .npy file
    :param TYPE: type of run [chronic, longi]
    :return: none
    '''
    subject_dict = {}
    div_dict = {}
    var_dict = {}
    hd_dict = {}
    gsi_list = []

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

    for subject, files_paths in subject_dict.items():
        hd_dict[subject] = {}
        for file in files_paths:
            seq_dict = OrderedDict()
            file_name = file.split('/')[-1]
            print file_name
            time = float(file.split('/')[-1].rsplit('.', 1)[0].split('-')[2][3:]) if TYPE == 'longi' else 1000
            hd_dict[subject][time] = defaultdict(int)
            fasta_sequences = SeqIO.parse(open(file), 'fasta')
            for fasta in fasta_sequences:
                name, sequence = fasta.id, str(fasta.seq)
                seq_dict[name] = sequence
            max_seq_len = max([len(seq.replace('_', '')) for seq in seq_dict.values()])
            seq_list = [seq for seq in seq_dict.values()]

            # Calculating fvalues
            fvalues = {}
            seq_count_dict = OrderedDict()
            for seq in seq_list:
                if seq not in seq_count_dict:
                    seq_count_dict[seq] = 0
                seq_count_dict[seq] += 1
            unique_seq_list = seq_count_dict.keys()
            nu = len(unique_seq_list)
            totalReads = sum(seq_count_dict.values()) * 1.0

            for i, seq in enumerate(unique_seq_list):
                fvalues[i] = seq_count_dict[seq] / totalReads

            # Creating pairwise hamming distance matrix for unique sequences 
            hd_mat = np.zeros((nu, nu))
            for i, seq1 in enumerate(unique_seq_list):
                for j, seq2 in enumerate(unique_seq_list):
                    if i == j:
                        hd_mat[i][j] = 0.0
                    elif j > i:
                        hd_mat[i][j] = hd_mat[j][i] = hamming_distance(seq1, seq2, **alignment_param)        
            

            unique_seq_dict = dict((seq, idx) for idx, seq in enumerate(unique_seq_list))
            # Creating hd dict for hd distribution and pairwise hamming distance matrix for complete sequences
            for i, seq1 in enumerate(seq_list):
                for j, seq2 in enumerate(seq_list):
                    if i < j:
                        if seq1 == seq2:
                            hd = 0
                        else:
                            idx1 = unique_seq_dict[seq1]
                            idx2 = unique_seq_dict[seq2]
                            hd = int(hd_mat[idx1][idx2])
                        hd_dict[subject][time][hd] += 1

            mat_path = ''.join(file.rsplit('.', 1)[:-1]) + '.npy'
            np.save(mat_path, hd_mat)

            # Calculating diversity
            try:
                actual_diversity = diversity(hd_mat, fvalues, max_seq_len)
                if subject not in div_dict:
                    div_dict[subject] = {}
                div_dict[subject][time] = actual_diversity
            except Exception as e:
                print 'Error while calculating Diversity : ', e
                print 'Subject : ', subject
                print 'Time point : ', time

            # Calculating GSI data
            try:
                GSI = gsi(unique_seq_list, hd_mat, fvalues)
                gsi_list.append({'File Name': file_name.replace('.fasta', '', ),
                                 'GSI0': GSI[0],
                                 'GSI1': GSI[1],
                                 'GSI2': GSI[2],
                                 'GSI3': GSI[3],
                                 'GSI4': GSI[4],
                                 'GSI5': GSI[5]})
            except Exception as e:
                print 'Error while calculating GSI : ', e
                print 'Subject : ', subject
                print 'Time point : ', time

            # Calculating VAR data
            try:
                var = var_freq(hd_mat, fvalues, max_seq_len)
                if subject not in var_dict:
                    var_dict[subject] = {}
                var_dict[subject][time] = var
            except Exception as e:
                print 'Error while calculating Variance : ', e
                print 'Subject : ', subject
                print 'Time point : ', time

    np.save(OUTPUT_DIVERSITY, div_dict)
    gsi_df = pd.DataFrame(gsi_list)
    gsi_df.to_csv(OUTPUT_GSI, sep='\t', index=False,
                  columns=['File Name', 'GSI0', 'GSI1', 'GSI2', 'GSI3', 'GSI4', 'GSI5'])
    np.save(OUTPUT_VAR, var_dict)
    np.save(OUTPUT_HD, hd_dict)


def diversity(hd_mat, fvalues, max_seq_len):
    '''
    Takes pair-wise hamming distance of the input sequences and returns
    the diversity
    :param hd_mat: numpy array of pairwise hamming distance
    :param fvalues: dict of frequency values
    :param max_seq_len: length of longest sequence
    :return: diversity
    '''
    actual_diversity = calc_diversity_frequency(hd_mat, fvalues, max_seq_len)
    return actual_diversity


def gsi(sequences, hd_mat, fvalues):
    '''
    Calculates GSI0 to GSI5 for input sequences
    :param sequences: input sequences
    :param hd_mat: numpy array of pair wise hamming distance
    :param fvalues: dict of frequency values
    :return: list of GSI values
    '''
    HDlist = []
    for i in range(HDrange):
        HDlist.append(list())

    hdAlreadyCalculated = dict()
    for key1, seq1 in enumerate(sequences):
        for key2, seq2 in enumerate(sequences):
            if key1 == key2:
                HDlist[0].append((key1, key2))
            else:
                if (key2, key1) not in hdAlreadyCalculated:
                    HD = int(hd_mat[key1][key2])
                    hdAlreadyCalculated[(key1, key2)] = HD
                else:
                    HD = hdAlreadyCalculated[(key2, key1)]
                if HD < HDrange:
                    HDlist[HD].append((key1, key2))

    GSI = [0] * HDrange
    for i in range(len(HDlist)):
        if i != 0:
            GSI[i] += GSI[i - 1]
        for pair in HDlist[i]:
            GSI[i] += fvalues[pair[0]] * fvalues[pair[1]]

    GSI = map(lambda x: round(x, 3), GSI)
    return GSI
