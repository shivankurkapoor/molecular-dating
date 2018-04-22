#!/usr/bin/env bash
#source /home/spark/moleculardating/mol_dat_venv/bin/activate
cd /home/spark/moleculardating/scripts/H4
/home/spark/ParallelIntegratedWebPage/my_virtual_env/bin/python /home/spark/moleculardating/scripts/H4/main.py --request_idx=$2 --align=True --request_id=$1 --input=/home/spark/moleculardating/result/$1/$2 --html_dir=/home/spark/moleculardating/application/templates/result/$1
