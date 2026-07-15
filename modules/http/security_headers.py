"""
WebSpectre Framework - Security Headers Module
Developer: Ryukinnn
"""

from core.base import BaseModule
from utils.network import fetch_headers
from utils.validator import normalize_target

class SecurityHeadersModule(BaseModule):
    def __init__(self):
        super().__init__()
        self.meta = {
            "name": "Security Headers Analysis",
            "description": "Menganalisis keberadaan dan konfigurasi HTTP Security Headers.",
            "author": "Ryukinnn",
            "version": "1.0.0",
            "category": "HTTP Analysis",
            "risk_level": "MEDIUM"
        }
        
        # Daftar header keamanan standar industri
        self.expected_headers = {
            "Strict-Transport-Security": "Mencegah serangan downgrade HTTP (HSTS).",
            "Content-Security-Policy": "Mencegah XSS dan injeksi data (CSP).",
            "X-Frame-Options": "Mencegah serangan Clickjacking.",
            "X-Content-Type-Options": "Mencegah MIME-sniffing (harus 'nosniff').",
            "Referrer-Policy": "Melindungi privasi referer pengguna."
        }

    def setup(self) -> bool:
        return True

    async def execute(self, target: str) -> None:
        target = normalize_target(target)
        headers = await fetch_headers(target)
        
        if not headers:
            self.add_finding(
                title="Gagal Mengambil Header",
                description="Tidak dapat terhubung ke target untuk memeriksa header keamanan.",
                severity="INFO"
            )
            return
            
        # Mengonversi header ke lowercase untuk mempermudah pencarian (case-insensitive)
        headers_lower = {k.lower(): v for k, v in headers.items()}
        
        missing_headers = []
        for header, desc in self.expected_headers.items():
            if header.lower() not in headers_lower:
                missing_headers.append(f"{header} ({desc})")
                
        if missing_headers:
            self.add_finding(
                title="Security Headers Tidak Lengkap",
                description=f"Ditemukan {len(missing_headers)} header keamanan yang tidak dikonfigurasi: \n- " + "\n- ".join(missing_headers),
                severity="MEDIUM"
            )
        else:
            self.add_finding(
                title="Security Headers Lengkap",
                description="Target telah mengonfigurasi header keamanan standar dengan baik.",
                severity="INFO"
            )

    def cleanup(self) -> None:
        pass
