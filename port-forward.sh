#!/bin/bash
pkill -f "kubectl port-forward" || true
kubectl port-forward service/frontend -n medical-chatbot 3000:80 &
kubectl port-forward service/backend -n medical-chatbot 8000:8000 &
kubectl port-forward service/elasticsearch -n medical-chatbot 9200:9200 &
kubectl port-forward service/logstash -n medical-chatbot 5044:5044 &
kubectl port-forward service/kibana -n medical-chatbot 5601:5601 &
wait
