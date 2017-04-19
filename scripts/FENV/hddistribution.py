'''
Author : Shivankur Kapoor
Contact : kapoors@usc.edu
Description: Generates hamming distance distribution plots for clustered and unclustered fasta flies
'''


import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import MaxNLocator


image_path = '/home/leelab/PycharmProjects/moleculardating/application/static/images'
#image_path = '/home/web/moleculardating/application/static/images'
#image_path = '/Users/shivankurkapoor/GitHub/moleculardating/application/static/images'

def distribution_plot(subject, time, hd, freq, output, type, request_type, request_id):
    '''
    Generates hd distribution plot
    :param subject: name of the subject
    :param time: time
    :param hd: pairwise hamming distance dict
    :param freq: list of frequency for each hd
    :param output: output directory
    :param type: type of run
    :return: none
    '''
    #plt.figure(figsize=(5, 5))
    ax = plt.figure().gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    #ax.(axis='both', which='major', pad=15)
    hist = plt.bar(hd, freq, color='grey')
    ymin, ymax = ax.get_ylim()
    if ymax == max(freq):
        plt.ylim((0, max(freq)+1))
    plt.xlabel('Hamming Distance', fontsize=14)
    plt.ylabel('Distribution', fontsize=14, labelpad=15)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    if request_type == 'SINGLE':
        plt.savefig(os.path.join(image_path, request_id + '_' + type + '.png'))
    else:
        plt.savefig(os.path.join(output, request_id + '_' + type + '.png'))
    plt.close()


def hd_distribution(CLUSTERED_HD_DATA, UNCLUSTERED_HD_DATA, SUBJECT_DATA, OUTPUT, REQUEST_TYPE, REQUEST_ID):
    '''
    :param CLUSTERED_HD_DATA: path of hamming distance npy file for clustered fasta files
    :param UNCLUSTERED_HD_DATA: path of hamming distance npy file for unclustered fasta files
    :param SUBJECT_DATA: path of final csv file
    :param OUTPUT: path of output dir
    :return:
    '''
    clustered_hd_dict = dict(np.load(CLUSTERED_HD_DATA).item())
    unclustered_hd_dict = dict(np.load(UNCLUSTERED_HD_DATA).item())
    df = pd.read_csv(SUBJECT_DATA, index_col=False, dtype={"#SUBJECT": "string"})

    for index, row in df.iterrows():
        subject = str(row['#SUBJECT'])
        clustered = str(row['CLUSTERED'])
        time = float(row['TIME'])
        if clustered == 'YES':
            hd_dict = clustered_hd_dict[subject][time]
            hd = sorted(hd_dict.keys())
            freq = [hd_dict[h] for h in hd]
            distribution_plot(subject, time, hd, freq, OUTPUT, 'CLUSTERED', REQUEST_TYPE, REQUEST_ID)

            hd_dict = unclustered_hd_dict[subject][time]
            hd = sorted(hd_dict.keys())
            freq = [hd_dict[h] for h in hd]
            distribution_plot(subject, time, hd, freq, OUTPUT, 'UNCLUSTERED', REQUEST_TYPE, REQUEST_ID)

        elif clustered == 'NO':
            hd_dict = unclustered_hd_dict[subject][time]
            hd = sorted(hd_dict.keys())
            freq = [hd_dict[h] for h in hd]
            distribution_plot(subject, time, hd, freq, OUTPUT, 'UNCLUSTERED', REQUEST_TYPE, REQUEST_ID)
