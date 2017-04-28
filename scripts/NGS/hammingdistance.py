'''
Author : Shivankur Kapoor
Contact : kapoors@usc.edu
Description: Calculates hamming distances between 2 sequences. Also apply alignment algorithm if sequences are misaligned
'''

import os
import numpy as np
# Parameters for needlemanwunsch algorithm
MATCH_REWARD = 1
MISMATCH_PENALTY = -1
GAP_OPENING_PENALTY = -5
GAP_EXTENSION_PENALTY = -2
NEG_INF = float('-inf')


def get_current(current, M, Ix, Iy, from_m, from_x, from_y):
    return {
        from_m: M,
        from_x: Ix,
        from_y: Iy
    }[current]


def needleman_using_affine_penalty(s1, s2):
    '''
     Local Sequence Alignment using Needlemanwunsch Algorithm
    :param s1: string sequence 1
    :param s2: string sequence 2
    :return: aligned sequence 1, alignment sequence 2
    '''
    if len(s1) == 0 or len(s2) == 0:
        print 'Error: One of the sequences is empty'
        return
    m = len(s1)
    n = len(s2)

    '''
    3 matrices required for affine penalty
    M: best score given that s1[i] is aligned to s2[j]
    Ix: best score given that s1[i] is aligned to a gap
    Iy: best score given that s2[j] is aligned to a gap
    '''
    import numpy as np

    M_Cost = np.zeros((m+1,n+1))
    M_Parent = np.zeros((m+1,n+1))
    Ix_Cost  =np.zeros((m+1,n+1))
    Ix_Parent = np.zeros((m+1,n+1))
    Iy_Cost = np.zeros((m+1,n+1))
    Iy_Parent = np.zeros((m+1,n+1))

    #M = [[(0, 0) for j in range(n + 1)] for i in range(m + 1)]
    #Ix = [[(0, 0) for j in range(n + 1)] for i in range(m + 1)]
    #Iy = [[(0, 0) for j in range(n + 1)] for i in range(m + 1)]

    from_m = 3
    from_x = 2
    from_y = 1
    M_Cost[0][0] = 0
    M_Parent[0][0] = 0
    Ix_Cost[0][0] = GAP_OPENING_PENALTY
    Ix_Parent[0][0] = 0
    Iy_Cost[0][0] = GAP_OPENING_PENALTY
    Iy_Parent[0][0] = 0

    for i in range(1, m + 1):
        M_Cost[i][0] = NEG_INF
        M_Parent[i][0] = 0

        Ix_Cost[i][0] = GAP_OPENING_PENALTY + GAP_EXTENSION_PENALTY * i
        Ix_Parent[i][0] = from_x

        Iy_Cost[i][0] = NEG_INF
        Iy_Parent[i][0] = 0

    for j in range(1, n + 1):
        M_Cost[0][j] = NEG_INF
        M_Parent[0][j] = 0

        Ix_Cost[0][j] = NEG_INF
        Ix_Parent[0][j] = 0

        Iy_Cost[0][j] =GAP_OPENING_PENALTY + GAP_EXTENSION_PENALTY * j
        Iy_Parent[0][j] = from_y

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            add_factor = MISMATCH_PENALTY
            if s1[i - 1] == s2[j - 1]:
                add_factor = MATCH_REWARD
            M_Cost[i][j], M_Parent[i][j] = max(
                (M_Cost[i - 1][j - 1] + add_factor, from_m),
                (Ix_Cost[i - 1][j - 1] + add_factor, from_x),
                (Iy_Cost[i - 1][j - 1] + add_factor, from_y)
            )



            Ix_Cost[i][j], Ix_Parent[i][j] = max(
                (M_Cost[i - 1][j] + GAP_OPENING_PENALTY + GAP_EXTENSION_PENALTY, from_m),
                (Ix_Cost[i - 1][j] + GAP_EXTENSION_PENALTY, from_x)
            )

            Iy_Cost[i][j], Iy_Parent[i][j] = max(
                (M_Cost[i][j - 1] + GAP_OPENING_PENALTY + GAP_EXTENSION_PENALTY, from_m),
                (Iy_Cost[i][j - 1] + GAP_EXTENSION_PENALTY, from_y)
            )

    alignseq1 = []
    alignseq2 = []
    if M_Cost[m][n] > Ix_Cost[m][n]:
        if M_Cost[m][n]> Iy_Cost[m][n]:
            current_cost = M_Cost

        else:
            current_cost = Iy_Cost
    else:
        if Ix_Cost[m][n] > Iy_Cost[m][n]:
            current_cost = Ix_Cost
        else:
            current_cost = Iy_Cost

    i = m
    j = n
    refer_dict = {
        from_m: M_Cost,
        from_x: Ix_Cost,
        from_y: Iy_Cost
    }
    while i > 0 or j > 0:
        if current_cost == M_Cost:
            current_cost = refer_dict[M_Parent[i][j]]
            i -= 1
            j -= 1
            alignseq1.append(s1[i])
            alignseq2.append(s2[j])
        elif current_cost == Ix_Cost:
            current_cost = refer_dict[Ix_Parent[i][j]]
            i -= 1
            alignseq1.append(s1[i])
            alignseq2.append('-')
        elif current_cost == Iy_Cost:
            current_cost = refer_dict[Iy_Parent[i][j]]
            j -= 1
            alignseq1.append('-')
            alignseq2.append(s2[j])
    alignseq1.reverse()
    alignseq2.reverse()
    return ''.join(alignseq1), ''.join(alignseq2)


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
                line = line.replace(' ', '-').strip()
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


def hamming_distance(s1, s2, input, gaps_ignore=True, **kwargs):
    '''
    Calculates Hamming Distance
    :param s1: String sequence 1
    :param s2: String sequence 2
    :param gaps_ignore: if gaps are considered while calculating HD
    :return: hamming distance
    '''
    try:

        s1, s2 = fast_sequence_alignment(input, s1.replace('-', ''), s2.replace('-', ''), **kwargs)
        matches, mismatches, insertionErrors, deletionErrors = 0, 0, 0, 0
        for i in range(len(s1)):
            if s1[i] == s2[i]:
                matches += 1
            elif s1[i] == '-':
                insertionErrors += 1
            elif s2[i] == '-':
                deletionErrors += 1
            else:
                mismatches += 1
        return mismatches if gaps_ignore else mismatches + insertionErrors + deletionErrors

    except Exception as e:
        print 'Sequences are not aligned correctly : ', e
        print s1
        print s2
        raise

