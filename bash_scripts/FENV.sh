#!/usr/bin/env bash
cd /home/spark/moleculardating/scripts/FENV
/home/spark/ParallelIntegratedWebPage/my_virtual_env/bin/python /home/spark/moleculardating/scripts/FENV/main.py --request_idx=$2 --align=False --request_id=$1 --input=/home/spark/moleculardating/result/$1/$2 --html_dir=/home/spark/moleculardating/application/templates/result/$1
