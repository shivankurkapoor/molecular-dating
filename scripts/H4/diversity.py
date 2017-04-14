import glob
import os
import numpy as np
from Bio import SeqIO
from hammingdistance import hamming_distance
from stats import *
from utilityfunc import *
from collections import OrderedDict

max_iterations = 10000


def generate_diversity_data(INPUT, OUTPUT, TYPE, OUTPUTHD, GAPS_IGNORE, ALIGN, **alignment_params):
    subject_dict = {}
    div_dict = {}
    # div_diff_dict = {}
    # ci_dict = {}
    hd_dict = {}
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
        print subject
        hd_dict[subject] = {}
        for file in files_paths:
            seq_dict = OrderedDict()
            time = float(file.split(os.sep)[-1].rsplit('.', 1)[0].split('-')[2][3:]) if TYPE == 'longi' else 1000.0
            fasta_sequences = SeqIO.parse(open(file), 'fasta')
            for fasta in fasta_sequences:
                name, sequence = fasta.id, str(fasta.seq)
                seq_dict[name + random_string(3)] = clean_seqeunce(sequence)
            max_seq_len = max([len(seq.replace('_', '')) for seq in seq_dict.values()])
            seq_list = [seq for seq in seq_dict.values()]
            hd_list = []

            # Creating pairwise hamming distance matrix and saving it to use it later
            n = len(seq_list)
            hd_mat = np.zeros((n, n))

            # Calculating actual diversity
            hd_dict[subject][time] = {}
            for i, seq_1 in enumerate(seq_list):
                for j, seq_2 in enumerate(seq_list):
                    if i == j:
                        hd_mat[i][j] = 0
                    elif i < j:
                        try:
                            hd = hamming_distance(seq_1, seq_2, INPUT, GAPS_IGNORE, ALIGN, **alignment_params)
                            hd_mat[i][j] = hd_mat[j][i] = hd
                            if hd in hd_dict[subject][time]:
                                hd_dict[subject][time][hd] += 1
                            else:
                                hd_dict[subject][time][hd] = 1
                            hd_list.append(hd)
                        except Exception as e:
                            print 'Error while calculating Hamming Distance', e
                            print 'Sequence 1 : ', seq_1
                            print 'Sequence 2 : ', seq_2
                            print 'Subject : ', subject
                            print 'Time point : ', time
            mat_path = ''.join(file.rsplit('.', 1)[:-1])
            np.save(mat_path, hd_mat)

            try:
                actual_diversity = calc_diversity(hd_list, max_seq_len, len(seq_list))
                if subject not in div_dict:
                    div_dict[subject] = {}
                div_dict[subject][time] = actual_diversity
            except Exception as e:
                print 'Error while calculating Diversity : ', e
                print 'Subject : ', subject
                print 'Time point : ', time

    np.save(OUTPUT, div_dict)
    np.save(OUTPUTHD, hd_dict)