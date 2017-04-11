'''
Author : Shivankur Kapoor
Contact : kapoors@usc.edu
'''

import glob
import os
import sys
import pandas as pd


def clean_directories(DIRS):
    '''
    Clean directories
    :param DIRS: list of directories
    :return: None
    '''
    for dir in DIRS:
        if not os.path.exists(dir):
            os.makedirs(dir)
        else:
            files = glob.glob(dir + '/*')
            for f in files:
                if not os.path.isdir(f):
                    os.remove(f)


if __name__ == '__main__':
    INPUT = sys.argv[1]
    OUTPUT = sys.argv[2]
    clean_directories([OUTPUT])

    df = pd.read_csv(INPUT, header=0, dtype={"#SUBJECT": "string"})
    grouped = df.groupby(['#SUBJECT'])
    for group in grouped.groups:
        dff = grouped.get_group(group)
        dff = dff.sort_values(by=['TIME'])
        init_diversity = dff[dff.TIME == 0.0].iloc[0]['DIVERSITY']
        init_effective_diversity = dff[dff.TIME == 0.0].iloc[0]['EFFECTIVE_DIVERSITY']
        dff['DIVERSITY'] = dff['DIVERSITY'].map(lambda x: x - init_diversity)
        dff['EFFECTIVE_DIVERSITY'] = dff['EFFECTIVE_DIVERSITY'].map(lambda x: x - init_effective_diversity)
        dff = dff.drop(dff.index[[0]])
        dff = dff.rename(columns={'DIVERSITY': 'DIVERISTY_DIFF',
                                  'EFFECTIVE_DIVERSITY': 'EFFECTIVE_DIV_DIFF'})
        dff.to_csv(OUTPUT + os.sep + group + '-time-dynamics' + '.txt', sep='\t', index=False)
