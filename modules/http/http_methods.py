"""
WebSpectre Framework - HTTP Methods Module
Developer: Ryukinnn
"""

from core.base import BaseModule
from utils.network import fetch_advanced
from utils.validator import normalize_target

class HTTPMethodsModule(BaseModule):
    def __init__(self):
        super().__init__()
        self.meta = {
            "name": "HTTP Methods Analysis",
            "description": "Mendeteksi metode HTTP berbahaya yang diaktifkan (seperti PUT, DELETE).",
            "author": "Ryukinnn",
            "version": "1.0.0",
            "category": "HTTP Analysis",
            "risk_level": "LOW"
        }

    def setup(self) -> bool:
        return True

    async def execute(self, target: str) -> None:
        target = normalize_target(target)
        
        # Mengirim OPTIONS request
        response = await fetch_advanced(target, method="OPTIONS")
        
        if not response:
            return
            
        headers = {k.lower(): v for k, v in response["headers"].items()}
        allowed_methods = headers.get("allow", "").upper()
        
        if not allowed_methods:
            self.add_finding(
                title="Metode HTTP Tidak Diketahui",
                description="Server tidak membalas header 'Allow' pada request OPTIONS.",
                severity="INFO"
            )
            return
            
        dangerous_methods = ["PUT", "DELETE", "TRACE", "TRACK"]
        found_dangerous = [m for m in dangerous_methods if m in allowed_methods]
        
        if found_dangerous:
            self.add_finding(
                title="Metode HTTP Berbahaya Terdeteksi",
                description=f"Server mengizinkan metode HTTP yang berpotensi berbahaya: {', '.join(found_dangerous)}",
                severity="MEDIUM"
            )
        else:
            self.add_finding(
                title="Metode HTTP Aman",
                description=f"Metode yang diizinkan terpantau aman: {allowed_methods}",
                severity="INFO"
            )

    def cleanup(self) -> None:
        pass
