import uuid


def generate_secret_key(username: str) -> str:
    try:
        secret_key = uuid.uuid4().hex
        return secret_key + username
    except Exception as e:
        raise RuntimeError(f"Failed to generate secret key:{str(e)}")
