download-data:
	python3 ./scripts/download_raw_data.py

merge-data:
	python3 ./scripts/merge_data.py

deploy-env:
	rsync -avr .env src/data/pipeline/.env
	rsync -avr .env src/data/mtl_pipeline/.env
	rsync -avr .env src/data/training_pipeline/.env
