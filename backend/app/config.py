# from pydantic import BaseSettings
# from typing import Optional

# class Settings(BaseSettings):
#     SECRET_KEY: str
#     MONGODB_URL: str
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
#     class Config:
#         env_file = ".env"

# settings = Settings()

import os
from pydantic import BaseSettings
from typing import Literal, Optional
from app.vault_loader import load_secrets_from_vault

# Attempt to load secrets from Vault
vault_secrets = load_secrets_from_vault()

# Track where secrets came from
SECRETS_SOURCE: Literal["vault", "env"] = "vault" if vault_secrets else "env"

class Settings(BaseSettings):
    SECRET_KEY: str
    MONGODB_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"  # fallback

settings = Settings()

# Log where the secrets came from
print(f"🔍 Config loaded from: {SECRETS_SOURCE.upper()}")
