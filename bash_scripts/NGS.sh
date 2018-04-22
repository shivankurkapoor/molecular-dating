#!/usr/bin/env bash
#source /home/spark/moleculardating/mol_dat_venv/bin/activate
cd /home/spark/moleculardating/scripts/NGS
/home/spark/ParallelIntegratedWebPage/my_virtual_env/bin/python /home/spark/moleculardating/scripts/NGS/main.py --request_idx=$2 --input_dir=/home/spark/moleculardating/result/$1/$2 --html_dir=/home/spark/moleculardating/application/templates/result/$1 --request_id=$1
