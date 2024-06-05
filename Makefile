NGROK_PID_FILE = /tmp/ngrok.pid

.PHONY: download_data merge_data deploy_env deploy_agent stop_agent deploy_jenkins stop_jenkins

download_data:
	python3 ./scripts/download_raw_data.py

merge_data:
	python3 ./scripts/merge_data.py

deploy_env:
	rsync -avr .env src/data/pipeline/.env
	rsync -avr .env src/data/mtl_pipeline/.env
	rsync -avr .env src/data/training_pipeline/.env
	rsync -avr .env src/data/model_serving/.env
	rsync -avr .env src/data/model_serving/deloyment/.env
	rsync -avr .env minikube

deploy_agent:
	java -jar agent.jar -url http://localhost:8080/ -secret @secret-file -name "jenkins-agent" -workDir "/home/kyphan38/thesis/mlops-platform" > agent.log 2>&1 &

stop_agent:
	@pid=$$(ps aux | grep '[a]gent.jar' | awk '{print $$2}'); if [ -n "$$pid" ]; then kill $$pid; echo "Agent stopped"; else echo "No agent process found"; fi

deploy_jenkins:
	@echo "Starting ngrok..."
	ngrok http 8080 --log=stdout > /dev/null & echo $$! > $(NGROK_PID_FILE)
	sleep 2
	@echo "Retrieving ngrok URL..."
	@NGROK_URL=$$(curl -s http://127.0.0.1:4045/api/tunnels | jq -r '.tunnels[0].public_url'); \
	echo "Ngrok URL: $$NGROK_URL"

stop_jenkins:
	@if [ -f $(NGROK_PID_FILE) ]; then \
		NGROK_PID=$$(cat $(NGROK_PID_FILE)); \
		kill $$NGROK_PID; \
		rm $(NGROK_PID_FILE); \
		echo "Ngrok process stopped."; \
	else \
		echo "No ngrok process found."; \
	fi
