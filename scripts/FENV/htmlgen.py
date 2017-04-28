import os
from shutil import copyfile
import pandas as pd
from utils import GSI_NUM
from utils import TEMPLATE, IMAGE_HEIGHT, IMAGE_WIDTH
from jinja2 import Environment, FileSystemLoader

PATH = os.getcwd()
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, 'templates')),
    trim_blocks=False)


local_css_path = '/home/leelab/PycharmProjects/moleculardating/scripts/FENV/static/style.css'

def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)


def create_html(INPUT, OUTPUT, REQUEST_TYPE, REQUEST_ID):
    try:
        gsi_num = GSI_NUM[-1]
        df = pd.read_csv(INPUT, dtype={"#SUBJECT": "string",
                                       "Single Lineage Diversity": "string",
                                       "Single Lineage GSI": "string",
                                       "Single Lineage Variance": "string",
                                       "Diversity": "string",
                                       "GSI": "string",
                                       "Variance": "string"},
                         index_col=False)
        for index, row in df.iterrows():
            time = float(row['TIME'])
            subject = str(row['#SUBJECT']).split('_', 1)[0]
            clustered = str(row['CLUSTERED'])
            days_since_infection = str(row['Days Since Infection'])
            row_df = pd.DataFrame([dict(row)])
            row_df = row_df.drop('#SUBJECT', 1)
            row_df = row_df.drop('TIME', 1)
            row_df = row_df.drop('Days Since Infection', 1)
            row_df = row_df.drop('CLUSTERED', 1)

            row_df = row_df[
                ['Single Lineage Diversity', 'Single Lineage GSI', 'Single Lineage Variance', 'Diversity', 'GSI',
                 'Variance']]

            if clustered == 'NO':
                row_df = row_df.drop('Single Lineage Diversity', 1)
                row_df = row_df.drop('Single Lineage GSI', 1)
                row_df = row_df.drop('Single Lineage Variance', 1)
            row_df = row_df.transpose()
            row_df = row_df.reset_index()
            row_df = row_df.rename(columns={'index': 'Attribute', 0: 'Value'})
            fname = OUTPUT + os.sep + REQUEST_ID + '.html'
            table = row_df.to_html(classes='page', justify='center', index=False, header=False)
            # For subscript notation
            table = table.replace('GSI', 'GSI<sub>' + gsi_num + '</sub>')

            if REQUEST_TYPE == 'SINGLE':
                graph_unclustered = '../../../static/images/' + REQUEST_ID + '_UNCLUSTERED.png'
                css = '../../../static/style/style_process.css'
            else:
                graph_unclustered = REQUEST_ID + '_UNCLUSTERED.png'
                css = 'style.css'
                copyfile(local_css_path,
                         os.path.join(OUTPUT, 'style.css'))
            context = {
                'title': 'Prediction Interval',
                'subject': 'Fasta File: ' + subject + '.fasta',
                'unclustered_header': 'Whole',
                'graph_unclustered': graph_unclustered,
                'prediction_interval': days_since_infection,
                'table': table,
                'h1': IMAGE_HEIGHT,
                'w1': IMAGE_WIDTH,
                'css': css
            }
            if clustered == 'YES':
                if REQUEST_TYPE == 'SINGLE':
                    graph_clustered = '../../../static/images/' + REQUEST_ID + '_CLUSTERED.png'
                else:
                    graph_clustered = REQUEST_ID + '_CLUSTERED.png'
                context.update({
                    'clustered_header': 'Single Lineage',
                    'graph_clustered': graph_clustered,
                    'h2': IMAGE_HEIGHT,
                    'w2': IMAGE_WIDTH
                })
            with open(fname, 'w') as f:
                html = render_template(TEMPLATE, context)
                print 'HTMLPRINT'
                f.write(html)
    except Exception as e:
        print 'Error in generating html file ', e
