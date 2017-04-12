import os
import yaml

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

mainconfig = cfg['mainconfig']
predictioninterval = cfg['predictioninterval']
filenames = cfg['filenames']
html = cfg['html']


'''
TYPE
'''
TYPE = str(mainconfig['type'])

'''
Diversity file
'''
DIVERSITY_FILE = str(filenames['diversity_file'])

'''
HD file
'''
HD_FILE = str(filenames['hd_file'])


'''
GSI FILE
'''
GSI_FILE = str(filenames['gsi_file'])

'''
REPORT FILE
'''
REPORT = str(filenames['report_file'])

'''
FINAL_REPORT FILE
'''
FINAL_REPORT = str(filenames['final_report'])

'''
PLOT FILE
'''
PLOT = str(filenames['plot'])

'''
PREDICTION INTERVAL FILES
'''
PRED_INTERVAL_FILE = str(filenames['pred_interval_file'])
PRED_INTERVAL_TXT_FILE = str(filenames['pred_interval_txt_file'])


'''
I/O Directory details for main file
'''

INPUT_UNCLUSTERED = 'fasta'
INPUT_CLUSTERED = 'clustered_fasta'
OUTPUT = 'output'
HTML_OUTPUT = OUTPUT

'''
Threshold GSI
'''
THRESHOLD_GSI = float(mainconfig['threshold_gsi'])

'''
Parameters for gsi
'''
GAPS_IGNORE = bool(mainconfig['gaps_ignore'])
GSI_UNCLUSTERED = INPUT_UNCLUSTERED + os.sep + GSI_FILE
GSI_CLUSTERED = INPUT_CLUSTERED + os.sep + GSI_FILE
GSI_NUM = str(mainconfig['gsi_num'])

'''
Parameters for diversity
'''
DIVERSITY_UNCLUSTERED = INPUT_UNCLUSTERED + os.sep + DIVERSITY_FILE
DIVERSITY_CLUSTERED = INPUT_CLUSTERED + os.sep + DIVERSITY_FILE

'''
Parameters for hd
'''
HD_UNCLUSTERED = INPUT_UNCLUSTERED + os.sep + HD_FILE
HD_CLUSTERED = INPUT_CLUSTERED + os.sep + HD_FILE


'''
Parameters for clustering
'''
THRESHOLD = float(mainconfig['threshold_clustering'])
DIVERSITY_THRESHOLD = float(mainconfig['threshold_diversity'])

'''
Columns
'''
COLS = ['#SUBJECT', 'TIME', 'TYPE', 'DIVERSITY', 'VAR', 'BETA', 'GSI', 'NUM_SEQ', 'EFFECTIVE_DIVERSITY',
        'VAR(After Clustering)', 'BETA(After Clustering)', 'EFFECTIVE_GSI', 'NUM_SEQ(After Clustering)', 'CLUSTERED', 'CLUSTERS']

'''
TYPE
'''
TYPES = ['chronic', 'longi']

'''
Threshold NUMSEQ 
'''
THRESHOLD_NUMSEQ = int(mainconfig['threshold_numseq'])

'''
Prediction Interval Configuration
'''
FIT_SLOPE = float(predictioninterval['fit_slope'])
FIT_INTERCEPT = float(predictioninterval['fit_intercept'])
LOWER_SLOPE = float(predictioninterval['lower_slope'])
LOWER_INTERCEPT = float(predictioninterval['lower_intercept'])
UPPER_SLOPE = float(predictioninterval['upper_slope'])
UPPER_INTERCEPT = float(predictioninterval['upper_intercept'])


'''
HTML Template file
'''
TEMPLATE = str(html['html_template'])
IMAGE_WIDTH = str(html['image_width'])
IMAGE_HEIGHT = str(html['image_height'])

'''
EFFECTIVE DIVERSITY THRESHOLD (for chronic)
'''
EFFECTIVE_DIVERSITY_TH = float(mainconfig['effective_diversity_th'])