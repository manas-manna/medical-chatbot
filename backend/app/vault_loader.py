import hvac
import os

VAULT_URL = os.getenv("VAULT_URL")
VAULT_TOKEN = os.getenv("VAULT_TOKEN") 

def load_secrets_from_vault():
    try:
        client = hvac.Client(url=VAULT_URL, token=VAULT_TOKEN)
        response = client.secrets.kv.v2.read_secret_version(
            path='myapp', mount_point='secret'
        )
        secrets = response['data']['data']
        for k, v in secrets.items():
            os.environ[k] = v
        return secrets
    except Exception as e:
        print(f"Vault error: {e}")
        return {}