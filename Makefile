download_data:
	python3 ./scripts/download_raw_data.py

merge_data:
	python3 ./scripts/merge_data.py

deploy_env:
	rsync -avr .env src/data/pipeline/.env
	rsync -avr .env src/data/mtl_pipeline/.env
	rsync -avr .env src/data/training_pipeline/.env

deploy_agent:
	java -jar configs/jenkins/agent/agent.jar -url http://localhost:8080/ -secret @configs/jenkins/agent/secret-file -name agent -workDir "$(PWD)" > configs/jenkins/agent/agent.log 2>&1 &

stop_agent:
	-@pid=$$(ps aux | grep '[a]gent.jar' | awk '{print $$2}'); if [ -n "$$pid" ]; then kill $$pid; echo "Agent stopped"; else echo "No agent process found"; fi
