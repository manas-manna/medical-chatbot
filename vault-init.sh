#!/bin/sh

echo ">> Waiting for Vault to be ready..."
sleep 3

export VAULT_ADDR=http://localhost:8200
export VAULT_TOKEN=root

echo ">> Writing secrets to Vault..."

vault kv put secret/expense-tracker \
  spring.datasource.url=jdbc:postgresql://postgres:5432/expense_tracker \
  spring.datasource.username=postgres \
  spring.datasource.password=postgres


echo "✅ Vault secrets initialized."
