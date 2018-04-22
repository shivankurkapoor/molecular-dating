HOST=192.168.22.2
PORT=5000
run:    
	~/moleculardating/mol_dat_venv/bin/gunicorn -w $(w) -b $(HOST):$(PORT) application:application -t 120
.PHONY: run
