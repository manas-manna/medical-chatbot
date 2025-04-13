#!/bin/sh

echo ">> Waiting for Vault to be ready..."
sleep 3

export VAULT_ADDR=http://localhost:8200
export VAULT_TOKEN=root

echo ">> Writing secrets to Vault..."

vault kv put secret/expense-tracker/backend \
  SPRING_DATASOURCE_URL=jdbc:postgresql://postgres:5432/expense_tracker \
  SPRING_DATASOURCE_USERNAME=postgres \
  SPRING_DATASOURCE_PASSWORD=postgres

echo "✅ Vault secrets initialized."
