"""
WebSpectre Framework - DNS Records Discovery Module
Developer: Ryukinnn
"""

import socket
import urllib.parse
from core.base import BaseModule

class DNSRecordsModule(BaseModule):
    def __init__(self):
        super().__init__()
        self.meta = {
            "name": "DNS Records Analysis",
            "description": "Mengumpulkan informasi DNS dasar (A Record) untuk menemukan alamat IP server.",
            "author": "Ryukinnn",
            "version": "1.0.0",
            "category": "Discovery",
            "risk_level": "INFO"
        }

    def setup(self) -> bool:
        return True

    async def execute(self, target: str) -> None:
        try:
            # Mengambil hostname murni tanpa scheme (http/https)
            parsed = urllib.parse.urlparse(target)
            hostname = parsed.netloc or parsed.path
            
            # Menghapus port jika ada
            if ":" in hostname:
                hostname = hostname.split(":")[0]

            # Melakukan resolusi DNS
            ip_address = socket.gethostbyname(hostname)
            
            self.add_finding(
                title=f"Resolusi DNS (A Record) untuk {hostname}",
                description=f"Domain berhasil di-resolve ke alamat IP: {ip_address}",
                severity="INFO"
            )
        except socket.gaierror:
            self.add_finding(
                title="Kegagalan Resolusi DNS",
                description="Gagal memetakan domain ke alamat IP. Pastikan target valid.",
                severity="LOW"
            )
        except Exception as e:
            self.add_finding(
                title="Kesalahan Modul DNS",
                description=f"Terjadi kesalahan saat memproses DNS: {str(e)}",
                severity="INFO"
            )

    def cleanup(self) -> None:
        pass
