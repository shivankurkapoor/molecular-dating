#!/usr/bin/env bash
source /home/spark/moleculardating/mol_dat_venv/bin/activate
cd /home/spark/moleculardating/scripts
python /home/spark/moleculardating/scripts/fastq_to_fasta.py --backward_primer= --base_count=0 --forward_file=/home/spark/moleculardating/result/05BQA051/0/fastq/forward_file_0.fastq --percent=0 --backward_file=/home/spark/moleculardating/result/05BQA051/0/fastq/backward_file_0.fastq --output_dir=/home/spark/moleculardating/result/05BQA051/0/fasta --request_id=05BQA051 --forward_primer= --seq_len=250 --request_idx=0