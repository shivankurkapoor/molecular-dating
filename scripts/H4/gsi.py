'''
Author : Shivankur Kapoor
Contact : kapoors@usc.edu
Description : Generates GSI data for all the input fasta files and saves then in a text file
'''

import os
from Bio import SeqIO
from hammingdistance import *
from utilityfunc import *

HDrange = 6
gapCost = 0


def gsi(INPUT, OUTPUT, gapsIgnore=True):
    '''
    Generates gsi for input fasta files
    :param INPUT: directory containing input fasta files
    :param OUTPUT: directory for the output gsi text file
    :param gapsIgnore: to consider gaps while calculating hammingdistance
    :return: None
    '''
    miseqfilepath = INPUT
    outputfile = OUTPUT
    filelist = []
    for file in os.listdir(miseqfilepath):
        if file.endswith(".fasta"):
            filelist.append(file)
    filelist = sorted(filelist)
    with open(outputfile, 'w') as f:
        f.write('File Name\tGSI0\tGSI1\tGSI2\tGSI3\tGSI4\tGSI5\n')

    for filename in filelist:
        print filename
        miseqfilehandle = open(miseqfilepath + os.sep + filename)
        miseqrecords = SeqIO.parse(miseqfilehandle, "fasta")
        rec = next(miseqrecords)
        sequences = dict()
        fvalues = dict()
        if ':' not in str(rec.id):
            sequenceCount = dict()
            while (rec.id != ""):
                try:
                    s = clean_seqeunce(str(rec.seq))
                    if s not in sequenceCount:
                        sequenceCount[s] = 1
                    else:
                        sequenceCount[s] += 1
                    rec = next(miseqrecords)
                except:
                    break
            count = 0
            totalReads = sum(sequenceCount.values()) * 1.0
            for s in sequenceCount:
                sequences[count] = s
                fvalues[count] = sequenceCount[s] / totalReads
                count += 1
        else:
            while rec.id != "":
                try:
                    recId = str(rec.id)
                    sequences[recId] = clean_seqeunce(str(rec.seq))
                    parts = recId.split(':')
                    fvalues[recId] = float(parts[-3]) / float(parts[-2])
                    rec = next(miseqrecords)
                except:
                    break

        HDlist = list()
        for i in range(HDrange):
            HDlist.append(list())

        hdAlreadyCalculated = dict()
        for key1 in sequences.keys():
            for key2 in sequences.keys():
                if key1 == key2:
                    HDlist[0].append((key1, key2))
                else:
                    if (key2, key1) not in hdAlreadyCalculated:
                        alignSeq1, alignSeq2 = sequences[key1], sequences[key2]
                        HD = hamming_distance(alignSeq1, alignSeq2, gapsIgnore)
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
        with open(outputfile, 'a') as f:
            f.write(filename.replace('.fasta', ''))
            for i in range(len(GSI)):
                f.write('\t' + str(round(GSI[i], 3)))
            f.write('\n')
        miseqfilehandle.close()
