#!/bin/bash

# Kill any existing port forwards
pkill -f "kubectl port-forward"

# Application services
kubectl port-forward service/frontend -n expense-tracker 3000:80 &
echo "Frontend running at http://localhost:3000"

kubectl port-forward service/backend -n expense-tracker 9000:9000 &
echo "Backend running at http://localhost:9000"

kubectl port-forward service/fraud-detection -n expense-tracker 8000:8000 &
echo "Fraud Detection running at http://localhost:8000"

kubectl port-forward service/postgres -n expense-tracker 5432:5432 &
echo "PostgreSQL running at localhost:5432"

# Infrastructure services
kubectl port-forward service/elasticsearch -n expense-tracker 9200:9200 &
echo "Elasticsearch running at http://localhost:9200"

kubectl port-forward service/logstash -n expense-tracker 5044:5044 &
echo "Logstash running at localhost:5044"

kubectl port-forward service/kibana -n expense-tracker 5601:5601 &
echo "Kibana running at http://localhost:5601"

kubectl port-forward service/vault -n expense-tracker 8200:8200 &
echo "Vault running at http://localhost:8200"

echo "Press Ctrl+C to stop all port forwarding"
wait
