'''
Author : Shivankur Kapoor
Contact : kapoors@usc.edu
Description: Performs PAM clustering using AgglomerativeClustering in sklearn
'''

from sklearn.cluster import AgglomerativeClustering

from stats import *

LARGE_NUM = 99999


def dissimilarity(distances):
    '''
    Calculates the dissimilarity matrix for clustering
    :param distances: HD dict
    :return: dissimilarity matrix as numpy array
    '''
    diss = np.zeros((len(distances), len(distances)))
    for i, value1 in distances.items():
        for j, value2 in value1.items():
            diss[i, j] = value2
    return diss


def pam_var(D, distances, seq_list, THRESHOLD, SEQ_THRESHOLD, freq_dict, K):
    '''
    Performs PAM (partition around mediod) clustering
    :param D: list of indices of input sequences
    :param distances: hamming distance dict
    :param seq_list: list of input sequences to be clustered
    :param THRESHOLD: Beta threshold
    :param SEQ_THRESHOLD: Threshold for minimum number of sequences in each cluster
    :param K: list of potential values for number of clusters
    :return: tuple of k, variance, diversity, beta, clusters, major cluster
    '''
    diss = dissimilarity(distances)
    results = {}
    for k in K:
        AggClusterDistObj = AgglomerativeClustering(n_clusters=k, linkage='complete', affinity="precomputed")
        clusters_labels = AggClusterDistObj.fit_predict(diss)
        C = {}
        for seq_idx, cluster in enumerate(clusters_labels):
            if not cluster in C:
                C[cluster] = []
            C[cluster].append(seq_idx)
        var_SE, diversity, beta, MC = stats(C, seq_list, distances, freq_dict)
        results[k] = (var_SE, diversity, beta, C, MC)
        len_mc = len(MC.values()[0])
        if len_mc < SEQ_THRESHOLD:
            results.pop(k)
            break
        if beta < THRESHOLD:
            break
    sorted_results = sorted(results.items(), key=lambda x: x[1][2])
    final_result = sorted_results[0]
    return final_result[0], final_result[1][0], final_result[1][1], final_result[1][2], final_result[1][3], \
           final_result[1][4]
