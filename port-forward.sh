#!/bin/bash
pkill -f "kubectl port-forward" || true
echo "🚀 Starting port-forwarding in background"

nohup kubectl port-forward service/frontend -n medical-chatbot 3000:80 > /tmp/frontend.log 2>&1 &
nohup kubectl port-forward service/backend -n medical-chatbot 8000:8000 > /tmp/backend.log 2>&1 &
nohup kubectl port-forward service/elasticsearch -n medical-chatbot 9200:9200 > /tmp/elasticsearch.log 2>&1 &
nohup kubectl port-forward service/logstash -n medical-chatbot 5044:5044 > /tmp/logstash.log 2>&1 &
nohup kubectl port-forward service/kibana -n medical-chatbot 5601:5601 > /tmp/kibana.log 2>&1 &

echo "✅ Port forwarding started in background"