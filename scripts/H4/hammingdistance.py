'''
Author : Shivankur Kapoor
Contact : kapoors@usc.edu
Description: Calculates hamming distances between 2 sequences. Also apply alignment algorithm if sequences are misaligned
'''

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


def hamming_distance(s1, s2, gaps_ignore=True):
    '''
    Calculates Hamming Distance
    :param s1: String sequence 1
    :param s2: String sequence 2
    :param gaps_ignore: if gaps are considered while calculating HD
    :return: hamming distance
    '''
    try:
        if len(s1) != len(s2):
            print 'One or more sequences are misaligned, aligning now'
            s1, s2 = needleman_wunsch(s1, s2)
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
