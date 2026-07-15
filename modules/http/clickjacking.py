"""
WebSpectre Framework - Clickjacking Module
Developer: Ryukinnn
"""

from core.base import BaseModule
from utils.network import fetch_advanced
from utils.validator import normalize_target

class ClickjackingModule(BaseModule):
    def __init__(self):
        super().__init__()
        self.meta = {
            "name": "Clickjacking Protection Analysis",
            "description": "Memeriksa kerentanan Clickjacking (UI Redressing) dengan menganalisis header X-Frame-Options dan CSP.",
            "author": "Ryukinnn",
            "version": "1.0.0",
            "category": "HTTP Analysis",
            "risk_level": "MEDIUM"
        }

    def setup(self) -> bool:
        return True

    async def execute(self, target: str) -> None:
        target = normalize_target(target)
        response = await fetch_advanced(target)
        
        if not response:
            return
            
        headers = {k.lower(): v for k, v in response["headers"].items()}
        
        xfo = headers.get("x-frame-options", "").upper()
        csp = headers.get("content-security-policy", "").lower()
        
        is_protected = False
        
        if xfo in ["DENY", "SAMEORIGIN"]:
            is_protected = True
            
        if "frame-ancestors" in csp:
            is_protected = True
            
        if is_protected:
            self.add_finding(
                title="Proteksi Clickjacking Aktif",
                description="Target terlindungi dari Clickjacking (X-Frame-Options atau CSP frame-ancestors dikonfigurasi).",
                severity="INFO"
            )
        else:
            self.add_finding(
                title="Rentan Terhadap Clickjacking",
                description="Website dapat disematkan ke dalam <iframe> asing. Penyerang dapat menipu pengguna untuk melakukan tindakan yang tidak diinginkan.",
                severity="MEDIUM"
            )

    def cleanup(self) -> None:
        pass
