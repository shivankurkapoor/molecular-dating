import numpy as np

LARGE_NUM = 99999


def var_freq(hd_mat, fvalues, max_seq_len):
    '''
    Calculates the variance based on frequency based formula
    :param hd_mat: numpy array of pairwise hamming distance
    :param fvalues: dict of frequency values
    :param max_seq_len: length of the longest sequence
    :return: diversity
    '''
    len_unique_len = np.shape(hd_mat)[0]
    term1 = 0.0
    term2 = 0.0
    # Calculating term1 and term2
    for i in range(len_unique_len):
        for j in range(len_unique_len):
            if j > i:
                term1 += hd_mat[i][j] ** 2 * fvalues[i] * fvalues[j]
                term2 += hd_mat[i][j] * fvalues[i] * fvalues[j]

    term2 = term2 ** 2
    var = ((term1 - term2) * 100) / max_seq_len
    return var


def calc_diversity_frequency(hd_mat, fvalues, max_seq_len):
    '''
    Calculates the diversity based on frequency based formula
    :param hd_mat: numpy array of pairwise hamming distance
    :param fvalues: dict of frequency values
    :param max_seq_len: length of the longest sequence
    :return: diversity
    '''
    len_unique_len = np.shape(hd_mat)[0]
    diversity = 0.0
    for i in range(len_unique_len):
        for j in range(len_unique_len):
            if j > i:
                diversity += hd_mat[i][j] * fvalues[i] * fvalues[j]

    diversity = (diversity * 100) / (max_seq_len)
    return diversity


def stats(C, unique_seq_list, hd_dict, freq_dict):
    '''
    Find the major cluster (having largest number of sequences) and calculates its variance, diversity, beta
    :param C: cluster assignment. output of clustering
    :param seq_list: list of sequences on which clustering is performed
    :param hd_dict: pairwise hamming distance dict
    :return: variance, diversity, beta, cluster assignment for major lineage
    '''
    sorted_clusters = sorted(C.items(), key=lambda x: len(x[1]), reverse=True)
    max_len = len(sorted_clusters[0][1])
    best_beta = LARGE_NUM
    best_var_SE = LARGE_NUM
    best_diversity = 0.001
    best_cluster = {sorted_clusters[0][0]: sorted_clusters[0][1]}
    for medoid, cluster in sorted_clusters:
        if len(cluster) == max_len:
            unique_seqs_mc = [unique_seq_list[i] for i in cluster]
            # seq_id_dict = {}
            # seq_count_dict = {}

            # for seq_id in cluster:
            #     if seq_list[seq_id] not in seq_id_dict:
            #         seq_id_dict[seq_list[seq_id]] = []
            #     seq_id_dict[seq_list[seq_id]].append(seq_id)
            #
            # for key, value in seq_id_dict.items():
            #     seq_count_dict[key] = len(value)

            nu = len(unique_seqs_mc)
            totalReads = sum([freq_dict[seq] for seq in unique_seqs_mc]) * 1.0

            # Creating fvalues
            fvalues = {}
            for i, seq in enumerate(unique_seqs_mc):
                fvalues[i] = freq_dict[seq] / totalReads

            # Creating hd mat for unique sequences in major cluster
            hd_mat = np.zeros((nu, nu))

            for i, unique_seq_id_1 in enumerate(cluster):
                for j, unique_seq_id_2 in enumerate(cluster):
                    if i == j:
                        hd_mat[i][j] = 0.0
                    elif j > i:
                        hd_mat[i][j] = hd_mat[j][i] = hd_dict[unique_seq_id_1][unique_seq_id_2]

            max_seq_len = max([len(seq.replace('-', '')) for seq in unique_seqs_mc])
            var_SE = var_freq(hd_mat, fvalues, max_seq_len)
            diversity = calc_diversity_frequency(hd_mat, fvalues, max_seq_len)
            beta = 1 if diversity == 0 or var_SE == 0 else var_SE / diversity

            if beta < best_beta:
                best_cluster = {medoid: cluster}
                best_var_SE = var_SE
                best_diversity = diversity
                best_beta = beta

        else:
            break
    return best_var_SE, best_diversity, best_beta, best_cluster
