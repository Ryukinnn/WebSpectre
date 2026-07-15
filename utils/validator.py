"""
WebSpectre Framework - Target Validator Utility
Developer: Ryukinnn

Utilitas untuk memvalidasi dan membersihkan input pengguna.
"""

import re
from urllib.parse import urlparse

def is_valid_url(url: str) -> bool:
    """Memeriksa apakah string adalah URL yang valid secara format."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def is_valid_ip(ip: str) -> bool:
    """Memeriksa apakah string adalah alamat IPv4 yang valid."""
    pattern = re.compile(
        r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}"
        r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    )
    return bool(pattern.match(ip))

def normalize_target(target: str) -> str:
    """Menormalisasi input pengguna (menambahkan skema http/https jika hilang)."""
    target = target.strip()
    if not target.startswith(("http://", "https://")):
        return f"http://{target}"
    return target
