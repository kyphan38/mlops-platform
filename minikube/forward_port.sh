#!/bin/bash

API_POD_NAME=$(kubectl get pods | grep -i api | awk '{print $1}')
echo "API Pod Name: ${API_POD_NAME}"

# Get the name of the Prometheus pod
PROMETHEUS_POD_NAME=$(kubectl get pods | grep -i prometheus | awk '{print $1}')
echo "Prometheus Pod Name: ${PROMETHEUS_POD_NAME}"

# Get the name of the Grafana pod
GRAFANA_POD_NAME=$(kubectl get pods | grep -i grafana | awk '{print $1}')
echo "Grafana Pod Name: ${GRAFANA_POD_NAME}"

# Port forward to the new API pod
nohup kubectl port-forward "${API_POD_NAME}" 7000:7000 > api-model-port-forward.log 2>&1 &

# Port forward to the Prometheus pod (uncomment if needed)
nohup kubectl port-forward "${PROMETHEUS_POD_NAME}" 9090:9090 > prometheus-port-forward.log 2>&1 &

# Port forward to the Grafana pod (uncomment if needed)
nohup kubectl port-forward "${GRAFANA_POD_NAME}" 3000:3000 > grafana-port-forward.log 2>&1 &