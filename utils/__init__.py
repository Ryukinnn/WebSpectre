"""
WebSpectre Framework - Utilities Package
Developer: Ryukinnn
"""

from .validator import is_valid_url, is_valid_ip, normalize_target
from .network import fetch_url, fetch_headers, fetch_advanced

__all__ = [
    "is_valid_url",
    "is_valid_ip",
    "normalize_target",
    "fetch_url",
    "fetch_headers",
    "fetch_advanced"
]
