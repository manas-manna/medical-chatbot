#!/bin/bash
# Kill any existing port forwards
pkill -f "kubectl port-forward" || true
# Application services
kubectl port-forward service/frontend -n medical-chatbot 3000:80 &
echo "Frontend running at http://localhost:3000"
kubectl port-forward service/backend -n medical-chatbot 8000:8000 &
echo "Backend running at http://localhost:8000"
# Infrastructure services
kubectl port-forward service/elasticsearch -n medical-chatbot 9200:9200 &
echo "Elasticsearch running at http://localhost:9200"
kubectl port-forward service/logstash -n medical-chatbot 5044:5044 &
echo "Logstash running at localhost:5044"
kubectl port-forward service/kibana -n medical-chatbot 5601:5601 &
echo "Kibana running at http://localhost:5601"
echo "Press Ctrl+C to stop all port forwarding"
wait
