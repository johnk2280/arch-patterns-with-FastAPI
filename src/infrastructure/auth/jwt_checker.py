from typing import Any

from cryptography.x509 import load_pem_x509_certificate

from config import get_settings

settings = get_settings()


def check_jwt(token: str) -> dict[str, Any]:
    public_key_text = (
            settings.BASE_DIR / 'src' / 'infrastructure' / 'auth'
            / 'product_service_public_key.pem'
    ).read_text()
    public_key = load_pem_x509_certificate(public_key_text.encode())
    return
