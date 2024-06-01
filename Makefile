download_data:
	python3 ./scripts/download_raw_data.py

merge_data:
	python3 ./scripts/merge_data.py

deploy_env:
	rsync -avr .env src/data/pipeline/.env
	rsync -avr .env src/data/mtl_pipeline/.env
	rsync -avr .env src/data/training_pipeline/.env

deploy_agent:
	java -jar agent.jar -url http://localhost:8080/ -secret @secret-file -name "jenkins-agent" -workDir "/home/kyphan38/thesis/mlops-platform" > agent.log 2>&1 &
	
stop_agent:
	-@pid=$$(ps aux | grep '[a]gent.jar' | awk '{print $$2}'); if [ -n "$$pid" ]; then kill $$pid; echo "Agent stopped"; else echo "No agent process found"; fi
