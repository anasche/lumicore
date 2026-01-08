import os

def get_env(key: str, default=None, required=False):
    value = os.getenv(key, default)

    if required and value is None:
        raise RuntimeError(f"Missing required environment variable: {key}")

    return value


# ------------------------
# External API Config
# ------------------------
BASE_API = get_env(
    "BASE_API",
    "https://fast-endpoint-production.up.railway.app"
)

CANDIDATE_ID = get_env(
    "CANDIDATE_ID",
    required=True
)

# ------------------------
# Django Core
# ------------------------
DEBUG = get_env("DEBUG", "False") == "True"
SECRET_KEY = get_env("SECRET_KEY", "unsafe-local-secret")
