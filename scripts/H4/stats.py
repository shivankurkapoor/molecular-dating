'''
Author : Shivankur Kapoor
Contact : kapoors@usc.edu
Description: Contains methods for calculating variance, diversity and major cluster
'''

LARGE_NUM = 99999


def var_se(maxlen, hd_list, N):
    '''
    Calculates variance
    :param maxlen: length of longest sequence
    :param hd_list: list of pairwise hamming distances
    :param N: total number of sequences
    :return: variance
    '''
    term1 = sum(map(lambda hd: hd ** 2, hd_list))
    term1 /= (N * (N - 1) / 2.0)
    term2 = sum(hd_list)
    term2 /= (N * (N - 1) / 2.0)
    term2 = term2 ** 2
    result = term1 - term2
    result /= maxlen
    return float(result) * 100


def calc_diversity(hd_list, max_seq_len, n):
    '''
    Calculates diversity
    :param hd_list: list of pairwise hamming distance
    :param max_seq_len: length of longest sequence
    :param n: total number of sequences
    :return: diversity
    '''
    try:
        assert len(hd_list) != 0
        diversity = sum(hd_list) * 100
        diversity /= (n * (n - 1)) / 2.0
        diversity /= max_seq_len
        return float(diversity)
    except Exception as e:
        print 'HD list not generated : ', e
        raise


def stats(C, seq_list, hd_dict):
    '''
    Find the major cluster (having largest number of sequences) and calculates its variance, diversity, beta
    :param C: cluster assignment. output of clustering
    :param seq_list: list of sequences on which clustering is performed
    :param hd_dict: pairwise hamming distance dict
    :return:
    '''
    sorted_clusters = sorted(C.items(), key=lambda x: len(x[1]), reverse=True)
    max_len = len(sorted_clusters[0][1])
    best_beta = LARGE_NUM
    best_var_SE = LARGE_NUM
    best_diversity = 0.001
    best_cluster = {sorted_clusters[0][0]: sorted_clusters[0][1]}
    for medoid, cluster in sorted_clusters:
        if len(cluster) == max_len:
            N = len(cluster)
            hd_list = []
            cluster = sorted(cluster)
            for i in cluster:
                for j in cluster:
                    if i < j:
                        hd_list.append(hd_dict[i][j])

            seqs = [seq_list[i] for i in cluster]
            max_seq_len = max([len(seq.replace('-', '')) for seq in seqs])
            var_SE = var_se(max_seq_len, hd_list, N)
            diversity = calc_diversity(hd_list, max_seq_len, N)
            beta = 1 if diversity == 0 or var_SE == 0 else var_SE / diversity

            if beta < best_beta:
                best_cluster = {medoid: cluster}
                best_var_SE = var_SE
                best_diversity = diversity
                best_beta = beta

        else:
            break
    return best_var_SE, best_diversity, best_beta, best_cluster
