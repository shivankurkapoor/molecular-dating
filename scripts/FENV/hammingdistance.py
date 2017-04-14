'''
Author : Shivankur Kapoor
Contact : kapoors@usc.edu
Description: Calculates hamming distances between 2 sequences. Also apply alignment algorithm if sequences are misaligned
'''

import os

gapCost = 0


def needleman_wunsch(s1, s2):
    '''
    Needleman Wunsch Sequence Alignment
    :param s1: String sequence 1
    :param s2: String sequence 2
    :return: Aligned sequences as a tuple
    '''
    if len(s1) == 0 or len(s2) == 0:
        print("One string empty")
    s1len = len(s1)
    s2len = len(s2)
    table = [[0] * (s2len + 1) for i in range(s1len + 1)]
    for i in range(1, s2len + 1):
        table[0][i] = gapCost * i
    for j in range(1, s1len + 1):
        table[j][0] = gapCost * j
    for i in range(1, s1len + 1):
        for j in range(1, s2len + 1):
            add = 0
            if s1[i - 1] == s2[j - 1]:
                add = 1
            table[i][j] = max((table[i - 1][j - 1] + add), table[i - 1][j] + gapCost, table[i][j - 1] + gapCost)
    alignSeq1 = ''
    alignSeq2 = ''
    i = s1len
    j = s2len
    while i > 0 and j > 0:
        currentValue = table[i][j]
        add = 0
        if s1[i - 1] == s2[j - 1]:
            add = 1
        if currentValue == table[i - 1][j - 1] + add:
            alignSeq1 = s1[i - 1] + alignSeq1
            alignSeq2 = s2[j - 1] + alignSeq2
            i -= 1
            j -= 1
        elif currentValue == table[i][j - 1] + gapCost:
            alignSeq1 = '_' + alignSeq1
            alignSeq2 = s2[j - 1] + alignSeq2
            j -= 1
        elif currentValue == table[i - 1][j] + gapCost:
            alignSeq2 = '_' + alignSeq2
            alignSeq1 = s1[i - 1] + alignSeq1
            i -= 1
    if j != 0:
        alignSeq1 = '_' * j + alignSeq1
        alignSeq2 = s2[:j] + alignSeq2
    elif i != 0:
        alignSeq2 = '_' * i + alignSeq2
        alignSeq1 = s1[:i] + alignSeq1
    return alignSeq1, alignSeq2


def fast_sequence_alignment(input, s1, s2, **kwargs):
    '''
    The Context-Dependent Alignment (CDA) program computes a global alignment
    of two sequences. It delivers the alignment in linear space,
    so long sequences can be aligned.
    Users supply scoring parameters. In the simplest form, users just
    provide 5 integers: ms, q, r, l and b, where ms is the score of a mismatch,
    q is gap-open penalty, r is gap-extension penalty, l is context length,
    and b is match bonus. Each match automatically receives a score of 10.
    The score of an i-symbol indel is -(q + r * i). A match in a substitution
    block receives a single left bonus of b if at least one other match occurs
    within l positions to the left of the match. Similarly, a match in a
    substitution block receives a single right bonus of b if at least one other
    match occurs within l positions to the right of the match.
    This simple scoring scheme may be used for DNA sequences.
    NOTE: all scores are integers.
    '''
    # Writing sequences to files A and B
    try:
        if os.path.exists(os.path.join(input, 'SEQUENCE_A')):
            os.remove(os.path.join(input, 'SEQUENCE_A'))
        if os.path.exists(os.path.join(input, 'SEQUENCE_B')):
            os.remove(os.path.join(input, 'SEQUENCE_B'))
        with open(os.path.join(input, 'SEQUENCE_A'), 'w') as f:
            f.write(s1)
        with open(os.path.join(input, 'SEQUENCE_B'), 'w') as f:
            f.write(s2)
    except IOError as e:
        print e
        raise

    try:
        if os.path.exists(os.path.join(input, 'ALIGNED_SEQUENCES.txt')):
            os.remove(os.path.join(input, 'ALIGNED_SEQUENCES.txt'))
        ms = kwargs.pop('ms', -1)
        q = kwargs.pop('q', 1)
        r = kwargs.pop('r', 1)
        l = kwargs.pop('l', 1)
        b = kwargs.pop('b', 0)
        cmd = "./cda {A} {B} {ms} {q} {r} {l} {b} > {R}".format(A=os.path.join(input, 'SEQUENCE_A'),
                                                                B=os.path.join(input, 'SEQUENCE_B'), ms=ms, q=q, r=r,
                                                                l=l, b=b,
                                                                R=os.path.join(input, 'ALIGNED_SEQUENCES.txt'))
        os.system(cmd)
    except Exception as e:
        print 'Error in running fast alignment', e
        raise
    try:
        seq1 = []
        gaps = []
        seq2 = []
        l = 0
        with open(os.path.join(input, 'ALIGNED_SEQUENCES.txt'), 'r') as f:
            for line in f.readlines():
                line = line.replace(' ', '_').strip()
                if l == 0:
                    seq1.append(line)
                elif l == 1:
                    gaps.append(line)
                elif l == 2:
                    seq2.append(line)
                l = (l + 1) % 3
        alignseq1 = ''.join(seq1)
        alignseq2 = ''.join(seq2)
        return alignseq1, alignseq2
    except IOError as e:
        print 'Error in reading alignment result', e
        raise


def hamming_distance(s1, s2, input, gaps_ignore=True, align=False, **kwargs):
    '''
    Calculates Hamming Distance
    :param s1: String sequence 1
    :param s2: String sequence 2
    :param gaps_ignore: if gaps are considered while calculating HD
    :return: hamming distance
    '''
    try:
        if align or len(s1) != len(s2):
            print 'One or more sequences are misaligned, aligning now'
            # s1, s2 = needleman_wunsch(s1, s2)
            s1, s2 = fast_sequence_alignment(input, s1.replace('_', ''), s2.replace('_', ''), **kwargs)
        matches, mismatches, insertionErrors, deletionErrors = 0, 0, 0, 0
        for i in range(len(s1)):
            if s1[i] == s2[i]:
                matches += 1
            elif s1[i] == '_':
                insertionErrors += 1
            elif s2[i] == '_':
                deletionErrors += 1
            else:
                mismatches += 1
        return mismatches if gaps_ignore else mismatches + insertionErrors + deletionErrors

    except Exception as e:
        print 'Sequences are not aligned correctly : ', e
        print s1
        print s2
        raise
