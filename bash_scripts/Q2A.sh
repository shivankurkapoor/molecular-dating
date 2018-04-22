#!/usr/bin/env bash
#source /home/spark/moleculardating/mol_dat_venv/bin/activate
cd /home/spark/moleculardating/scripts/H4
/home/spark/ParallelIntegratedWebPage/my_virtual_env/bin/python /home/spark/moleculardating/scripts/H4/main.py --request_idx=$2 --align=True --request_id=$1 --input=/home/spark/moleculardating/result/$1/$2 --html_dir=/home/spark/moleculardating/application/templates/result/$1

python /home/spark/moleculardating/scripts/fastq_to_fasta.py 
--backward_primer=backward_primer --base_count=base_count --forward_file=forward_file file_path --percent=base_percent --backward_file=backward_file file_path 
--forward_primer=forward_primer --seq_len=seq_len 

--request_id=$1
--request_idx=$2
--output_dir=/home/spark/moleculardating/result/$1/$2/fasta 

