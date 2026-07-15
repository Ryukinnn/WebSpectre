"""
WebSpectre Framework - CORS Review Module
Developer: Ryukinnn
"""

from core.base import BaseModule
from utils.network import fetch_advanced
from utils.validator import normalize_target

class CORSReviewModule(BaseModule):
    def __init__(self):
        super().__init__()
        self.meta = {
            "name": "CORS Misconfiguration Analysis",
            "description": "Menguji konfigurasi Cross-Origin Resource Sharing (CORS) yang lemah.",
            "author": "Ryukinnn",
            "version": "1.0.0",
            "category": "HTTP Analysis",
            "risk_level": "HIGH"
        }

    def setup(self) -> bool:
        return True

    async def execute(self, target: str) -> None:
        target = normalize_target(target)
        test_origin = "https://evil-webspectre-test.com"
        headers_req = {"Origin": test_origin, "User-Agent": "WebSpectre/1.0.0 (Security Assessment)"}
        
        response = await fetch_advanced(target, method="GET", headers=headers_req)
        
        if not response:
            return
            
        headers = {k.lower(): v for k, v in response["headers"].items()}
        
        acao = headers.get("access-control-allow-origin", "")
        acac = headers.get("access-control-allow-credentials", "")
        
        if acao == "*" or acao == test_origin:
            risk = "HIGH" if acac.lower() == "true" else "MEDIUM"
            self.add_finding(
                title="CORS Misconfiguration Terdeteksi",
                description=f"Server mengizinkan Origin '{acao}' sembarangan.\nCredentials Allow: {acac}",
                severity=risk
            )
        else:
            self.add_finding(
                title="Konfigurasi CORS Aman",
                description="Server tidak memantulkan origin asing atau menerapkan wildcard secara tidak aman.",
                severity="INFO"
            )

    def cleanup(self) -> None:
        pass
