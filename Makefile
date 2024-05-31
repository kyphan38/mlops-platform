download_data:
	python3 ./scripts/download_raw_data.py

merge_data:
	python3 ./scripts/merge_data.py

deploy_env:
	rsync -avr .env src/data/pipeline/.env
	rsync -avr .env src/data/mtl_pipeline/.env
	rsync -avr .env src/data/training_pipeline/.env
