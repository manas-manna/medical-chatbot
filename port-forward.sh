#!/bin/bash

echo "🔁 Killing any existing port-forward processes..."
pkill -f "kubectl port-forward" || true

LOG_DIR=~/logs
mkdir -p "$LOG_DIR"

echo "🚀 Starting port-forwarding in background..."

nohup kubectl port-forward service/frontend -n medical-chatbot 3000:80 > "$LOG_DIR/frontend.log" 2>&1 &
nohup kubectl port-forward service/backend -n medical-chatbot 8000:8000 > "$LOG_DIR/backend.log" 2>&1 &
nohup kubectl port-forward service/elasticsearch -n medical-chatbot 9200:9200 > "$LOG_DIR/elasticsearch.log" 2>&1 &
nohup kubectl port-forward service/logstash -n medical-chatbot 5044:5044 > "$LOG_DIR/logstash.log" 2>&1 &
nohup kubectl port-forward service/kibana -n medical-chatbot 5601:5601 > "$LOG_DIR/kibana.log" 2>&1 &

echo "✅ Port forwarding started in background. Logs in $LOG_DIR"
