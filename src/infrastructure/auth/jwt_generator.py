from datetime import datetime
from datetime import UTC
from typing import Any

import jwt
from cryptography.hazmat.primitives import serialization

from config import get_settings
from infrastructure.auth.jwt_test import payload

settings = get_settings()


def generate_jwt(payload: dict[str, Any]) -> str:
    now = datetime.now(UTC)
    private_key_text = (
            settings.BASE_DIR / 'src' / 'infrastructure' / 'auth'
            / 'product_service_private_key.pem'
    ).read_text()
    private_key = serialization.load_pem_private_key(
        private_key_text.encode(),
        password=None,
    )
    return jwt.encode(payload=payload, key=private_key, algorithm='RS256')


if __name__ == '__main__':
    print(generate_jwt(payload))
