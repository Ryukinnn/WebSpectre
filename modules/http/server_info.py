"""
WebSpectre Framework - Server Information Disclosure Module
Developer: Ryukinnn
"""

from core.base import BaseModule
from utils.network import fetch_headers
from utils.validator import normalize_target

class ServerInfoModule(BaseModule):
    def __init__(self):
        super().__init__()
        self.meta = {
            "name": "Server Information Disclosure",
            "description": "Mendeteksi pengeksposan informasi teknologi server melalui HTTP Headers.",
            "author": "Ryukinnn",
            "version": "1.0.0",
            "category": "HTTP Analysis",
            "risk_level": "LOW"
        }

    def setup(self) -> bool:
        return True

    async def execute(self, target: str) -> None:
        target = normalize_target(target)
        headers = await fetch_headers(target)
        
        if not headers:
            return
            
        headers_lower = {k.lower(): v for k, v in headers.items()}
        
        # Mengecek header yang sering mengekspos teknologi backend
        leaked_info = {}
        if "server" in headers_lower:
            leaked_info["Server"] = headers_lower["server"]
        if "x-powered-by" in headers_lower:
            leaked_info["X-Powered-By"] = headers_lower["x-powered-by"]
        if "x-aspnet-version" in headers_lower:
            leaked_info["X-AspNet-Version"] = headers_lower["x-aspnet-version"]
            
        if leaked_info:
            details = "\n- ".join([f"{k}: {v}" for k, v in leaked_info.items()])
            self.add_finding(
                title="Informasi Server Terekspos",
                description=f"Ditemukan header yang mengekspos versi perangkat lunak atau teknologi backend:\n- {details}",
                severity="LOW"
            )
        else:
            self.add_finding(
                title="Penyembunyian Informasi Server",
                description="Target berhasil menyembunyikan identitas perangkat lunak server (Server Header disamarkan/dihapus).",
                severity="INFO"
            )

    def cleanup(self) -> None:
        pass
